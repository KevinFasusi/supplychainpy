import logging
import re
from unittest import TestCase

from decimal import Decimal

import multiprocessing

import os

from supplychainpy import model_inventory
from supplychainpy._helpers._config_file_paths import ABS_FILE_PICKLE
from supplychainpy.reporting.load import batch, pickle_ses_forecast, cleanup_pickled_files
from supplychainpy.sample_data.config import ABS_FILE_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestReportingSuiteLoadScript(TestCase):
    def setUp(self):
        self.orders_analysis = model_inventory.analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_XSM'],
                                                       z_value=Decimal(1.28),
                                                       reorder_cost=Decimal(5000),
                                                       file_type="csv",
                                                       length=12,
                                                       currency='USD')

        self.cores = int(multiprocessing.cpu_count()) - 1
        self.batched_analysis = [i for i in batch(self.orders_analysis, self.cores)]

    def tearDown(self):
        cleanup_pickled_files()

    def test_pickled_ses_files(self):
        pickled_paths = pickle_ses_forecast(batched_analysis=self.batched_analysis)
        path_to_newly_pickled_files = []
        ses_file_regex = re.compile('[s][e][s]\d+[.][p][i][c][k][l][e]')
        for filename in os.listdir(ABS_FILE_PICKLE):
            if ses_file_regex.match(filename) and filename.endswith(".pickle"):
                path_to_newly_pickled_files.append(filename)
        path_to_newly_pickled_files = [os.path.abspath(os.path.join(ABS_FILE_PICKLE, path)) for path in path_to_newly_pickled_files]
        for i in path_to_newly_pickled_files:
            self.assertIn(i, pickled_paths)