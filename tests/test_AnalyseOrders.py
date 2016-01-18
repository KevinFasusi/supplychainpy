import unittest
from decimal import Decimal
from unittest import TestCase

from supplybipy.demand import analyse_uncertain_demand


class TestAnalyseOrders(TestCase):
    _data_set = {'jan': 25, 'feb': 25, 'mar': 25, 'apr': 25, 'may': 25, 'jun': 25, 'jul': 75,
                 'aug': 75, 'sep': 75, 'oct': 75, 'nov': 75, 'dec': 75}

    def test_is_average(self):
        # act

        d = analyse_uncertain_demand.UncertainDemand(self._data_set, 'Rx493-90', 4, 554.99, 400.00)
        a = Decimal(d.get_average_orders)
        # assert
        self.assertEqual(a, 50)

    def test_order_constraint(self):
        # arrange
        orders_placed = [2, 2, 2]  # less than five demand are specified
        # act
        # assert
        with self.assertRaises(TypeError):
            analyse_uncertain_demand.UncertainDemand(orders_placed, 'Rx493-90', 4)

    def test_standard_deviation(self):
        # arrange
        # act
        d = analyse_uncertain_demand.UncertainDemand(self._data_set, 'Rx493-90', 4, 554.99, 400.00)
        a = d.standard_deviation
        # assert
        self.assertEqual(a, 25)


# put the tests here. if this is called as main then the tests will run


if __name__ == '__main__':
    unittest.main()
