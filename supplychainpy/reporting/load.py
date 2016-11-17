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

import datetime
import logging
import os

from decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy._csv_management._csv_manager import _Orchestrate
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import deserialise_config
from supplychainpy.bi.recommendation_generator import run_sku_recommendation, run_profile_recommendation
from supplychainpy.inventory.summarise import Inventory
from supplychainpy.reporting.views import TransactionLog, Recommendations, ProfileRecommendation
from supplychainpy.reporting.views import Forecast
from supplychainpy.reporting.views import ForecastType
from supplychainpy.reporting.views import ForecastStatistics
from supplychainpy.reporting.views import ForecastBreakdown
from supplychainpy.reporting.views import InventoryAnalysis
from supplychainpy.reporting.views import MasterSkuList
from supplychainpy.reporting.views import Currency
from supplychainpy.reporting.views import Orders
from supplychainpy.launch_reports import db, app
from supplychainpy.sample_data.config import ABS_FILE_PATH

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def currency_codes():
    codes = {"AED": ("United Arab Emirates Dirham", "&#92;&#117;&#48;&#54;&#50;&#102;&#46;"),
             "ANG": ("Netherlands Antilles Guilder","&#402"),
             "EUR": ("Euro Member Countries", "&#8364;"),
             "GBP": ("United Kingdom Pound", "&#163;"),
             "USD": ("United States Dollar", "&#36;"),
             }
    return codes


def load(file_path: str, location: str = None):
    if location is not None and os.name in ['posix', 'mac']:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/reporting.db'.format(location)

    elif location is not None and os.name == 'nt':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\reporting.db'.format(location)

    log.log(logging.DEBUG, 'Loading data analysis for reporting suite... \n')

    db.create_all()

    log.log(logging.DEBUG, 'loading currency symbols...\n')
    print('loading currency symbols...', end="")
    fx = currency_codes()
    for key, value in fx.items():
        codes = Currency()
        codes.country = value[0]
        codes.symbol = value[1]
        codes.currency_code = key
        db.session.add(codes)
    db.session.commit()
    print('[COMPLETED]\n')
    config = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
    currency = config.get('currency')

    log.log(logging.DEBUG, 'Analysing file: {}...\n'.format(file_path))
    print('Analysing file: {}...'.format(file_path), end="")
    orders_analysis = model_inventory.analyse(file_path=file_path,
                                              z_value=Decimal(1.28),
                                              reorder_cost=Decimal(5000),
                                              file_type="csv", length=12,currency=currency)

    # remove assumption file type is csv

    ia = [analysis.orders_summary() for analysis in
          model_inventory.analyse(file_path=file_path, z_value=Decimal(1.28),
                                  reorder_cost=Decimal(5000), file_type="csv", length=12, currency=currency)]
    date_now = datetime.datetime.now()
    analysis_summary = Inventory(processed_orders=orders_analysis)
    print('[COMPLETED]\n')

    log.log(logging.DEBUG, 'Calculating Forecasts...\n')
    print('Calculating Forecasts...', end="")
    simple_forecast = {analysis.sku_id: analysis.simple_exponential_smoothing_forecast for analysis in
                       model_inventory.analyse(file_path=file_path, z_value=Decimal(1.28),
                                               reorder_cost=Decimal(5000), file_type="csv",
                                               length=12, currency=currency)}
    holts_forecast = {analysis.sku_id: analysis.holts_trend_corrected_forecast for analysis in
                      model_inventory.analyse(file_path=file_path, z_value=Decimal(1.28),
                                              reorder_cost=Decimal(5000), file_type="csv",
                                              length=12,currency=currency)}

    transact = TransactionLog()
    transact.date = date_now
    db.session.add(transact)
    db.session.commit()

    transaction_sub = db.session.query(db.func.max(TransactionLog.date))
    transaction_id = db.session.query(TransactionLog).filter(TransactionLog.date == transaction_sub).first()

    # loads inventory profile recommendations
    load_profile_recommendations(analysed_order=orders_analysis, forecast=holts_forecast,
                                 transaction_log_id=transaction_id)

    #d = _Orchestrate()
    #d.update_database(int(transaction_id.id))

    forecast_types = ('ses', 'htces')

    for f_type in forecast_types:
        forecast_type = ForecastType()
        forecast_type.type = f_type
        db.session.add(forecast_type)
    db.session.commit()
    ses_id = db.session.query(ForecastType.id).filter(ForecastType.type == forecast_types[0]).first()
    htces_id = db.session.query(ForecastType.id).filter(ForecastType.type == forecast_types[1]).first()
    print('[COMPLETED]\n')
    log.log(logging.DEBUG, 'loading database ...\n')
    print('loading database ...', end="")

    for item in ia:
        re = 0
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
        for i, forecasted_demand in enumerate(simple_forecast, 1):
            if forecasted_demand == item['sku']:
                forecast_stats = ForecastStatistics()
                forecast_stats.analysis_id = inva.id
                forecast_stats.mape = simple_forecast.get(forecasted_demand)['mape']
                forecast_stats.forecast_type_id = ses_id.id
                forecast_stats.slope = simple_forecast.get(forecasted_demand)['statistics']['slope']
                forecast_stats.p_value = simple_forecast.get(forecasted_demand)['statistics']['pvalue']
                forecast_stats.test_statistic = simple_forecast.get(forecasted_demand)['statistics']['test_statistic']
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
                forecast_stats.slope = holts_forecast.get(holts_forecast_demand)['statistics']['slope']
                forecast_stats.p_value = holts_forecast.get(holts_forecast_demand)['statistics']['pvalue']
                forecast_stats.test_statistic = holts_forecast.get(holts_forecast_demand)['statistics'][
                    'test_statistic']
                forecast_stats.slope_standard_error = holts_forecast.get(holts_forecast_demand)['statistics'][
                    'slope_standard_error']
                forecast_stats.intercept = holts_forecast.get(holts_forecast_demand)['statistics']['intercept']
                forecast_stats.standard_residuals = holts_forecast.get(holts_forecast_demand)['statistics'][
                    'std_residuals']
                forecast_stats.trending = holts_forecast.get(holts_forecast_demand)['statistics']['trend']
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
                for i, htcesf in enumerate(holts_forecast.get(holts_forecast_demand)['forecast_breakdown']):
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
                    forecast_breakdown.regression = holts_forecast.get(holts_forecast_demand)['regression'][i]
                    db.session.add(forecast_breakdown)
                break

    db.session.commit()
    print('[COMPLETED]\n')
    loading = 'Loading recommendations into database... '
    print(loading, end="")
    load_recommendations(summary=ia, forecast=holts_forecast, analysed_order=orders_analysis)
    print('[COMPLETED]\n')
    log.log(logging.DEBUG, "Analysis ...\n")
    print("Analysis ... [COMPLETED]")


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
    load(ABS_FILE_PATH['COMPLETE_CSV_XSM'])
