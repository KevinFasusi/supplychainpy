import unittest
from unittest import TestCase
from decimal import Decimal
from supplybipy import model_inventory
import os


def print(selected):
    pass


class TestBuildModel(TestCase):
    _yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
                      'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}
    _t = {}
    _inventory_summary = {'average_order': type(0.00), 'economic_order_quantity': type(0.00),
                          'reorder_level': type(0.00)}

    def test_model_orders_type(self):
        summary = model_inventory.model_orders(self._yearly_demand, 'RX983-90', 3, 50.99, 400, 1.28)
        self.assertIs(type(summary), type(self._t))

    def test_model_orders_content(self):
        summary = model_inventory.model_orders(self._yearly_demand, 'RX983-90', 3, 50.99, 400, 1.28)
        for item in summary:
            self._inventory_summary.get(item)

    def test_standard_deviation_row_count(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_row(abs_file_path, 1.28, 400)
        # act

        # assert
        self.assertGreater(len(d), 2)

    def test_standard_deviation_col_count(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28, file_type="txt")
        # act
        # assert
        self.assertGreater(len(d), 2)

    def test_standard_deviation_row_value(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_row(abs_file_path, 1.28, 400)

        for row in d:
            std = row.get('standard_deviation')
        # assert
        self.assertEqual(Decimal(std), 227)

    def test_standard_deviation_col_value(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28, file_type="txt")
        # act
        # assert
        print(d.get('standard_deviation'))
        self.assertGreater(Decimal(d.get('standard_deviation')), 25)


if __name__ == '__main__':
    unittest.main()
