<<<<<<< HEAD
from decimal import Decimal
=======
import unittest
from decimal import Decimal
<<<<<<< HEAD

>>>>>>> 12442747b231687ec11b9e4d642a81f79c733460
from supplybipy import analyse_orders
=======
>>>>>>> 1abec7657f65b054adff81d6d75d02f657abb523
from unittest import TestCase

from supplybipy.orders import analyse_orders


class TestAnalyseOrders(TestCase):
    def test_is_average(self):
        # act
        data_set = {'jan': 25, 'feb': 25, 'mar': 25, 'apr': 25, 'may': 25, 'jun': 25, 'jul': 75,
                    'aug': 75, 'sep': 75, 'oct': 75, 'nov': 75, 'dec': 75}
<<<<<<< HEAD

        d = analyse_orders.OrdersUncertainDemand(data_set, 'Rx493-90', 4, 554.99, 400.00)
        a = d.get_average_orders
=======
        d = analyse_orders.OrdersUncertainDemand(data_set, 'Rx493-90', 4, 554.99, 400.00)
        a = Decimal(d.get_average_orders)
>>>>>>> 12442747b231687ec11b9e4d642a81f79c733460
        # assert
        self.assertEqual(Decimal(a), 50)

    def test_order_constraint(self):
        # arrange
        orders_placed = [2, 2, 2]  # less than five orders are specified
        # act
        # assert
        with self.assertRaises(TypeError):
            analyse_orders.OrdersUncertainDemand(orders_placed, 'Rx493-90', 4)

    def test_standard_deviation(self):
        # arrange
        data_set = {'jan': 25, 'feb': 25, 'mar': 25, 'apr': 25, 'may': 25, 'jun': 25, 'jul': 75,
                    'aug': 75, 'sep': 75, 'oct': 75, 'nov': 75, 'dec': 75}
<<<<<<< HEAD

=======
>>>>>>> 12442747b231687ec11b9e4d642a81f79c733460
        # act
        d = analyse_orders.OrdersUncertainDemand(data_set, 'Rx493-90', 4, 554.99, 400.00)
        a = d.standard_deviation
        # assert
        self.assertEqual(a, 25)


# put the tests here. if this is called as main then the tests will run


if __name__ == '__main__':
    unittest.main()
