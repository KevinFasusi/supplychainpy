import numpy as np


class Forecast:
    def __init__(self, orders: list):
        self.__orders = orders
        self.__moving_average_forecast = []

    @property
    def moving_average_forecast(self, forecast: list):
        self.__moving_average_forecast = forecast

    @moving_average_forecast.getter
    def moving_average_forecast(self) -> list:
        return self.__moving_average_forecast

    # specify a start position and the forecast will build from this position
    def calculate_moving_average_forecast(self, average_period: int = 3, forecast_length: int = 2,
                                          base_forecast: bool = False, start_position: int = 0) -> list:

        """ Generates a forecast from moving averages.

        Generate a forecast from moving averages for as many periods as specified.

        Args:
            average_period (int):       Number of periods to average.
            forecast_length (int):      Number of periods to forecast for.
            base_forecast (bool):       Start a moving average forecast from anywhere in the list. For use when
                                        evaluating a forecast.
            start_position (int):       Where to start the forecast in the list when 
            reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                    of purchase orders placed in the previous period.
            z_value (Decimal):      The service level required to calculate the safety stock
            file_type (str):       Type of 'file csv' or 'text'
            period (str):          The period of time the data points are bucketed into.

        Returns:
            dict:       The summary of the analysis, containing:
                        average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                        reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                        and ABC_XYZ_Classification. For example:

                        {'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                        'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                        'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                        'standard_deviation': '28', 'safety_stock': '51'}
        Raises:
            Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
            Exception:


        """

        if base_forecast:
            start_period = start_position + average_period
            end_period = len(self.__orders)
            total_orders = 0
            moving_average = []
            if len(self.__orders[0:start_position]) < average_period:
                raise ValueError("Incorrect number of orders supplied. Please make sure you have enough orders to "
                                 "calculate an average. The average_period is {}, while the \n"
                                 "number of orders supplied is {}. The number of orders supplied should be equal "
                                 "or greater than the average_period.\n Either decrease the average_period or "
                                 "increase the start_postion in the list.".format(average_period, start_position))
            else:
                for i in self.__orders[0:start_position]:
                    moving_average.append(self.__orders[i])
                    # in the base_forecast the length of the forecast is the same as the length of the initial run of demand
                    # retrieved from the demand list to the moving_average list

            count = 0
            average_orders = 0.0
            while count < forecast_length:
                for items in moving_average[0:end_period]:
                    total_orders += items
                count += 1
                average_orders = total_orders / float(average_period)
                moving_average.append(average_orders)
                average_orders = 0.0
                total_orders = 0.0
                if count < 1:
                    start_period += len(moving_average) - average_period
                else:
                    start_period += 1

                end_period = len(moving_average)
                self.__moving_average_forecast = moving_average

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
                moving_average.append(average_orders)
                average_orders = 0.0
                total_orders = 0.0
                if count < 1:
                    start_period += len(moving_average) - average_period
                else:
                    start_period += 1

                end_period = len(moving_average)
                self.__moving_average_forecast = moving_average
            return moving_average



    # make sure the number of weights matches the average period if not error
    def calculate_weighted_moving_average_forecast(self, weights: list, average_period: int = 3,
                                                   forecast_length: int = 3) -> list:

            if sum(weights) != 1 or len(weights) != average_period:
                raise Exception(
                    'The weights should equal 1 and be as long as the average period (default 3).'
                    ' The supplied weights total {} and is {} members long. Please check the supplied weights.'.format(
                        sum(weights), len(weights)))
            else:
                start_period = len(self.__orders) - average_period
            end_period = len(self.__orders)
            total_orders = 0
            moving_average = self.__orders
            count = 0
            average_orders = 0.0
            weight_count = 0
            while count < forecast_length:
                weight_count = 0
                for items in moving_average[start_period:end_period]:
                    total_orders += items
                average_orders = (total_orders / float(average_period)) * weights[weight_count]
                count += 1
                moving_average.append(average_orders)
                average_orders = 0.0
                total_orders = 0.0
                if count < 1:
                    start_period += len(moving_average) - average_period
                else:
                    start_period += 1

                end_period = len(moving_average)
            return moving_average


    def calculate_simple_exponential_smoothed_forecast(self, forecasts: list) -> list:
        pass

    # also use to calculate the MAD for all forecasting methods given a spcific length of order

    def calculate_mean_absolute_deviation(self, forecasts: list, orders: list, base_forecast: bool = False) -> np.array:
        if base_forecast:
            forecast_array = np.array(forecasts)
            orders_array = np.array(self.__orders[0: len(forecasts)])
            print(orders_array)
            print(forecast_array)
            std_array = orders_array - forecast_array
            std_array = sum(abs(std_array)) / len(std_array)
        else:
            forecast_array = np.array(forecasts)
            orders_array = np.array(self.__orders)
            print(orders_array)
            print(forecast_array)
            std_array = orders_array - forecast_array
            std_array = sum(abs(std_array)) / len(std_array)
        return std_array

    def calculate_mean_forecast_error(self):
        pass

    def calculate_mean_aboslute_percentage_error(self, **forecasts) -> list:
        pass

    def optimise_select_optimal_forecast_technique(self):
        pass

    def model_linear_regression_forecast(self):
        pass

    def model_autoregressive_forecast(self):
        pass

    # select which algorithm to use list available algorithms in the documentations
    def model_genetic_algorithm(self):
        pass
