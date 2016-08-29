import os
import unittest
import logging
from cmath import isclose
from decimal import Decimal
from unittest import TestCase

from supplychainpy import model_inventory

#logging.basicConfig(filename='suchpy_tests_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class TestBuildModel(TestCase):
    _yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
                      'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}
    _yearly_demand2 = {'jan': 75}

    _categories = ('unit_cost', 'sku', 'reorder_level', 'safety_stock', 'reorder_quantity', 'ABC_XYZ_Classification',
                   'revenue', 'standard_deviation', 'quantity_on_hand', 'average_orders', 'shortages', 'excess_stock',
                   'demand_variability')

    _expected_values = ('50', 'RX983-90', '99', '12', '57', '', '360000', '25', '390', '50', '0', '205', '0.500')

    def test_model_orders_type(self):
        """Tests analyse_orders returns a 'dict' type. """
        summary = model_inventory.analyse_orders(self._yearly_demand,
                                                 sku_id='RX983-90',
                                                 lead_time=Decimal(3),
                                                 unit_cost=Decimal(50.99),
                                                 reorder_cost=Decimal(400),
                                                 z_value=Decimal(1.28),
                                                 retail_price=Decimal(600),
                                                 quantity_on_hand=Decimal(390))

        self.assertIsInstance(summary, dict)

    def test_model_orders_length(self):
        """supplied orders data must be greater than 3 items long."""
        with self.assertRaises(expected_exception=ValueError):
            summary = model_inventory.analyse_orders(self._yearly_demand2,
                                                     sku_id="RX983-90",
                                                     lead_time=Decimal(3),
                                                     unit_cost=Decimal(50.99),
                                                     reorder_cost=Decimal(400),
                                                     z_value=Decimal(.28),
                                                     retail_price=Decimal(600),
                                                     quantity_on_hand=Decimal(390))

    def test_model_orders_content(self):
        """ test the return values for simple analyse orders"""
        summary = model_inventory.analyse_orders(self._yearly_demand,
                                                 sku_id="RX983-90",
                                                 lead_time=Decimal(3),
                                                 unit_cost=Decimal(50),
                                                 reorder_cost=Decimal(400),
                                                 z_value=Decimal(.28),
                                                 retail_price=Decimal(600),
                                                 quantity_on_hand=Decimal(390))

        for i, k in zip(self._categories, self._expected_values):
            self.assertEqual(str(k), summary.get(i))

            # finish with all members

    def test_standard_deviation_row_count(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_row(file_path=abs_file_path,
                                                         z_value=Decimal(1.28),
                                                         reorder_cost=Decimal(400),
                                                         retail_price=Decimal(455))

        # assert
        self.assertEqual(len(d), 16)

    def test_file_path_extension_row(self):
        # arrange,act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/tel.tt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # assert
        with self.assertRaises(expected_exception=Exception):
            model_inventory.analyse_orders_from_file_row(file_path=abs_file_path,
                                                         reorder_cost=Decimal(450),
                                                         z_value=Decimal(1.28), retail_price=Decimal(455))

    def test_file_path_extension_col(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test.tt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # assert
        with self.assertRaises(expected_exception=Exception):
            model_inventory.analyse_orders_from_file_row(abs_file_path,
                                                         reorder_cost=Decimal(450),
                                                         z_value=Decimal(1.28), retail_price=Decimal(100))

    def test_standard_deviation_col_count(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = model_inventory.analyse_orders_from_file_col(file_path=abs_file_path,
                                                         sku_id='RX9304-43',
                                                         lead_time=Decimal(2),
                                                         unit_cost=Decimal(400),
                                                         reorder_cost=Decimal(45),
                                                         z_value=Decimal(1.28),
                                                         file_type="text",
                                                         retail_price=Decimal(30))
        # assert
        self.assertEqual(len(d), 18)

    def test_standard_deviation_col_count_csv(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data_col.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_col(abs_file_path, 'RX9304-43',
                                                         reorder_cost=Decimal(45),
                                                         unit_cost=Decimal(400),
                                                         lead_time=Decimal(45),
                                                         z_value=Decimal(1.28),
                                                         file_type="csv",
                                                         retail_price=Decimal(30))
        # assert
        self.assertEqual(len(d), 18)

    def test_standard_deviation_row_value(self):
        # arrange
        std = int(0)

        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_row(file_path=abs_file_path,
                                                         retail_price=Decimal(400),
                                                         reorder_cost=Decimal(450),
                                                         z_value=Decimal(1.28))

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
        d = model_inventory.analyse_orders_from_file_col(file_path=abs_file_path,
                                                         sku_id='RX9304-43',
                                                         reorder_cost=Decimal(45),
                                                         unit_cost=Decimal(400),
                                                         lead_time=Decimal(45),
                                                         z_value=Decimal(1.28),
                                                         file_type="text",
                                                         retail_price=Decimal(30))

        # assert
        self.assertEqual(Decimal(d.get('standard_deviation')), 25)

    def test_analyse_orders_from_file_row_csv(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = model_inventory.analyse_orders_from_file_row(file_path=abs_file_path,
                                                         reorder_cost=Decimal(45),
                                                         z_value=Decimal(1.28),
                                                         file_type="csv",
                                                         retail_price=Decimal(30),
                                                         currency='USD')
        std = 0
        for row in d:
            if row['sku'] == 'KR202-210':
                std = row.get('standard_deviation')
                break
        # assert
        self.assertTrue(isclose(Decimal(std), 950, abs_tol=2))

    def test_file_path_abcxyz_extension(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.sv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # assert
        with self.assertRaises(expected_exception=Exception):
            abc = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                                  z_value=Decimal(1.28),
                                                                  reorder_cost=Decimal(5000),
                                                                  file_type="csv")

    def test_abcxyz_classification(self):
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        abc = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                              z_value=Decimal(1.28),
                                                              reorder_cost=Decimal(5000),
                                                              file_type="csv")
        for sku in abc:
            item = sku.orders_summary()
            if item['sku'] == 'KR202-209':
                self.assertEqual(item['ABC_XYZ_Classification'], 'AY')


if __name__ == '__main__':
    unittest.main()
