import re
from unittest import TestCase

import logging

import os
from flask import Flask

from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._db_connection import database_connection_uri
from supplychainpy._helpers._pickle_config import serialise_config
from supplychainpy.bot._controller import excess_controller, shortage_controller, revenue_controller, \
    inventory_turns_controller, average_orders_controller, safety_stock_controller, reorder_level_controller
from supplychainpy.launch_reports import load_db
from supplychainpy.reporting.config.settings import IntegrationConfig
from supplychainpy.reporting.extensions import db
from supplychainpy.sample_data.config import ABS_FILE_PATH

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


class TestBotController(TestCase):

    def test_controllers(self):
        app = Flask(__name__, instance_relative_config=True)
        PWD = os.path.abspath(os.curdir)
        i_c = IntegrationConfig
        i_c.SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/reporting.db'.format(PWD)
        app.config.from_object(i_c)
        print('\n\n\n', PWD,'\n\n\n')
        app.config['DATABASE'] = PWD
        app.config['TESTING'] = True
        self.app = app.test_client()
        self._file= ABS_FILE_PATH['COMPLETE_CSV_XSM']
        app_settings = {
            'file': self._file,
            'currency': 'USD',
            'database_path': PWD,
        }

        serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
        with app.app_context():
            db.init_app(app)
            db.create_all()
            load_db(file=self._file, location=PWD)

        smallest_excess = excess_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
        largest_excess = excess_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
        smallest_shortage = shortage_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
        largest_shortage = shortage_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
        smallest_revenue = revenue_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
        largest_revenue = revenue_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
        smallest_inventory_turns = inventory_turns_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
        largest_inventory_turns = inventory_turns_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
        smallest_average_orders = average_orders_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
        biggest_average_orders = average_orders_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
        smallest_safety_stock =  safety_stock_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
        biggest_safety_stock = safety_stock_controller(database_connection_uri(retrieve='retrieve'), direction='biggest`')
        smallest_reorder_level = reorder_level_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
        biggest_reorder_level = reorder_level_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')

        result = [smallest_average_orders, smallest_excess, largest_excess, smallest_shortage, largest_shortage,
                  smallest_revenue, largest_revenue, smallest_inventory_turns, largest_inventory_turns,
                  biggest_average_orders, smallest_safety_stock, biggest_safety_stock, smallest_reorder_level,
                  biggest_reorder_level]

        ses_file_regex = re.compile('\w+[-]\d+')
        for i in result:
            self.assertTrue(ses_file_regex.match(i[1]))

