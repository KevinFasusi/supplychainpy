import unittest
from unittest import TestCase

from supplychainpy.demand import forecast_demand
from supplychainpy.demand.evolutionary_algorithms import OptimiseSmoothingLevelGeneticAlgorithm
from supplychainpy.demand.forecast_demand import Forecast


class TestForecast(TestCase):
    __orders = [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20]
    __orders2 = [4, 5, 7, 33, 45, 53, 55, 35, 53, 53, 43, 34]
    __weights = [.3, .5, .2]

    def setUp(self):
        self.__orders_ex = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147, 188, 161,
                            162,
                            169,
                            185,
                            188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218, 264, 304]

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

    def test_simple_exponential_smoothing(self):
        total_orders = 0
        for order in self.__orders_ex[:12]:
            total_orders += order
        avg_orders = total_orders / 12
        f = Forecast(self.__orders_ex, avg_orders)
        alpha = [0.2, 0.3, 0.4, 0.5, 0.6]
        s = [i for i in f.simple_exponential_smoothing(*alpha)]
        sum_squared_error = f.sum_squared_errors(s, 0.5)
        self.assertEqual(15346.859449597407, sum_squared_error[0.5])

    def test_standard_error(self):
        total_orders = 0
        for order in self.__orders_ex[:12]:
            total_orders += order
        avg_orders = total_orders / 12
        f = Forecast(self.__orders_ex, avg_orders)
        alpha = [0.2, 0.3, 0.4, 0.5, 0.6]
        s = [i for i in f.simple_exponential_smoothing(*alpha)]
        sum_squared_error = f.sum_squared_errors(s, 0.5)
        standard_error = f.standard_error(sum_squared_error, len(self.__orders_ex), 0.5)
        self.assertEqual(20.93995459784777, standard_error)

    def test_optimise_smoothing_level_genetic_algorithm(self):
        total_orders = 0
        for order in self.__orders_ex[:12]:
            total_orders += order
        avg_orders = total_orders / 12
        f = Forecast(self.__orders_ex, avg_orders)
        alpha = [0.2, 0.3, 0.4, 0.5, 0.6]
        s = [i for i in f.simple_exponential_smoothing(*alpha)]
        sum_squared_error = f.sum_squared_errors(s, 0.5)
        standard_error = f.standard_error(sum_squared_error, len(self.__orders_ex), 0.5)
        evo_mod = OptimiseSmoothingLevelGeneticAlgorithm(orders=self.__orders_ex, average_order=avg_orders,
                                                         smoothing_level=0.5,
                                                         population_size=10, standard_error=standard_error)
        self.assertGreaterEqual(len(evo_mod.initial_population),10)


if __name__ == '__main__':
    unittest.main()
