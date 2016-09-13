# Copyright (c) 2015-2016, Kevin Fasusi
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

from supplychainpy import data_cleansing
from supplychainpy.data_cleansing import check_extension
from supplychainpy.demand.evolutionary_algorithms import OptimiseSmoothingLevelGeneticAlgorithm
from supplychainpy.demand.forecast_demand import Forecast
from supplychainpy.demand.regression import LinearRegression
from supplychainpy._helpers._enum_formats import FileFormats


def simple_exponential_smoothing_forecast(demand: list, smoothing_level_constant: float, forecast_length: int = 5,
                                          initial_estimate_period: int = 6,
                                          **kwargs) -> dict:
    """

    Args:
        forecast_length:
        demand:
        smoothing_level_constant:
        initial_estimate_period:
        **kwargs:

    Returns:

    """
    orders = [int(i) for i in demand]
    forecast_demand = Forecast(orders)

    # optimise, population_size, genome_length, mutation_probability, recombination_types
    if len(kwargs) != 0:
        if kwargs['optimise']:

            ses_forecast = [i for i in forecast_demand.simple_exponential_smoothing(*(smoothing_level_constant,))]

            sum_squared_error = forecast_demand.sum_squared_errors(ses_forecast, smoothing_level_constant)

            standard_error = forecast_demand.standard_error(sum_squared_error, len(orders), smoothing_level_constant)
            total_orders = 0

            for order in orders[:initial_estimate_period]:
                total_orders += order

            avg_orders = total_orders / initial_estimate_period

            evo_mod = OptimiseSmoothingLevelGeneticAlgorithm(orders=orders,
                                                             average_order=avg_orders,
                                                             smoothing_level=smoothing_level_constant,
                                                             population_size=10,
                                                             standard_error=standard_error,
                                                             recombination_type='single_point')

            ses_evo_forecast = evo_mod.simple_exponential_smoothing_evo(
                smoothing_level_constant=smoothing_level_constant,
                initial_estimate_period=initial_estimate_period)

            return ses_evo_forecast
    else:

        forecast_breakdown = [i for i in forecast_demand.simple_exponential_smoothing(smoothing_level_constant)]
        ape = LinearRegression(forecast_breakdown)
        mape = forecast_demand.mean_aboslute_percentage_error_opt(forecast_breakdown)
        stats = ape.least_squared_error()
        simple_forecast = forecast_demand.simple_exponential_smoothing_forecast(forecast=forecast_breakdown,
                                                                                forecast_length=forecast_length)

        return {'forecast_breakdown': forecast_breakdown, 'mape': mape, 'statistics': stats,
                'forecast': simple_forecast, 'alpha': smoothing_level_constant}


def simple_exponential_smoothing_forecast_from_file(file_path: str, file_type: str, length: int,
                                                    smoothing_level_constant: float, forecast_length=5,
                                                    **kwargs) -> dict:
    item_list = {}

    if check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            f = open(file_path, 'r')
            item_list = (data_cleansing.clean_orders_data_row(f, length))
        elif file_type == FileFormats.csv.name:
            f = open(file_path)
            item_list = data_cleansing.clean_orders_data_row_csv(f, length=length)
    else:
        incorrect_file = "Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter."
        raise Exception(incorrect_file)

    for sku in item_list:

        sku_id, unit_cost, lead_time, retail_price, quantity_on_hand = sku.get("sku id"), sku.get("unit cost"), sku.get(
            "lead time"), sku.get("retail_price"), sku.get("quantity_on_hand")

        orders = [int(i) for i in sku.get("demand")]

        if kwargs['optimise']:
            yield {sku_id: simple_exponential_smoothing_forecast(demand=orders,
                                                                 forecast_length=forecast_length,
                                                                 smoothing_level_constant=smoothing_level_constant,
                                                                 optimise=True)}

        else:
            yield {sku_id: simple_exponential_smoothing_forecast(demand=orders,
                                                                 forecast_length=forecast_length,
                                                                 smoothing_level_constant=smoothing_level_constant)}


def holts_trend_corrected_exponential_smoothing_forecast(demand: list, alpha: float, gamma: float,
                                                         forecast_length: int = 4, initial_period: int = 6, **kwargs):
    if len(kwargs) != 0:
        if kwargs['optimise']:

            total_orders = 0

            for order in demand[:initial_period]:
                total_orders += order

            avg_orders = total_orders / initial_period
            forecast_demand = Forecast(demand)

            processed_demand = [{'t': index, 'demand': order} for index, order in enumerate(demand, 1)]
            stats = LinearRegression(processed_demand)

            log_stats = stats.least_squared_error(slice_end=6)

            htces_forecast = [i for i in
                              forecast_demand.holts_trend_corrected_exponential_smoothing(alpha=alpha, gamma=gamma,
                                                                                          intercept=log_stats.get(
                                                                                              'intercept'),
                                                                                          slope=log_stats.get(
                                                                                              'slope'))]

            sum_squared_error = forecast_demand.sum_squared_errors_indi_htces(squared_error=[htces_forecast],
                                                                              alpha=alpha, gamma=gamma)

            standard_error = forecast_demand.standard_error(sum_squared_error, len(demand), (alpha, gamma), 2)

            evo_mod = OptimiseSmoothingLevelGeneticAlgorithm(orders=demand,
                                                             average_order=avg_orders,
                                                             population_size=10,
                                                             standard_error=standard_error,
                                                             recombination_type='single_point')

            optimal_alpha = evo_mod.initial_population(individual_type='htces')
            # print(optimal_alpha[1][0], optimal_alpha[1][1])
            htces_forecast = [i for i in
                              forecast_demand.holts_trend_corrected_exponential_smoothing(alpha=optimal_alpha[1][0],
                                                                                          gamma=optimal_alpha[1][1],
                                                                                          intercept=log_stats.get(
                                                                                              'intercept'),
                                                                                          slope=log_stats.get(
                                                                                              'slope'))]

            holts_forecast = forecast_demand.holts_trend_corrected_forecast(forecast=htces_forecast,
                                                                            forecast_length=forecast_length)

            ape = LinearRegression(htces_forecast)
            mape = forecast_demand.mean_aboslute_percentage_error_opt(htces_forecast)
            stats = ape.least_squared_error()

            return {'forecast_breakdown': htces_forecast,'forecast': holts_forecast, 'mape': mape, 'statistics': stats, 'optimal_alpha': optimal_alpha[1][0],
                    'optimal_gamma': optimal_alpha[1][1]}

    else:

        forecast_demand = Forecast(demand)
        processed_demand = [{'t': index, 'demand': order} for index, order in enumerate(demand, 1)]
        stats = LinearRegression(processed_demand)

        log_stats = stats.least_squared_error(slice_end=6)

        htces_forecast = [i for i in
                          forecast_demand.holts_trend_corrected_exponential_smoothing(alpha=alpha, gamma=gamma,
                                                                                      intercept=log_stats.get(
                                                                                          'intercept'),
                                                                                      slope=log_stats.get(
                                                                                          'slope'))]

        holts_forecast = forecast_demand.holts_trend_corrected_forecast(forecast=htces_forecast,
                                                                        forecast_length=forecast_length)

        sum_squared_error = forecast_demand.sum_squared_errors_indi_htces(squared_error=[htces_forecast],
                                                                          alpha=alpha, gamma=gamma)

        ape = LinearRegression(htces_forecast)
        mape = forecast_demand.mean_aboslute_percentage_error_opt(htces_forecast)
        stats = ape.least_squared_error()

        return {'forecast_breakdown': htces_forecast,
                'forecast': holts_forecast,
                'mape': mape,
                'statistics': stats,
                'sum_squared_errors': sum_squared_error}


def holts_trend_corrected_exponential_smoothing_forecast_from_file(file_path: str, file_type: str, length: int,
                                                                   alpha: float, gamma: float, **kwargs):
    item_list = {}
    if check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            f = open(file_path, 'r')
            item_list = (data_cleansing.clean_orders_data_row(f, length))
        elif file_type == FileFormats.csv.name:
            f = open(file_path)
            item_list = data_cleansing.clean_orders_data_row_csv(f, length=length)
    else:
        incorrect_file = "Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter."
        raise Exception(incorrect_file)

    for sku in item_list:
        sku_id, unit_cost, lead_time, retail_price, quantity_on_hand = sku.get("sku id"), sku.get("unit cost"), sku.get(
            "lead time"), sku.get("retail_price"), sku.get("quantity_on_hand")

        orders = [int(i) for i in sku.get("demand")]

        if kwargs['optimise']:
            yield {sku_id: holts_trend_corrected_exponential_smoothing_forecast(demand=orders, alpha=alpha, gamma=gamma,
                                                                                forecast_length=4, initial_period=18,
                                                                                optimise=True)}

        else:
            yield {sku_id: holts_trend_corrected_exponential_smoothing_forecast(demand=orders, alpha=alpha, gamma=gamma,
                                                                                forecast_length=4, initial_period=18,
                                                                                optimise=True)}
