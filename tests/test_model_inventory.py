import unittest
from cmath import isclose
from unittest import TestCase
from decimal import Decimal
from supplychainpy import model_inventory
from supplychainpy.demand import economic_order_quantity
import os


class TestBuildModel(TestCase):
    _yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
                      'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}
    _yearly_demand2 = {'jan': 75}
    _t = {}
    _inventory_summary = {'average_order': type(0.00), 'economic_order_quantity': type(0.00),
                          'reorder_level': type(0.00)}

    def test_model_orders_type(self):
        summary = model_inventory.analyse_orders(self._yearly_demand, 'RX983-90', 3, 50.99, 400, 1.28)
        self.assertIs(type(summary), type(self._t))

    def test_model_orders_length(self):
        with self.assertRaises(expected_exception=ValueError):
            summary = model_inventory.analyse_orders(self._yearly_demand2, 'RX983-90', 3, 50.99, 400, 1.28)

    def test_model_orders_content(self):
        summary = model_inventory.analyse_orders(self._yearly_demand, 'RX983-90', 3, 50.99, 400, 1.28)
        self.assertEqual(int(summary.get("average_order")), int(50))
        self.assertEqual(int(summary.get("standard_deviation")), int(25))
        # finish with all members

    def test_standard_deviation_row_count(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_row(abs_file_path, Decimal(1.28), Decimal(400))

        # assert
        self.assertEqual(len(d), 16)

    def test_file_path_extension_row(self):
        # arrange,act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/tel.tt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # assert
        with self.assertRaises(expected_exception=Exception):
            d = model_inventory.analyse_orders_from_file_row(abs_file_path, 1.28, 400, file_type="text")

    def test_file_path_extension_col(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test.tt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # assert
        with self.assertRaises(expected_exception=Exception):
            d = model_inventory.analyse_orders_from_file_col(abs_file_path, 1.28, 400, file_type="text")

    def test_standard_deviation_col_count(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', Decimal(2), Decimal(400),
                                                         Decimal(45), Decimal(1.28), file_type="text")
        # assert
        self.assertEqual(len(d), 11)

    def test_standard_deviation_col_count_csv(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data_col.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28, file_type="csv")
        # assert
        self.assertEqual(len(d), 11)

    def test_standard_deviation_row_value(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_row(abs_file_path, 1.28, 400)

        for row in d:
            std = row.get('standard_deviation')
        # assert
        self.assertEqual(Decimal(std), 25)

    def test_standard_deviation_col_value(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28, file_type="text")

        # assert
        self.assertEqual(Decimal(d.get('standard_deviation')), 25)

    def test_analyse_orders_from_file_row_csv(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_row(abs_file_path, z_value=Decimal(1.28),
                                                         reorder_cost=Decimal(400), file_type="csv")
        for row in d:
            if row['sku'] == 'KR202-209':
                std = row.get('standard_deviation')
        # assert
        self.assertTrue(isclose(Decimal(std), 976, abs_tol=2))

    def test_file_path_abcxyz_extension(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data.sv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # assert
        with self.assertRaises(expected_exception=Exception):
            abc = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                                  reorder_cost=Decimal(5000), file_type="csv")

    def test_file_path_abcxyz(self):
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        abc = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                              reorder_cost=Decimal(5000),
                                                              file_type="csv")
        for sku in abc.orders:
            item = sku.orders_summary()
            if item['sku'] == 'KR202-209':
                self.assertEqual(item['ABC_XYZ_Classification'], 'CZ')


if __name__ == '__main__':
    unittest.main()
