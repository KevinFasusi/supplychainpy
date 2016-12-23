import unittest
from unittest import TestCase

from supplychainpy.demand._evolutionary_algorithms import OptimiseSmoothingLevelGeneticAlgorithm
from supplychainpy.demand._forecast_demand import Forecast


class TestForecast(TestCase):
    def setUp(self):
        self.__orders_ex = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147, 188, 161,
                            162, 169, 85, 188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218, 264, 304]

    