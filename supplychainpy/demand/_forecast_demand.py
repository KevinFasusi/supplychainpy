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

import numpy as np
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Forecast:
    """

    """
    __simple_exponential_smoothing_forecast = {}

    # make keyword args
    def __init__(self, orders: list = None, average_orders: float = None, **kwargs):
        self.__weighted_moving_average = None
        self.__orders = orders
        self.__average_orders = sum([int(demand) for demand in self.__orders]) / len(self.__orders)
        self.__moving_average = []
        self.__total_orders = sum([int(demand) for demand in self.__orders])

    @property
    def total_orders(self):
        return self.__total_orders

    @property
    def moving_average(self) -> list:
        return self.__moving_average

    @moving_average.setter
    def moving_average(self, forecast: list):
        self.__moving_average = forecast

    @property
    def weighted_moving_average(self) -> list:
        return self.__weighted_moving_average

    # specify a start position and the forecast will build from this position
    def moving_average_forecast(self, average_period: int = 3, forecast_length: int = 2,
                                base_forecast: bool = False, start_position: int = 0) -> list:
        """ Generates a forecast from moving averages.

        Generate a forecast from moving averages for as many periods as specified.

        Args:
            average_period (int):       Number of periods to average.
            forecast_length (int):      Number of periods to forecast for.
            base_forecast (bool):       Start a moving average forecast from anywhere
                                        in the list. For use when evaluating a forecast.
            start_position (int):       Where to start the forecast in the list when

        Returns:
            list:       Returns a list of orders including the original and the forecast appended to the end.
                        The appended forecast is as long as specified by the forecast_length. For example

                        orders = [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20]
                        d = forecast_demand.Forecast(orders)
                        d.calculate_moving_average_forecast(forecast_length=3)
                        print(d.moving_average_forecast)

                            output:

                                [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20, 26, 27, 24]

                        orders = [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20]
                        d = forecast_demand.Forecast(orders)
                        d.calculate_moving_average_forecast(forecast_length=3, base_forecast=True, start_position=3)
                        print(d.moving_average_forecast):

                            output:

                                [3, 67, 65, 45, 60, 80]

        Raises:
            ValueError: Incorrect number of orders supplied. Please make sure you have enough orders to
                        calculate an average. The average_period is {}, while the
                        number of orders supplied is {}. The number of orders supplied should be equal
                        or greater than the average_period. Either decrease the average_period or
                        increase the start_position in the list.n
        """

        if base_forecast:
            start_period = start_position + average_period
            end_period = len(self.__orders)
            total_orders = 0
            moving_average = []
            if len(self.__orders[0:start_position]) < average_period:
                raise ValueError("Incorrect number of orders supplied. Please make sure you have enough orders to "
                                 "calculate an average. The average_period is {}, while the \n"
                                 "number of orders supplied is {}. The number of orders supplied should  be equal "
                                 "or greater than the average_period.\n Either decrease the average_period or "
                                 "increase the start_position in the list.".format(average_period, start_position))
            else:
                for i in self.__orders[0:start_position]:
                    moving_average.append(self.__orders[i])

            count = 0
            average_orders = 0.0
            while count < forecast_length:
                for items in moving_average[0:end_period]:
                    total_orders += items
                count += 1
                average_orders = total_orders / float(average_period)
                moving_average.append(round(average_orders))
                average_orders = 0.0
                total_orders = 0.0
                if count < 1:
                    start_period += len(moving_average) - average_period
                else:
                    start_period += 1

                end_period = len(moving_average)
            self.__moving_average = moving_average

        else:
            start_period = len(self.__orders) - average_period
            end_period = len(self.__orders)
            total_orders = 0
            moving_average = self.__orders
            count = 0
            average_orders = 0.0
            while count < forecast_length:
                for items in moving_average[start_period:end_period]:
                    total_orders += items
                count += 1
                average_orders = total_orders / float(average_period)
                moving_average.append(round(average_orders))
                average_orders = 0.0
                total_orders = 0.0
                if count < 1:
                    start_period += len(moving_average) - average_period
                else:
                    start_period += 1

                end_period = len(moving_average)
                self.__moving_average = moving_average
            return moving_average

    def weighted_moving_average_forecast(self, weights: list, average_period: int = 3,
                                         forecast_length: int = 3, base_forecast: bool = False,
                                         start_position=0) -> list:
        """ Generates a forecast from moving averages using user supplied weights.

        Generate a forecast from moving averages for as many periods as specified and adjusts the forecast based
        on the supplied weights.

        Args:
            average_period (int):       Number of periods to average.
            forecast_length (int):      Number of periods to forecast for.
            weights (list):             A list of weights that sum up to one.
            base_forecast(bool):        Start a moving average forecast from anywhere
                                        in the list. For use when evaluating a forecast.
            start_position(int):        Start position

        Returns:
            list:       Returns a list of orders including the original and the forecast appended to the end.
                        The appended forecast is as long as specified by the forecast_length. For example

                        orders = [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20]
                        d = forecast_demand.Forecast(orders)
                        d.calculate_moving_average_forecast(forecast_length=3)
                        print(d.moving_average_forecast)

                            output:

                                [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20, 13, 11, 7]

        Raises:
            ValueError: The weights should equal 1 and be as long as the average period (default 3).'
                        The supplied weights total {} and is {} members long. Please check the supplied
                        weights.'.format(sum(weights), len(weights)))
        """

        if sum(weights) != 1 or len(weights) != average_period:
            raise ValueError(
                'The weights should equal 1 and be as long as the average period (default 3).'
                ' The supplied weights total {} and is {} members long. Please check the supplied weights.'.format(
                    sum(weights), len(weights)))
        else:
            start_period = len(self.__orders) - average_period

        if base_forecast:
            start_period = start_position + average_period
            end_period = len(self.__orders)
            total_orders = 0
            weighted_moving_average = []
            if start_position + 1 < average_period:
                raise ValueError("Incorrect number of orders supplied. Please make sure you have enough orders to "
                                 "calculate an average. The average_period is {}, while the \n"
                                 "number of orders supplied is {}. The number of orders supplied should  be equal "
                                 "or greater than the average_period.\n Either decrease the average_period or "
                                 "increase the start_position in the list.".format(average_period, start_position))
            else:
                for i in self.__orders[0:start_position]:
                    weighted_moving_average.append(self.__orders[i])

            count = 0
            weight_count = 0
            while count < forecast_length:
                for items in weighted_moving_average[0:end_period]:
                    total_orders += items

                count += 1
                average_orders = (total_orders / float(average_period)) * weights[weight_count]
                weighted_moving_average.append(round(average_orders))
                total_orders = 0.0
                if count < 1:
                    start_period += len(weighted_moving_average) - average_period
                else:
                    start_period += 1
            self.__weighted_moving_average = weighted_moving_average
        else:
            end_period = len(self.__orders)
            total_orders = 0
            weighted_moving_average = self.__orders
            count = 0
            average_orders = 0.0
            while count < forecast_length:
                weight_count = 0
                for items in weighted_moving_average[start_period:end_period]:
                    total_orders += items
                average_orders = (total_orders / float(average_period)) * weights[weight_count]
                count += 1
                weighted_moving_average.append(round(average_orders))
                average_orders = 0.0
                total_orders = 0.0
                if count < 1:
                    start_period += len(weighted_moving_average) - average_period
                else:
                    start_period += 1

                end_period = len(weighted_moving_average)

        self.__weighted_moving_average = weighted_moving_average
        return weighted_moving_average

    # also use to calculate the MAD for all forecasting methods given a spcific length of order

    # TODO-feature fix base_forecast for correct period to period MAD calculation
    def mean_absolute_deviation(self, forecasts: list, base_forecast: bool = False, start_period: int = 3) -> np.array:

        """ calculates the mean absolute deviation (MAD) for a given forecast.

        Calculates the mean absolute deviation for a forecast. The forecast and

        Args:
            forecasts (list):       A previously calculated forecast.
            base_forecast (bool):   Start a moving average forecast from anywhere
                                    in the list.
            start_period (int):     The start period of the forecast.

        Returns:
            np.array

        Raises:
            ValueError:
        """

        if base_forecast:
            end_period = len(forecasts) - start_period
            forecast_array = np.array(forecasts[:end_period])
            orders_array = np.array(self.__orders[start_period: len(forecasts)])
            std_array = orders_array - forecast_array
            std_array = sum(abs(std_array)) / len(std_array)
        else:
            forecast_array = np.array(forecasts)
            orders_array = np.array(self.__orders)
            std_array = orders_array - forecast_array
            std_array = sum(abs(std_array)) / len(std_array)

        return std_array

    def simple_exponential_smoothing(self, *alpha) -> dict:
        """ Generates forecast using simple exponential smoothing (SES).

        Args:
            alpha(args):    A list of smoothing level constants (alpha values)

        Returns:
            dict:           Forecast containing
                            {'demand': 165, 'level_estimates': 164.49748124123246, 'alpha': 0.7487406206162335,
                            'one_step_forecast': 163.0, 'forecast_error': 2.0, 'squared_error': 4.0, 't': 1}
         Examples:
                            forecast_demand = Forecast(orders)
                            alpha_values = [0.2, 0.3, 0.4, 0.5, 0.6]
                            ses_forecast = [forecast for forecast in forecast_demand.simple_exponential_smoothing(*alpha_values)]

       """

        for arg in alpha:
            forecast = {}

            current_level_estimate = self.__average_orders
            forecast.update({'alpha': arg,
                             't': 0,
                             'demand': 0,
                             'level_estimates': current_level_estimate,
                             'one_step_forecast': 0,
                             'forecast_error': 0,
                             'squared_error': 0})
            previous_level_estimate = current_level_estimate
            for index, demand in enumerate(tuple(self.__orders), 1):
                current_level_estimate = self._level_estimate(previous_level_estimate, arg, demand)
                yield {'alpha': arg,
                       't': index,
                       'demand': demand,
                       'level_estimates': current_level_estimate,
                       'one_step_forecast': previous_level_estimate,
                       'forecast_error': self._forecast_error(demand, previous_level_estimate),
                       'squared_error': self._forecast_error(demand, previous_level_estimate) ** 2
                       }
                previous_level_estimate = current_level_estimate

    def holts_trend_corrected_exponential_smoothing(self, alpha: float, gamma: float, intercept: float, slope: float):
        forecast = {}
        #log.debug('holts ')
        current_level_estimate = intercept
        forecast.update({'alpha': alpha,
                         'gamma': gamma,
                         't': 0,
                         'demand': 0,
                         'level_estimates': current_level_estimate,
                         'trend': slope,
                         'one_step_forecast': 0,
                         'forecast_error': 0,
                         'squared_error': 0

                         })
        previous_trend = slope
        previous_level_estimate = current_level_estimate
        for index, demand in enumerate(tuple(self.__orders), 1):
            #log.debug('demand: {}'.format(demand))
            one_step = previous_level_estimate + previous_trend
            #log.debug('one_step: {}'.format(one_step))
            forecast_error = self._forecast_error(demand, one_step)
            #log.debug('forecast_error: {}'.format(forecast_error))
            current_trend = self._holts_trend(previous_trend, gamma, alpha, forecast_error)
            #log.debug('trend: {}'.format(current_trend))
            current_level_estimate = self._level_estimate_holts_trend_corrected(previous_level_estimate,
                                                                                alpha,
                                                                                previous_trend,
                                                                                forecast_error)
            #log.debug('current_level: {}'.format(current_level_estimate))
            squared_error = forecast_error ** 2
            yield {'alpha': alpha,
                   'gamma': gamma,
                   't': index,
                   'demand': demand,
                   'trend': current_trend,
                   'level_estimates': current_level_estimate,
                   'one_step_forecast': one_step,
                   'forecast_error': forecast_error,
                   'squared_error': squared_error
                   }
            #log.debug('squared_error: {}'.format(squared_error))
            previous_level_estimate = current_level_estimate
            previous_trend = current_trend

    @staticmethod
    def holts_trend_corrected_forecast(forecast: list, forecast_length: int):
        """Creates a forecast for as many periods.

        Args:
            forecast:
            forecast_length:

        Returns:

        """
        end_of_forecast = len(forecast) - 1
        # print(forecast[end_of_forecast])

        new_forecast = []

        for i in range(forecast_length):
            demand_forecast = forecast[end_of_forecast]['level_estimates'] + i * forecast[end_of_forecast]['trend']
            new_forecast.append(demand_forecast)
        return new_forecast

    @staticmethod
    def simple_exponential_smoothing_forecast(forecast: list, forecast_length: int):
        end_of_forecast = len(forecast) - 1
        new_forecast = []

        for i in range(forecast_length):
            demand_forecast = forecast[end_of_forecast]['level_estimates']
            new_forecast.append(demand_forecast)
        return new_forecast

    @staticmethod
    def _holts_trend(previous_trend: float, gamma: float, alpha: float, current_forecast_error: float):
        return previous_trend + alpha * gamma * current_forecast_error

    @staticmethod
    def _level_estimate(lvl: float, smoothing_parameter: float, demand: int):
        return lvl + smoothing_parameter * (demand - lvl)

    @staticmethod
    def _level_estimate_holts_trend_corrected(previous_level: float, smoothing_parameter: float, previous_trend: float,
                                              forecast_error: float):
        return previous_level + previous_trend + smoothing_parameter * forecast_error

    @staticmethod
    def _forecast_error(demand: int, one_step_forecast: float):
        return float(demand) - one_step_forecast

    @staticmethod
    def sum_squared_errors(squared_error: list, smoothing_parameter: float) -> dict:
        sse = 0
        for sq_e in squared_error:
            if sq_e['alpha'] == smoothing_parameter:
                sse += sq_e["squared_error"]

        return {smoothing_parameter: sse}

    @staticmethod
    def sum_squared_errors_indi(squared_error: list, smoothing_parameter: float) -> dict:
        sse = 0

        for sq_e in squared_error:
            #sse += sum([i["squared_error"] for i in sq_e if i['alpha'] == smoothing_parameter])
            for i in sq_e:
                if i['alpha'] == smoothing_parameter:
                    sse += i["squared_error"]

        return {smoothing_parameter: sse}

    @staticmethod
    def sum_squared_errors_indi_htces(squared_error: list, alpha: float, gamma: float) -> dict:
        sse = 0

        for sq_e in squared_error:
            for i in sq_e:
                if i['alpha'] == alpha and i['gamma'] == gamma:
                    sse += i["squared_error"]

        return {(alpha, gamma): sse}

    @staticmethod
    def standard_error(sse: dict, orders_count, smoothing_parameter, df: int = 1) -> float:
        return (sse[smoothing_parameter] / (orders_count - df)) ** 0.5

    def mean_forecast_error(self):

        """

        Args:
            forecasts (int):        Number of periods to average.
            base_forecast (bool):   A list of weights that sum up to one.


        Returns:
            np.array

        Raises:
            ValueError:
        """

        pass

    def mean_aboslute_percentage_error_opt(self, forecast: list) -> list:
        sum_ape = sum([abs((i['demand'] - i['level_estimates']) / i['demand']) for i in forecast])
        mape = (sum_ape / len(forecast)) * 100
        return mape

    def optimise(self):

        """

        Args:
            forecasts (int):        Number of periods to average.
            base_forecast (bool):   A list of weights that sum up to one.


        Returns:
            np.array

        Raises:
            ValueError:
        """
        pass

    def linear_regression(self):

        """

        Args:
            line (int):        Number of periods to average.
            base_forecast (bool):   A list of weights that sum up to one.


        Returns:
            np.array

        Raises:
            ValueError:
        """
        pass

    def autoregressive(self):
        """

        Args:
            forecasts (int):        Number of periods to average.
            base_forecast (bool):   A list of weights that sum up to one.


        Returns:
            np.array

        Raises:
            ValueError:
        """
        pass


if __name__ == '__main__':
    orders = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147, 188, 161, 162, 169, 185,
              188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218, 264, 304]

    total_orders = 0
    avg_orders = 0
    for order in orders[:12]:
        total_orders += order

    avg_orders = total_orders / 12
    f = Forecast(orders, avg_orders)
    alpha = [0.2, 0.3, 0.4, 0.5, 0.6]
    s = [i for i in f.simple_exponential_smoothing(*alpha)]

    sum_squared_error = f.sum_squared_errors(s, 0.5)
    #print(sum_squared_error)

    standard_error = f.standard_error(sum_squared_error, len(orders), smoothing_parameter=0.5)
    #print(standard_error)
