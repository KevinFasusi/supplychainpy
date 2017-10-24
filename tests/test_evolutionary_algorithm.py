from unittest import TestCase
import unittest
import logging

import collections

from supplychainpy.demand._evolutionary_algorithms import OptimiseSmoothingLevelGeneticAlgorithm
from supplychainpy.demand._forecast_demand import Forecast
#from supplychainpy.demand._evo_algo import OptimiseSmoothingLevelGeneticAlgorithm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestForecast(TestCase):
    def setUp(self):
        self.__orders_ex = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147, 188, 161,
                            162, 169, 85, 188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218, 264, 304]

        self.__smoothing_level_constant = 0.5
        self.__initial_estimate_period = 18

    def test_htces(self):
        forecast_demand = Forecast(self.__orders_ex)

        ses_forecast = [i for i in forecast_demand.simple_exponential_smoothing(*(self.__smoothing_level_constant,))]

        sum_squared_error = forecast_demand.sum_squared_errors(ses_forecast, self.__smoothing_level_constant)

        standard_error = forecast_demand.standard_error(sum_squared_error, len(self.__orders_ex), self.__smoothing_level_constant)
        total_orders = 0

        for order in self.__orders_ex[:self.__initial_estimate_period]:
            total_orders += order

        avg_orders = total_orders / self.__initial_estimate_period

        evo_mod = OptimiseSmoothingLevelGeneticAlgorithm(orders=self.__orders_ex,
                                                         average_order=avg_orders,
                                                         smoothing_level=self.__smoothing_level_constant,
                                                         population_size=10,
                                                         standard_error=standard_error,
                                                         recombination_type='two_point')

        ses_evo_forecast = evo_mod.simple_exponential_smoothing_evo(
            smoothing_level_constant=self.__smoothing_level_constant,
            initial_estimate_period=self.__initial_estimate_period)
        self.assertEqual(7, len(ses_evo_forecast))

if __name__ == "__main__":
    unittest.main()