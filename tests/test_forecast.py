import unittest
from unittest import TestCase

import logging

from supplychainpy.demand._evo_algo import OptimiseSmoothingLevelGeneticAlgorithm
from supplychainpy.demand._forecast_demand import Forecast

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TestForecast(TestCase):
    __orders = [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20]
    __orders2 = [4, 5, 7, 33, 45, 53, 55, 35, 53, 53, 43, 34]
    __weights = [.3, .5, .2]

    def setUp(self):
        self.__orders_ex = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147, 188, 161,
                            162, 169, 85, 188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218, 264, 304]

    def test_moving_average_value_err(self):
        with self.assertRaises(expected_exception=ValueError):
            d = Forecast(self.__orders)
            d.moving_average_forecast(forecast_length=6, base_forecast=True, start_position=1)

    def test_weighted_moving_average_value_err(self):
        with self.assertRaises(expected_exception=ValueError):
            forecast = Forecast(self.__orders)
            forecast.weighted_moving_average_forecast(weights=self.__weights, average_period=2, forecast_length=3)

    def test_weighted_moving_average_list_err(self):
        with self.assertRaises(expected_exception=ValueError):
            forecast = Forecast(self.__orders)
            forecast.weighted_moving_average_forecast(weights=self.__weights[:2], average_period=2, forecast_length=3)

    def test_mean_absolute_deviation(self):
        forecast = Forecast(self.__orders)
        forecast.weighted_moving_average_forecast(weights=self.__weights, average_period=3, forecast_length=9,
                                                  base_forecast=True, start_position=3)
        k = Forecast(self.__orders)
        k.moving_average_forecast(forecast_length=9, base_forecast=True, start_position=3, average_period=3)
        result_array = k.mean_absolute_deviation(forecast.weighted_moving_average)
        result_array2 = forecast.mean_absolute_deviation(k.moving_average)
        self.assertNotEqual(result_array, result_array2)

    def test_mean_absolute_deviation_(self):
        orders1 = [1, 3, 5, 67, 4, 65, 44, 50, 48, 24, 34, 20]
        orders2 = [1, 3, 5, 67, 4, 65, 44, 50, 48, 24, 34, 20]
        weights = [.5, .3, .2]
        forecast = Forecast(orders1)
        forecast.weighted_moving_average_forecast(weights=weights, average_period=3, forecast_length=9,
                                                  start_position=3)
        # d.moving_average(forecast_length=3, base_forecast=True, start_position=3)
        # print(d.moving_average_forecast)
        k = Forecast(orders2)
        k.moving_average_forecast(forecast_length=9, start_position=3, average_period=3)
        result_array = k.mean_absolute_deviation(forecast.weighted_moving_average)
        result_array2 = forecast.mean_absolute_deviation(k.moving_average)
        self.assertEqual(result_array, result_array2)

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
        self.assertEqual(28447.178137569197, sum_squared_error[0.5])

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
        self.assertEqual(29, round(standard_error))

    def test_optimise_smoothing_level_genetic_algorithm(self):
        total_orders = 0
        for order in self.__orders_ex[:12]:
            total_orders += order
        avg_orders = total_orders / 12
        f = Forecast(self.__orders_ex, avg_orders)
        alpha = [0.2, 0.3, 0.4, 0.5, 0.6]
        s = [i for i in f.simple_exponential_smoothing(*alpha)]
        sum_squared_error = f.sum_squared_errors(s, 0.5)
        standard_error = f.standard_error(sum_squared_error, len(self.__orders_ex), 0.5, 2)
        evo_mod = OptimiseSmoothingLevelGeneticAlgorithm(orders=self.__orders_ex,
                                                         average_order=avg_orders,
                                                         smoothing_level=0.5,
                                                         population_size=10,
                                                         standard_error=standard_error,
                                                         recombination_type='single_point')
        pop = evo_mod.initial_population()

        self.assertGreaterEqual(len(pop), 2)
        self.assertNotAlmostEqual(pop[0], 20.72, places=3)
        self.assertNotAlmostEqual(pop[1], 0.73, places=3)

    def test_holts_trend_corrected_exponential_smoothing_len(self):
        total_orders = 0

        for order in self.__orders_ex[:12]:
            total_orders += order

        avg_orders = total_orders / 12
        f = Forecast(self.__orders_ex)
        p = [i for i in f.holts_trend_corrected_exponential_smoothing(0.5, 0.5, 155.88, 0.8369)]
        self.assertEqual(len(p), 36)

    def test_holts_trend_corrected_exponential_smoothing_forecast(self):
        total_orders = 0

        for order in self.__orders_ex[:12]:
            total_orders += order

        f = Forecast(self.__orders_ex)
        p = [i for i in f.holts_trend_corrected_exponential_smoothing(0.5, 0.5, 155.88, 0.8369)]
        holts_forecast = f.holts_trend_corrected_forecast(forecast=p, forecast_length=4)
        self.assertEqual(round(holts_forecast[0]), 281)
        self.assertEqual(round(holts_forecast[1]), 307)
        self.assertEqual(round(holts_forecast[2]), 334)
        self.assertEqual(round(holts_forecast[3]), 361)

        # sum_squared_error = f.sum_squared_errors(p, 0.5)
        # print(sum_squared_error)
        # standard_error = f.standard_error(sum_squared_error, len(self.__orders_ex), 0.5, 2)
        # print(standard_error)
        # standard_error = f.standard_error(sum_squared_error, len(self.__orders_ex), 0.5)


if __name__ == '__main__':
    unittest.main()
