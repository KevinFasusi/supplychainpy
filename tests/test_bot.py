import os
import tempfile
from unittest import TestCase

import logging

from flask import Flask

from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import serialise_config
from supplychainpy.bot.dash import ChatBot
from supplychainpy.launch_reports import load_db
from supplychainpy.reporting.config.settings import ProdConfig, DevConfig, IntegrationConfig
from supplychainpy.reporting.extensions import db
from supplychainpy.sample_data.config import ABS_FILE_PATH

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


#class TestBot(TestCase):
#    def setUp(self):
#        self.__dude = ChatBot()
#        self.__SALUTATION_RESPONSES = ["hi", "hello", "how's tricks?"]
#        app = Flask(__name__, instance_relative_config=True)
#        PWD = os.path.abspath(os.curdir)
#        i_c = IntegrationConfig
#        i_c.SQLALCHEMY_DATABASE_URI ='sqlite:///{}/reporting.db'.format(PWD)
#        app.config.from_object(i_c)
#
#        app.config['DATABASE'] = PWD
#        app.config['TESTING'] = True
#        self.app = app.test_client()
#
#        file_path = ABS_FILE_PATH['COMPLETE_CSV_XSM']
#        app_settings = {
#            'file': file_path,
#            'currency': 'USD',
#            'database_path': PWD,
#        }
#        serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)
#        with app.app_context():
#            db.init_app(app)
#            db.create_all()
#            load_db(file=file_path,location=PWD)
#
#    def test_chat_bot(self):
#        greeting1 = self.__dude.chat_machine("hello")[0]
#        self.assertIn(*greeting1, self.__SALUTATION_RESPONSES)
#        #print(self.__dude.chat_machine("show KR202-214")[0])
#        #self.assertEqual('<a href="/sku_detail/36">Here you go!</a>', self.__dude.chat_machine("show KR202-244")[0])
#        #self.assertIn('SKU KR202-247', *self.__dude.chat_machine("what is the biggest shortage?")[0])
#        #self.assertIn('SKU KR202-247', *self.__dude.chat_machine("what is the biggest excess?")[0])
#        #self.assertIn('SKU KR202-235', *self.__dude.chat_machine("what is the biggest revenue?")[0])
#        #self.assertIn('SKU KR202-212', *self.__dude.chat_machine("what is the smallest revenue?")[0])
#        #self.assertIn('SKU KR202-245', *self.__dude.chat_machine("what is the smallest excess?")[0])
#        #self.assertIn('SKU KR202-213', *self.__dude.chat_machine("Which SKU has the smallest average order?")[0])
#        #self.assertIn('SKU KR202-241', *self.__dude.chat_machine("Which SKU has the greatest safety stock?")[0])