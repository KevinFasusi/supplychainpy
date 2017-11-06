import logging
import unittest
from unittest import TestCase

from supplychainpy._helpers import _data_cleansing
from supplychainpy.model_demand import holts_trend_corrected_exponential_smoothing_forecast, \
    simple_exponential_smoothing_forecast
from supplychainpy.model_demand import holts_trend_corrected_exponential_smoothing_forecast_from_file
from supplychainpy.model_demand import simple_exponential_smoothing_forecast_from_file
from supplychainpy.sample_data.config import ABS_FILE_PATH

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

class TestModelDemand(TestCase):
    def setUp(self):
        self._data_set = {'jan': 25, 'feb': 25, 'mar': 25, 'apr': 25, 'may': 25, 'jun': 25, 'jul': 75,
                          'aug': 75, 'sep': 75, 'oct': 75, 'nov': 75, 'dec': 75}

        self._orders = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147, 188, 161, 162,
                        169, 185, 188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218, 264, 304]

        self.ses_components = [
            'mape',
            'regression',
            'forecast',
            'forecast_breakdown',
            'alpha',
            'statistics',
            'standard_error',
            'optimal_alpha'
        ]
        with open(ABS_FILE_PATH['COMPLETE_CSV_XSM'], 'r') as raw_data:
            self.item_list = _data_cleansing.clean_orders_data_row_csv(raw_data, length=12)
        self.sku_id = []

        for sku in self.item_list:
            self.sku_id.append(sku.get("sku_id"))



    def test_simple_exponential_smoothing_forecast_trend(self):

        self.ses_forecast = [i for i in
                             simple_exponential_smoothing_forecast_from_file(
                                 file_path=ABS_FILE_PATH['COMPLETE_CSV_XSM'],
                                 file_type='csv',
                                 length=12,
                                 smoothing_level_constant=0.5,
                                 optimise=True)]

        self.keys = [list(i.keys()) for i in self.ses_forecast]
        self.unpack_keys = [i[0] for i in self.keys]
        for key in self.sku_id:
            self.assertIn(key, self.unpack_keys)

        trending = [list(i.values()) for i in self.ses_forecast]
        unpack_trending = [i[0] for i in trending]
        stats = []
        for i in unpack_trending:
            stats.append(i.get('statistics'))
        for stat in stats:
            if stat.get('trend'):
                self.assertTrue(stat.get('pvalue') < 0.05)

    def test_holts_trend_corrected_exponential_smoothing(self):

        self.htces_forecast = [i for i in
                               holts_trend_corrected_exponential_smoothing_forecast_from_file(
                                   file_path=ABS_FILE_PATH['COMPLETE_CSV_XSM'],
                                   file_type='csv',
                                   length=12,
                                   alpha=0.5,
                                   gamma=0.5,
                                   smoothing_level_constant=0.5,
                                   optimise=True)]


        holts_trend_corrected_esf = holts_trend_corrected_exponential_smoothing_forecast(demand=self._orders,
                                                                                         alpha=0.5,
                                                                                         gamma=0.5,
                                                                                         forecast_length=6,
                                                                                         initial_period=18,
                                                                                         optimise=False)

        self.assertEqual(281, round(holts_trend_corrected_esf.get('forecast')[0]))
        self.assertEqual(308, round(holts_trend_corrected_esf.get('forecast')[1]))
        self.assertEqual(334, round(holts_trend_corrected_esf.get('forecast')[2]))

        self.keys = [list(i.keys()) for i in self.htces_forecast]
        self.unpack_keys_htces = [i[0] for i in self.keys]

        for key in self.sku_id:
            self.assertIn(key, self.unpack_keys_htces)

        for i in self.htces_forecast:
            for k in i.values():
                self.assertGreater(k.get('original_standard_error'), k.get('standard_error'))

    def test_simple_exponential_smoothing_key(self):
        ses = simple_exponential_smoothing_forecast(demand=self._orders, alpha=0.5, forecast_length=6, initial_period=18)
        for k in ses:
            self.assertIn(k, self.ses_components)

if __name__ == "__main__":
    unittest.main()