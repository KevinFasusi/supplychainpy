import os
import unittest
import logging
from cmath import isclose
from decimal import Decimal
from unittest import TestCase

import pandas as pd
from pandas import DataFrame
from supplychainpy import model_inventory
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import deserialise_config
from supplychainpy.model_inventory import analyse, recommendations
from supplychainpy.sample_data.config import ABS_FILE_PATH
# logging.basicConfig(filename='suchpy_tests_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        d = model_inventory.analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                    z_value=Decimal(1.28),
                                    reorder_cost=Decimal(400),
                                    retail_price=Decimal(455),
                                    file_type='csv')

        analysed_orders = [demand.orders_summary() for demand in d]

        self.assertEqual(len(d), 39)

    def test_file_path_extension_row(self):
        with self.assertRaises(expected_exception=Exception):
            model_inventory.analyse_orders_from_file_row(file_path='test.tt',
                                                         reorder_cost=Decimal(450),
                                                         z_value=Decimal(1.28), retail_price=Decimal(455))

    def test_file_path_extension_col(self):
        # arrange, act
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/test.tt'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        with self.assertRaises(expected_exception=Exception):
            model_inventory.analyse_orders_from_file_row(abs_file_path,
                                                         reorder_cost=Decimal(450),
                                                         z_value=Decimal(1.28), retail_price=Decimal(100))

    def test_standard_deviation_col_count(self):
        d = model_inventory.analyse_orders_from_file_col(file_path=ABS_FILE_PATH['PARTIAL_COL_TXT_SM'],
                                                         sku_id='RX9304-43',
                                                         lead_time=Decimal(2),
                                                         unit_cost=Decimal(400),
                                                         reorder_cost=Decimal(45),
                                                         z_value=Decimal(1.28),
                                                         file_type="text",
                                                         retail_price=Decimal(30))
        self.assertEqual(len(d), 19)

    def test_standard_deviation_col_count_csv(self):
        d = model_inventory.analyse_orders_from_file_col(ABS_FILE_PATH['PARTIAL_COL_CSV_SM'], 'RX9304-43',
                                                         reorder_cost=Decimal(45),
                                                         unit_cost=Decimal(400),
                                                         lead_time=Decimal(45),
                                                         z_value=Decimal(1.28),
                                                         file_type="csv",
                                                         retail_price=Decimal(30))
        self.assertEqual(len(d), 19)

    def test_standard_deviation_row_value(self):
        """Test Standard deviation value of row data, from text file."""
        std = 0
        d = model_inventory.analyse_orders_from_file_row(file_path=ABS_FILE_PATH['PARTIAL_ROW_TXT_SM'],
                                                         retail_price=Decimal(400),
                                                         reorder_cost=Decimal(450),
                                                         z_value=Decimal(1.28))
        for row in d:
            std = row.get('standard_deviation')
        self.assertEqual(Decimal(std), 25)

    def test_standard_deviation_col_value(self):
        d = model_inventory.analyse_orders_from_file_col(file_path=ABS_FILE_PATH['PARTIAL_COL_TXT_SM'],
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
        """"""
        d = model_inventory.analyse_orders_from_file_row(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                                         reorder_cost=Decimal(45),
                                                         z_value=Decimal(1.28),
                                                         file_type="csv",
                                                         retail_price=Decimal(30),
                                                         currency='USD')
        std = 0
        for row in d:
            if row.get('sku') == 'KR202-210':
                std = row.get('standard_deviation')
                break
        # assert
        self.assertTrue(isclose(Decimal(std), 950, abs_tol=2))

    def test_file_path_abcxyz_extension(self):
        with self.assertRaises(expected_exception=Exception):
            abc = model_inventory.analyse_orders_abcxyz_from_file(file_path='test.ts',
                                                                  z_value=Decimal(1.28),
                                                                  reorder_cost=Decimal(5000),
                                                                  file_type="csv")

    def test_abcxyz_classification(self):
        abc = model_inventory.analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                                              z_value=Decimal(1.28),
                                                              reorder_cost=Decimal(5000),
                                                              file_type="csv")
        for sku in abc:
            item = sku.orders_summary()
            if item['sku'] == 'KR202-209':
                self.assertEqual(item['ABC_XYZ_Classification'], 'BY')

    def test_data_frame(self):
        raw_df = pd.read_csv(ABS_FILE_PATH['COMPLETE_CSV_SM'])
        analysis_df = analyse(df=raw_df, start=1, interval_length=12, interval_type='months')
        self.assertIsInstance(analysis_df[['sku', 'quantity_on_hand', 'excess_stock', 'shortages', 'ABC_XYZ_Classification']], DataFrame)

    def test_short_raw_data(self):
        yearly_demand = {'jan': 75, 'feb': 75}
        with self.assertRaises(expected_exception=ValueError):
            summary = model_inventory.analyse_orders(yearly_demand,
                                                     sku_id='RX983-90',
                                                     lead_time=Decimal(3),
                                                     unit_cost=Decimal(50.99),
                                                     reorder_cost=Decimal(400),
                                                     z_value=Decimal(1.28),
                                                     retail_price=Decimal(600),
                                                     quantity_on_hand=Decimal(390))


    #def test_recommendation_per_sku(self):
    #    app_config = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
    #    analysed_order = analyse(file_path=app_config['file'],z_value=Decimal(1.28),
    #                             reorder_cost=Decimal(5000), file_type="csv", length=12, currency='USD')
    #    skus = [sku.orders_summary().get('sku') for sku in analysed_order]
    #    holts_forecast = {analysis.sku_id: analysis.holts_trend_corrected_forecast for analysis in
    #                      analyse(file_path=app_config['file'],
    #                              z_value=Decimal(1.28),
    #                              reorder_cost=Decimal(5000),
    #                              file_type="csv",
    #                              length=12,
    #                              currency='USD')}
    #    recommend = recommendations(analysed_orders=analysed_order, forecast=holts_forecast)
#
    #    for i in recommend.get('sku_recommendations'):
    #        self.assertIn(i, skus)

if __name__ == '__main__':
    unittest.main()
