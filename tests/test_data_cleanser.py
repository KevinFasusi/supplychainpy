from unittest import TestCase

import logging

from supplychainpy._helpers import _data_cleansing
from supplychainpy.sample_data.config import ABS_FILE_PATH

#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestCleanser(TestCase):
    def test_incorrect_row_length(self):
        """ Tests for incorrect specification of number of columns after initial SKU identification. """
        with open(ABS_FILE_PATH['COMPLETE_CSV_XSM']) as f:
            for i in range(0, 11):
                with self.assertRaises(expected_exception=Exception):
                    _data_cleansing.clean_orders_data_row_csv(f, length=i)
