import unittest
from decimal import Decimal
from unittest import TestCase

from supplychainpy.demand import analyse_uncertain_demand


class TestAnalyseOrders(TestCase):
    _data_set = {'jan': 25, 'feb': 25, 'mar': 25, 'apr': 25, 'may': 25, 'jun': 25, 'jul': 75,
                 'aug': 75, 'sep': 75, 'oct': 75, 'nov': 75, 'dec': 75}

    def test_is_average(self):
        # act

        d = analyse_uncertain_demand.UncertainDemand(self._data_set, sku='Rx493-90', lead_time=Decimal(4),
                                                     reorder_cost=Decimal(450), z_value=Decimal(1.28),
                                                     holding_cost=Decimal(0.25), retail_price=Decimal(4.58),
                                                     unit_cost=Decimal(55))
        a = Decimal(d.average_orders)
        # assert
        self.assertEqual(a, 50)

    def test_order_constraint(self):
        # arrange
        orders_placed = [25, 25,25] # less than five demand are specified
        # act
        # assert
        with self.assertRaises(AttributeError):
            analyse_uncertain_demand.UncertainDemand(orders=orders_placed, sku='Rx493-90', lead_time=Decimal(4),
                                                     unit_cost=Decimal(40), reorder_cost=Decimal(400),
                                                     retail_price=Decimal(600))

    def test_standard_deviation(self):
        # arrange
        # act
        d = analyse_uncertain_demand.UncertainDemand(self._data_set, sku='Rx493-90', lead_time=Decimal(4),
                                                     reorder_cost=Decimal(450), z_value=Decimal(1.28),
                                                     holding_cost=Decimal(0.25), retail_price=Decimal(4.58),
                                                     unit_cost=Decimal(55))
        a = d.standard_deviation
        # assert
        self.assertEqual(a, 25)




if __name__ == '__main__':
    unittest.main()
