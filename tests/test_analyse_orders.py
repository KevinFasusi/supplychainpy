import logging
import unittest
from decimal import Decimal
from unittest import TestCase

from supplychainpy import model_inventory
from supplychainpy.inventory import analyse_uncertain_demand
from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
from supplychainpy.sample_data.config import ABS_FILE_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestAnalyseOrders(TestCase):
    """A class for testing the output of analysisng orders using the UncertainDemand class."""
    def setUp(self):
        self._z_value = Decimal(1.28)
        self._lead_time = Decimal(4)
        self._holding_cost_percentge = Decimal(0.25)
        self._retail_price = Decimal(5000)
        self._unit_cost = Decimal(55)
        self._reorder_cost = Decimal(450)
        self._quantity_on_hand = 1000
        self._backlog = 0

        self._data_set = {'jan': 25, 'feb': 25, 'mar': 25, 'apr': 25, 'may': 25, 'jun': 25,
                          'jul': 75, 'aug': 75, 'sep': 75, 'oct': 75, 'nov': 75, 'dec': 75}

        self._orders_analysis = model_inventory.analyse(
            file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
            z_value=Decimal(1.28),
            reorder_cost=Decimal(5000),
            file_type="csv",
            length=12,
            currency='USD')

        self._uncertain_demand = analyse_uncertain_demand.UncertainDemand(
            self._data_set,
            sku='Rx493-90',
            lead_time=self._lead_time,
            reorder_cost=self._reorder_cost,
            z_value=self._z_value,
            holding_cost=self._holding_cost_percentge,
            retail_price=self._retail_price,
            unit_cost=self._unit_cost,
            currency='USD',
            quantity_on_hand=self._quantity_on_hand,
            backlog=0
            )

    def test_orders_type(self):
        """Asserts orders_analysis returns a list type"""
        self.assertIsInstance(self._orders_analysis, list)

    def test_order_list_type(self):
        """Asserts the orders_analysis returns a list of UncertainDemand objects"""
        for order in self._orders_analysis:
            self.assertIsInstance(order, UncertainDemand)

    def test_safety_stock(self):
        """Asserts orders_analysis returns the standard deviation of orders"""
        safety_stock = self._uncertain_demand.safety_stock
        avg_order = sum([int(item) for item in self._data_set.values()]) //len(self._data_set)
        variance = [(item - avg_order) for item in self._data_set.values()]
        stdev = pow(sum([pow(j, 2) for j in variance]) / len(self._data_set), 0.5)
        cal_safety = lambda x, y, z: x * y * (z ** 0.5)
        test_safety = cal_safety(float(self._z_value), float(stdev), float(self._lead_time))
        self.assertEqual(float(safety_stock), float(test_safety))

    def test_demand_variability(self):
        """Asserts order_analysis returns the demand variability of orders"""
        demand_variability = self._uncertain_demand.demand_variability
        avg_order = sum([int(item) for item in self._data_set.values()]) //len(self._data_set)
        variance = [(item - avg_order) for item in self._data_set.values()]
        stdev = pow(sum([pow(j, 2) for j in variance]) / len(self._data_set), 0.5)
        cal_variability = lambda x, y: x / y
        test_variability = cal_variability(stdev, avg_order)
        self.assertEqual(demand_variability, test_variability)

    def test_reorder_level(self):
        """Asserts order_analysis returns the reorder_level"""
        reorder_level = self._uncertain_demand.reorder_level
        avg_order = sum([int(item) for item in self._data_set.values()]) //len(self._data_set)
        variance = [(item - avg_order) for item in self._data_set.values()]
        stdev = pow(sum([pow(j, 2) for j in variance]) / len(self._data_set), 0.5)
        cal_safety = lambda x, y, z: x * y * (z ** 0.5)
        safety_stock = cal_safety(float(self._z_value), float(stdev), float(self._lead_time))
        cal_reorder_level = lambda x, y, z: ((x ** 0.5) * y) + z
        test_reorder = cal_reorder_level(float(self._lead_time), avg_order, float(safety_stock))
        self.assertEqual(float(reorder_level), test_reorder)

    def test_fixed_order_quantity(self):
        """Asserts order_analysis returns the fixed_order_quantity"""
        fixed_order_quantity = self._uncertain_demand.fixed_order_quantity
        avg_order = sum([int(item) for item in self._data_set.values()]) //len(self._data_set)
        cal_fixed_orders = lambda j, x, y, z: (2 * j * (x / (y * z))) ** 0.5
        test_fixed_orders = cal_fixed_orders(
            float(self._reorder_cost),
            float(avg_order),
            float(self._unit_cost),
            float(self._holding_cost_percentge)
            )

        self.assertEqual(int(fixed_order_quantity), int(test_fixed_orders))

    def test_excess_quantity(self):
        """Asserts order_analysis returns excess_stock"""
        excess = self._uncertain_demand.excess_stock
        avg_order = sum([int(item) for item in self._data_set.values()]) //len(self._data_set)
        variance = [(item - avg_order) for item in self._data_set.values()]
        stdev = pow(sum([pow(j, 2) for j in variance]) / len(self._data_set), 0.5)
        cal_safety = lambda x, y, z: x * y * (z ** 0.5)
        safety_stock = cal_safety(float(self._z_value), float(stdev), float(self._lead_time))
        cal_reorder_level = lambda x, y, z: ((x ** 0.5) * y) + z
        reorder = cal_reorder_level(float(self._lead_time), avg_order, float(safety_stock))
        cal_excess = lambda x, y, z: round(x - (y + (y - z)), 0) if x > y + (y - z) else 0
        test_excess = cal_excess(self._quantity_on_hand, reorder, safety_stock)
        self.assertEqual(int(excess), int(test_excess))

    def test_shortage_quantity(self):
        """Asserts order_analysis returns shortages"""
        shortages = self._uncertain_demand.shortages
        avg_order = sum([int(item) for item in self._data_set.values()]) //len(self._data_set)
        variance = [(item - avg_order) for item in self._data_set.values()]
        stdev = pow(sum([pow(j, 2) for j in variance]) / len(self._data_set), 0.5)
        cal_safety = lambda x, y, z: x * y * (z ** 0.5)
        safety_stock = cal_safety(float(self._z_value), float(stdev), float(self._lead_time))
        cal_reorder_level = lambda x, y, z: ((x ** 0.5) * y) + z
        reorder = cal_reorder_level(float(self._lead_time), avg_order, float(safety_stock))
        cal_shortages = lambda l, k, j, x, y: round(abs(((j + (j - k)) - l) + x)) if l < k else 0
        test_shortage = cal_shortages(
            self._quantity_on_hand,
            safety_stock, reorder,
            self._quantity_on_hand,
            self._backlog
            )
        self.assertEqual(shortages, test_shortage)

    def test_is_average(self):
        """Asserts the average value of the demand"""
        avg_orders = Decimal(self._uncertain_demand.average_orders)
        self.assertEqual(avg_orders, 50)


    def test_order_constraint(self):
        """Test the constraint for performing the calculation with less than five data points"""
        orders_placed = [25, 25, 25]
        with self.assertRaises(Exception):
            analyse_uncertain_demand.UncertainDemand(
                orders=orders_placed,
                sku='Rx493-90',
                lead_time=Decimal(4),
                unit_cost=Decimal(40),
                reorder_cost=Decimal(400),
                retail_price=Decimal(600),
                currency='USD'
                )



if __name__ == '__main__':
    unittest.main()
