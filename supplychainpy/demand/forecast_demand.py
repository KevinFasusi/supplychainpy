import numpy as np
from decimal import Decimal, localcontext


class Forecast:
    def __init__(self, orders: list):
        self.__weighted_moving_average = None
        self.__orders = orders
        self.__moving_average = []

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

    def simple_exponential_smoothing(self, forecasts: list) -> list:
        pass

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

    def mean_aboslute_percentage_error(self, **forecasts) -> list:

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

    # select which algorithm to use list available algorithms in the documentations
    def genetic_algorithm(self):

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
