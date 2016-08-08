import os
import tempfile
import unittest
import tkinter as tk

from supplychainpy.launch_reports import load_db, SupplychainpyReporting
from supplychainpy.reporting.views import app, db


class TestFlaskReports(unittest.TestCase):

    def setUp(self):
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

        self.db_rs, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            load_db(file=abs_file_path)

    def tearDown(self):
        os.close(self.db_rs)
        os.unlink(app.config['DATABASE'])

    def test_loaded_db(self):
        index_page = self.app.get('/')
        headings = [b'Top 10 Shortages', b'Classification Breakdown',  b'Top 10 Shortages']
        for heading in headings:
            assert heading in index_page.data

    def test_inventory_analysis_api(self):
        inventory_analysis = self.app.get('/api/inventory_analysis')
        headings = [b'abc_xyz_classification', b'average_orders',  b'currency']
        print(inventory_analysis.data)
        for heading in headings:
            assert heading in inventory_analysis.data

    #def test_launch_report(self):
    #    launcher = tk.Tk()
    #    spawn = SupplychainpyReporting(launcher)
    #    with self.assertRaises(ValueError):
    #        spawn.spawn_reports()




