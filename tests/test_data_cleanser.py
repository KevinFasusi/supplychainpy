import os
from unittest import TestCase

from supplychainpy import data_cleansing


class TestCleanser(TestCase):

    def test_incorrect_row_length(self):
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        f = open(abs_file_path)

        with self.assertRaises(expected_exception=Exception):
            data_cleansing.clean_orders_data_row_csv(f, length=11)
