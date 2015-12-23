import unittest
from unittest import TestCase
from decimal import Decimal
from supplybipy import build_model
import os

class TestBuildModel(TestCase):
    def test_standard_deviation_row_count(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = build_model.analyse_orders_from_file_row(abs_file_path, 1.28, 400)
        # act

        # assert
        self.assertGreater(len(d), 2)

    def test_standard_deviation_col_count(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = build_model.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28)
        # act
        # assert
        self.assertGreater(len(d), 2)

    def test_standard_deviation_row_value(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test_row_small.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        d = build_model.analyse_orders_from_file_row(abs_file_path, 1.28, 400)

        for row in d:
            std = row.get('standard_deviation')
        # assert
        self.assertEqual(Decimal(std), 227)

    def test_standard_deviation_col_value(self):
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplybipy/test.txt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        d = build_model.analyse_orders_from_file_col(abs_file_path, 'RX9304-43', 2, 400, 45, 1.28)
        # act
        # assert
        print(d.get('standard_deviation'))
        self.assertGreater(Decimal(d.get('standard_deviation')), 25)


if __name__ == '__main__':
    unittest.main()
