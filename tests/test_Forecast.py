import unittest
from unittest import TestCase
from decimal import Decimal

from supplychainpy.demand import forecast_demand


class TestForecast(TestCase):
    _orders = [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20]
    _orders2 = [4, 5, 7, 33, 45, 53, 55, 35, 53, 53, 43, 34]
    _weights = [.3, .5, .2]

    def test_moving_average(self):
        with self.assertRaises(expected_exception=ValueError):
            d = forecast_demand.Forecast(self._orders)
            d.calculate_moving_average_forecast(forecast_length=6, base_forecast=True, start_position=1)




if __name__ == '__main__':
    unittest.main()
