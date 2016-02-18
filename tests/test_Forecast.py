import unittest
from unittest import TestCase
from decimal import Decimal

from supplychainpy.demand import forecast_demand


class TestForecast(TestCase):
    __orders = [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20]
    __orders2 = [4, 5, 7, 33, 45, 53, 55, 35, 53, 53, 43, 34]
    __weights = [.3, .5, .2]

    def test_moving_average_value_err(self):
        with self.assertRaises(expected_exception=ValueError):
            d = forecast_demand.Forecast(self.__orders)
            d.moving_average_forecast(forecast_length=6, base_forecast=True, start_position=1)

    def test_weighted_moving_average_value_err(self):
        with self.assertRaises(expected_exception=ValueError):
            forecast = forecast_demand.Forecast(self.__orders)
            forecast.weighted_moving_average_forecast(weights=self.__weights, average_period=2, forecast_length=3)

    def test_weighted_moving_average_list_err(self):
        with self.assertRaises(expected_exception=ValueError):
            forecast = forecast_demand.Forecast(self.__orders)
            forecast.weighted_moving_average_forecast(weights=self.__weights[:2], average_period=2, forecast_length=3)

    def test_mean_absolute_deviation(self):
        forecast = forecast_demand.Forecast(self.__orders)
        forecast.weighted_moving_average_forecast(weights=self.__weights, average_period=3, forecast_length=9,
                                                  base_forecast=True, start_position=3)
        k = forecast_demand.Forecast(self.__orders)
        k.moving_average_forecast(forecast_length=9, base_forecast=True, start_position=3, average_period=3)
        result_array = k.mean_absolute_deviation(forecast.weighted_moving_average)
        result_array2 = forecast.mean_absolute_deviation(k.moving_average)
        self.assertNotEqual(result_array, result_array2)

    def test_mean_absolute_deviation_(self):
        orders1 = [1, 3, 5, 67, 4, 65, 44, 50, 48, 24, 34, 20]
        orders2 = [1, 3, 5, 67, 4, 65, 44, 50, 48, 24, 34, 20]
        weights = [.5, .3, .2]
        forecast = forecast_demand.Forecast(orders1)
        forecast.weighted_moving_average_forecast(weights=weights, average_period=3, forecast_length=9,
                                                  start_position=3)
        # d.moving_average(forecast_length=3, base_forecast=True, start_position=3)
        # print(d.moving_average_forecast)
        k = forecast_demand.Forecast(orders2)
        k.moving_average_forecast(forecast_length=9, start_position=3, average_period=3)
        result_array = k.mean_absolute_deviation(forecast.weighted_moving_average)
        result_array2 = forecast.mean_absolute_deviation(k.moving_average)
        self.assertEquals(result_array, result_array2)

    def test_mean_forecast_error(self):
        pass

    def test_mean_aboslute_percentage_error(self):
        pass

    def test_optimise(self):
        pass

    def test_linear_regression(self):
        pass


if __name__ == '__main__':
    unittest.main()
