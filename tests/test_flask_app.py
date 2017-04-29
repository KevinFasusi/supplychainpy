import logging
import os
import tempfile

from unittest import TestCase

from flask import Flask
import tkinter as tk
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import serialise_config
from supplychainpy.launch_reports import load_db, SupplychainpyReporting
from supplychainpy.reporting.config.settings import ProdConfig
from supplychainpy.reporting.extensions import db
from supplychainpy.sample_data.config import ABS_FILE_PATH

#logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


#class TestFlaskReports(TestCase):
#
#   def setUp(self):
#       app = Flask(__name__, instance_relative_config=True)
#       app.config.from_object(ProdConfig)
#       db.init_app(app)
#       self.db_rs, app.config['DATABASE'] = tempfile.mkstemp()
#       app.config['TESTING'] = True
#       self.app = app.test_client()
#       app_settings = {
#           'file': ABS_FILE_PATH['COMPLETE_CSV_XSM'],
#           'currency': 'USD'
#       }
#       serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
#       with app.app_context():
#           load_db(file=ABS_FILE_PATH['COMPLETE_CSV_XSM'])
#
#   def test_loaded_db(self):
#       index_page = self.app.get('/')
#       print(index_page.data)
#       headings = [b'Top 10 Shortages', b'Classification Breakdown',  b'Top 10 Shortages']
       #for heading in headings:
       #    assert heading in index_page.data
       #inventory_analysis = self.app.get('/api/inventory_analysis')
       #headings = [b'abc_xyz_classification', b'average_orders',  b'currency']
       #for heading in headings:
       #    assert heading in inventory_analysis.data
       #launcher = tk.Tk()
       #spawn = SupplychainpyReporting(launcher)
       #with self.assertRaises(ValueError):
       #    spawn.spawn_reports()




