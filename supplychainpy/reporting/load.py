# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import concurrent
import datetime
import logging
import multiprocessing as mp
import os
import pickle
import re
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG, ABS_FILE_PICKLE
from supplychainpy._helpers._pickle_config import deserialise_config
from supplychainpy.bi.recommendation_generator import run_sku_recommendation, run_profile_recommendation
from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
from supplychainpy.inventory.summarise import Inventory
from supplychainpy.reporting.app import create_app
from supplychainpy.reporting.blueprints.models import Currency
from supplychainpy.reporting.blueprints.models import Forecast
from supplychainpy.reporting.blueprints.models import ForecastBreakdown
from supplychainpy.reporting.blueprints.models import ForecastStatistics
from supplychainpy.reporting.blueprints.models import ForecastType
from supplychainpy.reporting.blueprints.models import InventoryAnalysis
from supplychainpy.reporting.blueprints.models import MasterSkuList
from supplychainpy.reporting.blueprints.models import Orders
from supplychainpy.reporting.blueprints.models import TransactionLog, Recommendations, ProfileRecommendation
from supplychainpy.reporting.extensions import db
from supplychainpy.sample_data.config import ABS_FILE_PATH

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def currency_codes() -> dict:
    """ Retrives HTML Entity (decimal) for currency symbol.

    Returns:
        dict: Currency Symbols.

    """
    codes = {"AED": ("United Arab Emirates Dirham", "&#92;&#117;&#48;&#54;&#50;&#102;&#46;"),
             "ANG": ("Netherlands Antilles Guilder", "&#402"),
             "EUR": ("Euro Member Countries", "&#8364;"),
             "GBP": ("United Kingdom Pound", "&#163;"),
             "USD": ("United States Dollar", "&#36;"),
             }
    return codes


def _analysis_forecast_simple(analysis: UncertainDemand) -> dict:
    """ Retrieves simple_exponential_forecast from an instance of UncertainDemand.
        Function only required for Concurrent.futures.

    Args:
        analysis (UncertainDemand): Instance of UncertainDemand

    Returns:
        dict:   Forecast breakdown.
    """
    logging.log(logging.INFO,
                "Simple exponential smoothing forecast for SKU: {}\nObject id: {} ".format(
                    analysis.sku_id,
                    id(analysis)
                )
                )
    return analysis.simple_exponential_smoothing_forecast


def _analysis_forecast_holt(analysis: UncertainDemand) -> dict:
    """ Retrieves holts_exponential_forecast from an instance of UncertainDemand.
        Function only required for Concurrent.futures.

    Args:
        analysis (UncertainDemand): Instance of UncertainDemand

    Returns:
        dict:   Forecast breakdown.
    """
    logging.log(logging.INFO,
                "Holt's trend corrected exponential smoothing forecast for SKU: {}\nObject id: {} ".format(
                    analysis.sku_id,
                    id(analysis)
                )
                )
    return analysis.holts_trend_corrected_forecast


def load_currency(fx_codes: currency_codes(), ctx: db):
    """Loads Currency Symbols"""

    for key, value in fx_codes.items():
        codes = Currency()
        codes.country = value[0]
        codes.symbol = value[1]
        codes.currency_code = key
        ctx.session.add(codes)
    ctx.session.commit()


def batch(analysis, n):
    """Yield n-sized batches from analysis.
    Args:
        analysis:
        n:
    """

    for i in range(0, len(analysis), n):
        yield analysis[i:i + n]


def parallelise_ses(pickled_ses_batch_files: list, core_count: int) -> dict:
    """ Execute the exponential smoothing forecast in parallel.

    Args:
        pickled_ses_batch_files:   Uncertain demand objects batched for appropriate number of cores available on
                                    the host machine
        core_count:                 Number of cores available on the host machine, minus one.

    Returns:
        dict
    """
    attempts = 0
    simple_forecast = {}
    pickled_ses_batch_files_completed = []
    log.log(logging.INFO, 'Multiprocessing batch {} files using {} cores'.format(len(pickled_ses_batch_files), core_count))
    try:
        for num, batch_path in enumerate(pickled_ses_batch_files):
            order_batch = read_pickle(batch_path)[0]
            with ProcessPoolExecutor(max_workers=core_count) as executor:
                simple_forecast = {}
                ses_forecast_futures = {analysis.sku_id: executor.submit(_analysis_forecast_simple, analysis) for
                                        analysis in order_batch}
                ses_forecast_gen = {future: concurrent.futures.as_completed(ses_forecast_futures[future], timeout=20)
                                    for future
                                    in ses_forecast_futures}
                simple_forecast.update(
                    {value: ses_forecast_futures[value].result(timeout=30, ) for value in ses_forecast_gen})
                build_results_pickle(simple_forecast)
                log.log(logging.INFO, 'Batch processed: {}'.format(batch_path))
                pickled_ses_batch_files_completed.append(batch_path)
                # simple_forecast.clear()
                # ses_forecast_gen.clear()
                # ses_forecast_futures.clear()
                # del ses_forecast_futures
                # del ses_forecast_gen
                # del simple_forecast

        simple_forecast = retrieve_results_pickle()
        simple_forecast = simple_forecast[0]

        return simple_forecast
    except concurrent.futures.TimeoutError as err:
        print(err)
        attempts +=1
        pickled_ses_batch_files_remaining = set(pickled_ses_batch_files) -  set(pickled_ses_batch_files_completed)
        log.log(logging.INFO, 'ERROR processing batch. Retrying remaining batch files: {}'.format(pickled_ses_batch_files_remaining))
        for file_path in pickled_ses_batch_files_completed:
            remove_pickle(file_path)

        if len(pickled_ses_batch_files_remaining) > 0 and attempts > 4:
            parallelise_ses(pickled_ses_batch_files=list(pickled_ses_batch_files_remaining), core_count=core_count)
        else:
            print('The forecasting calculation process was unable to complete. Please check the source file.')
            return {}
    except OSError as err:
        print(err)


def parallelise_htc(batched_analysis: list, core_count: int):
    """ Execute the Holts' trend corrected smoothing forecast in parallel.

    Args:
        batched_analysis: Uncertain demand objects batched for appropriate number of cores available on the host machine
        core_count: Number of cores available on the host machine, minus one.

    Returns:
        dict
    """
    holts_forecast = {}
    try:
        for order_batch in batched_analysis:
            with ProcessPoolExecutor(max_workers=core_count) as executor:
                holts_forecast_futures = {analysis.sku_id: executor.submit(_analysis_forecast_holt, analysis) for
                                          analysis in order_batch}
                holts_forecast_gen = {future: concurrent.futures.as_completed(holts_forecast_futures[future]) for future
                                      in holts_forecast_futures}
                holts_forecast.update({value: holts_forecast_futures[value].result() for value in holts_forecast_gen})
    except TypeError as err:
        print('{}'.format(err))
    return holts_forecast


def write_pickle(**kwargs) -> str:
    """pickle data to file"""
    try:
        for k, v in kwargs.items():
            path = os.path.abspath(os.path.join(ABS_FILE_PICKLE, k))
            log.log(logging.INFO, 'Pickled file created at: {}'.format(path))
            with open(path, "wb") as ses:
                pickle.dump(v, ses)
            return path
    except OSError as err:
        print(err)
        return ''


def read_pickle(batch_path: str):
    """Read pickled data from file"""
    retrieved_pickle = []
    try:
        with open(batch_path, "r+b") as ses:
            log.log(logging.INFO, 'Pickled file retrieved from : {}'.format(ses))
            retrieved_pickle.append(pickle.load(ses))
        return retrieved_pickle
    except OSError as err:
        print(err)
        return retrieved_pickle


def remove_pickle(path: str):
    try:
        os.remove(path=path)
    except OSError as err:
        print('file not present. {}'.format(err))
        pass


def pickle_ses_forecast(batched_analysis: list) -> list:
    pickled_paths = []
    for num, item in enumerate(batched_analysis):
        filename = 'ses{}.pickle'.format(num)
        pickle_me = {filename: item}
        pickle_path = write_pickle(**pickle_me)
        pickled_paths.append(pickle_path)
    return pickled_paths


def build_results_pickle(ses_forecast_results: dict):
    filename = 'ses_forecast_results'
    path = os.path.abspath(os.path.join(ABS_FILE_PICKLE, filename))
    log.log(logging.INFO, 'Generating results pickle at: {}'.format(path))
    stored_ses_data = read_pickle(path)
    for i in stored_ses_data:
        ses_forecast_results.update(i)
    with open(path, "wb") as ses:
        pickle.dump(ses_forecast_results, ses)


def retrieve_results_pickle():
    filename = 'ses_forecast_results'
    path = os.path.abspath(os.path.join(ABS_FILE_PICKLE, filename))
    stored_ses_data = read_pickle(path)
    remove_pickle(path=path)
    return stored_ses_data


def cleanup_pickled_files():
    try:
        filename = 'ses_forecast_results'
        path = os.path.abspath(os.path.join(ABS_FILE_PICKLE, filename))
        remove_pickle(path=path)
        ses_file_regex = re.compile('[s][e][s]\d+[.][p][i][c][k][l][e]')
        for filename in os.listdir(ABS_FILE_PICKLE):
            if ses_file_regex.match(filename) and filename.endswith(".pickle"):
                path = os.path.abspath(os.path.join(ABS_FILE_PICKLE, filename))
                log.log(logging.INFO, 'Cleaning up pickled file at: {}'.format(path))
                remove_pickle(path)

    except FileNotFoundError as err:
        print(err)
        pass
    except OSError as err:
        print(err)


def load(file_path: str, location: str = None):
    """ Loads analysis and forecast into local database for reporting suite.

    Args:
        file_path (str):    File path to source file containing data for analysis.
        location (str):     Location of database to populate.

    """
    try:
        app = create_app()
        db.init_app(app)
        if location is not None and os.name in ['posix', 'mac']:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/reporting.db'.format(location)

        elif location is not None and os.name == 'nt':
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\reporting.db'.format(location)

        log.log(logging.DEBUG, 'Loading data analysis for reporting suite... \n')

        with app.app_context():
            db.create_all()
            log.log(logging.DEBUG, 'loading currency symbols...\n')
            print('loading currency symbols...\n')
            fx = currency_codes()
            load_currency(fx, db)

            print('loading currency symbols...[COMPLETED]\n')
            config = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
            currency = config.get('currency')

            log.log(logging.DEBUG, 'Analysing file: {}...\n'.format(file_path))
            print('Analysing file: {}...\n'.format(file_path))
            orders_analysis = model_inventory.analyse(file_path=file_path,
                                                      z_value=Decimal(1.28),
                                                      reorder_cost=Decimal(5000),
                                                      file_type="csv", length=12, currency=currency)

            ia = [analysis.orders_summary() for analysis in orders_analysis]
            date_now = datetime.datetime.now()
            analysis_summary = Inventory(processed_orders=orders_analysis)
            print('Analysing file: {}...[COMPLETED]\n\nCalculating Forecasts...\n'.format(file_path))
            log.log(logging.DEBUG, 'Calculating Forecasts...\n')

            cores = int(mp.cpu_count())
            cores -= 1
            batched_analysis = [i for i in batch(orders_analysis, cores)]
            pickled_paths = pickle_ses_forecast(batched_analysis=batched_analysis)
            try:
                simple_forecast = parallelise_ses(pickled_ses_batch_files=pickled_paths, core_count=cores)
            except:
                simple_forecast = {}
            cleanup_pickled_files()

            try:
                holts_forecast = parallelise_htc(batched_analysis=batched_analysis, core_count=cores)
            except:
                holts_forecast = {}

            transact = TransactionLog()
            transact.date = date_now
            db.session.add(transact)
            db.session.commit()

            transaction_sub = db.session.query(db.func.max(TransactionLog.date))
            transaction_id = db.session.query(TransactionLog).filter(TransactionLog.date == transaction_sub).first()
            load_profile_recommendations(analysed_order=orders_analysis, forecast=holts_forecast,
                                         transaction_log_id=transaction_id)

            # d = _Orchestrate()
            # d.update_database(int(transaction_id.id))
            forecast_types = ('ses', 'htces')
            for f_type in forecast_types:
                forecast_type = ForecastType()
                forecast_type.type = f_type
                db.session.add(forecast_type)
            db.session.commit()
            ses_id = db.session.query(ForecastType.id).filter(ForecastType.type == forecast_types[0]).first()
            htces_id = db.session.query(ForecastType.id).filter(ForecastType.type == forecast_types[1]).first()
            current_msk = db.session.query(MasterSkuList.sku_id).all()
            match_sku = [str(i) for i in current_msk]
            print(match_sku)
            print('Calculating Forecasts...[COMPLETED]\n')
            log.log(logging.DEBUG, 'loading database ...\n')
            print('loading database ...\n')

            for item in ia:
                skus_description = [summarised for summarised in analysis_summary.describe_sku(item['sku'])]
                denom = db.session.query(Currency.id).filter(Currency.currency_code == item['currency']).first()
                master_sku = MasterSkuList()
                master_sku.sku_id = item['sku']
                db.session.add(master_sku)
                i_up = InventoryAnalysis()
                mk = db.session.query(MasterSkuList.id).filter(MasterSkuList.sku_id == item['sku']).first()
                i_up.sku_id = mk.id
                tuple_orders = item['orders']
                # print(tuple_orders)
                i_up.abc_xyz_classification = item['ABC_XYZ_Classification']
                i_up.standard_deviation = item['standard_deviation']
                i_up.backlog = item['backlog']
                i_up.safety_stock = item['safety_stock']
                i_up.reorder_level = item['reorder_level']
                i_up.economic_order_quantity = item['economic_order_quantity']
                i_up.demand_variability = item['demand_variability']
                i_up.average_orders = round(float(item['average_orders']))
                i_up.shortages = item['shortages']
                i_up.excess_stock = item['excess_stock']
                i_up.reorder_quantity = item['reorder_quantity']
                i_up.economic_order_variable_cost = item['economic_order_variable_cost']
                i_up.unit_cost = item['unit_cost']
                i_up.revenue = item['revenue']
                i_up.date = date_now
                i_up.safety_stock_rank = skus_description[0]['safety_stock_rank']
                i_up.shortage_rank = skus_description[0]['shortage_rank']
                i_up.excess_cost = skus_description[0]['excess_cost']
                i_up.percentage_contribution_revenue = skus_description[0]['percentage_contribution_revenue']
                i_up.excess_rank = skus_description[0]['excess_rank']
                i_up.retail_price = skus_description[0]['retail_price']
                i_up.gross_profit_margin = skus_description[0]['gross_profit_margin']
                i_up.min_order = skus_description[0]['min_order']
                i_up.safety_stock_cost = skus_description[0]['safety_stock_cost']
                i_up.revenue_rank = skus_description[0]['revenue_rank']
                i_up.markup_percentage = skus_description[0]['markup_percentage']
                i_up.max_order = skus_description[0]['max_order']
                i_up.shortage_cost = skus_description[0]['shortage_cost']
                i_up.quantity_on_hand = item['quantity_on_hand']
                i_up.currency_id = denom.id
                i_up.traffic_light = skus_description[0]['inventory_traffic_light']
                i_up.inventory_turns = skus_description[0]['inventory_turns']
                i_up.transaction_log_id = transaction_id.id
                db.session.add(i_up)
                inva = db.session.query(InventoryAnalysis.id).filter(InventoryAnalysis.sku_id == mk.id).first()
                for i, t in enumerate(tuple_orders['demand'], 1):
                    orders_data = Orders()
                    # print(r)
                    orders_data.order_quantity = t
                    orders_data.rank = i
                    orders_data.analysis_id = inva.id
                    db.session.add(orders_data)
                    # need to select sku id
                if simple_forecast is not None:
                    for i, forecasted_demand in enumerate(simple_forecast, 1):
                        if forecasted_demand == item['sku']:
                            forecast_stats = ForecastStatistics()
                            forecast_stats.analysis_id = inva.id
                            forecast_stats.mape = simple_forecast.get(forecasted_demand)['mape']
                            forecast_stats.forecast_type_id = ses_id.id
                            forecast_stats.slope = simple_forecast.get(forecasted_demand)['statistics']['slope']
                            forecast_stats.p_value = simple_forecast.get(forecasted_demand)['statistics']['pvalue']
                            forecast_stats.test_statistic = simple_forecast.get(forecasted_demand)['statistics'][
                                'test_statistic']
                            forecast_stats.slope_standard_error = simple_forecast.get(forecasted_demand)['statistics'][
                                'slope_standard_error']
                            forecast_stats.intercept = simple_forecast.get(forecasted_demand)['statistics']['intercept']
                            forecast_stats.standard_residuals = simple_forecast.get(forecasted_demand)['statistics'][
                                'std_residuals']
                            forecast_stats.trending = simple_forecast.get(forecasted_demand)['statistics']['trend']
                            forecast_stats.optimal_alpha = simple_forecast.get(forecasted_demand)['optimal_alpha']
                            forecast_stats.optimal_gamma = 0
                            db.session.add(forecast_stats)
                            for p in range(0, len(simple_forecast.get(forecasted_demand)['forecast'])):
                                forecast_data = Forecast()
                                forecast_data.forecast_quantity = simple_forecast.get(forecasted_demand)['forecast'][p]
                                forecast_data.analysis_id = inva.id
                                forecast_data.forecast_type_id = ses_id.id
                                forecast_data.period = p + 1
                                forecast_data.create_date = date_now
                                db.session.add(forecast_data)
                            for q, sesf in enumerate(simple_forecast.get(forecasted_demand)['forecast_breakdown']):
                                forecast_breakdown = ForecastBreakdown()
                                forecast_breakdown.analysis_id = inva.id
                                forecast_breakdown.forecast_type_id = ses_id.id
                                forecast_breakdown.trend = 0
                                forecast_breakdown.period = sesf['t']
                                forecast_breakdown.level_estimates = \
                                    sesf['level_estimates']
                                forecast_breakdown.one_step_forecast = \
                                    sesf['one_step_forecast']
                                forecast_breakdown.forecast_error = \
                                    sesf['forecast_error']
                                forecast_breakdown.squared_error = sesf['squared_error']
                                forecast_breakdown.regression = simple_forecast.get(forecasted_demand)['regression'][q]
                                db.session.add(forecast_breakdown)
                            break

                for i, holts_forecast_demand in enumerate(holts_forecast, 1):
                    if holts_forecast_demand == item['sku']:
                        forecast_stats = ForecastStatistics()
                        forecast_stats.analysis_id = inva.id
                        forecast_stats.mape = holts_forecast.get(holts_forecast_demand)['mape']
                        forecast_stats.forecast_type_id = htces_id.id
                        forecast_stats.slope = holts_forecast.get(holts_forecast_demand)['statistics'].get('slope')
                        forecast_stats.p_value = holts_forecast.get(holts_forecast_demand)['statistics'].get('pvalue')
                        forecast_stats.test_statistic = holts_forecast.get(holts_forecast_demand)['statistics'].get(
                            'test_statistic')
                        forecast_stats.slope_standard_error = holts_forecast.get(holts_forecast_demand)['statistics'].get(
                            'slope_standard_error')
                        forecast_stats.intercept = holts_forecast.get(holts_forecast_demand)['statistics'].get('intercept')
                        forecast_stats.standard_residuals = holts_forecast.get(holts_forecast_demand)['statistics'].get('std_residuals')
                        forecast_stats.trending = holts_forecast.get(holts_forecast_demand)['statistics'].get('trend')
                        forecast_stats.optimal_alpha = holts_forecast.get(holts_forecast_demand)['optimal_alpha']
                        forecast_stats.optimal_gamma = holts_forecast.get(holts_forecast_demand)['optimal_gamma']
                        db.session.add(forecast_stats)
                        for p in range(0, len(holts_forecast.get(holts_forecast_demand)['forecast'])):
                            forecast_data = Forecast()
                            forecast_data.forecast_quantity = holts_forecast.get(holts_forecast_demand)['forecast'][p]
                            forecast_data.analysis_id = inva.id
                            forecast_data.forecast_type_id = htces_id.id
                            forecast_data.period = p + 1
                            forecast_data.create_date = date_now
                            db.session.add(forecast_data)
                        for k, htcesf in enumerate(holts_forecast.get(holts_forecast_demand)['forecast_breakdown']):
                            forecast_breakdown = ForecastBreakdown()
                            forecast_breakdown.analysis_id = inva.id
                            forecast_breakdown.forecast_type_id = htces_id.id
                            forecast_breakdown.trend = htcesf['trend']
                            forecast_breakdown.period = htcesf['t']
                            forecast_breakdown.level_estimates = \
                                htcesf['level_estimates']
                            forecast_breakdown.one_step_forecast = \
                                htcesf['one_step_forecast']
                            forecast_breakdown.forecast_error = \
                                htcesf['forecast_error']
                            forecast_breakdown.squared_error = htcesf['squared_error']
                            forecast_breakdown.regression = holts_forecast.get(holts_forecast_demand)['regression'][k]
                            db.session.add(forecast_breakdown)
                        break

            db.session.commit()
            print('loading database ...[COMPLETED]\n')
            loading = 'Loading recommendations into database...'
            print(loading, end="")
            load_recommendations(summary=ia, forecast=holts_forecast, analysed_order=orders_analysis)
            print('Loading recommendations into database...[COMPLETED]\n')
            log.log(logging.DEBUG, 'Analysis ...\n')
            print('Analysis ... [COMPLETED]\n')
    except OSError as e:
        print(e)


def load_recommendations(summary, forecast, analysed_order):
    recommend = run_sku_recommendation(analysed_orders=analysed_order, forecast=forecast)
    for item in summary:
        rec = Recommendations()
        mk = db.session.query(MasterSkuList.id).filter(MasterSkuList.sku_id == item['sku']).first()
        inva = db.session.query(InventoryAnalysis.id).filter(InventoryAnalysis.sku_id == mk.id).first()
        rec.analysis_id = inva.id
        reco = 'There are no recommendation at this time.' if recommend.get(item['sku'],
                                                                            'There are no recommendation at this time.'
                                                                            ) == '' else recommend.get(item['sku'],
                                                                                                       'None')
        rec.statement = reco
        db.session.add(rec)
        db.session.commit()


def load_profile_recommendations(analysed_order, forecast, transaction_log_id):
    recommend = run_profile_recommendation(analysed_orders=analysed_order, forecast=forecast)
    rec = ProfileRecommendation()
    rec.transaction_id = int(transaction_log_id.id)
    rec.statement = recommend.get('profile')
    db.session.add(rec)
    db.session.commit()


if __name__ == '__main__':
    load(ABS_FILE_PATH['COMPLETE_CSV_SM'])
