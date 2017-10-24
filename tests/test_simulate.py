import os
import re
from unittest import TestCase
import unittest
from decimal import Decimal

import logging

from supplychainpy import simulate
from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
from supplychainpy.sample_data.config import ABS_FILE_PATH
from supplychainpy.simulate import summarise_frame

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestSimulate(TestCase):
    """ Test for simulation logic"""

    def setUp(self):
        self.__skus = ['KR202-209', 'KR202-210', 'KR202-211']

        self.__orders_analysis = analyse_orders_abcxyz_from_file(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                                                 z_value=Decimal(1.28),
                                                                 reorder_cost=Decimal(5000),
                                                                 file_type="csv",
                                                                 length=12)
        self.sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis, runs=1, period_length=12)

    # if backlog is zero then shortage cost is zero as well
    def test_shortage_cost_zero(self):
        """ Ensures that there is 0 shortage cost when a backlog has not been recorded."""

        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis,
                                       runs=10, period_length=12)
        for period in sim[0]:
            if int(period[0].get("backlog")) == 0:
                self.assertEqual(int(period[0].get("shortage_cost")), 0)

    def test_shortage_cost(self):
        """ Test shortage cost when a backlog has been recorded. """

        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis, runs=1, period_length=12)
        for period in sim[0]:
            if int(period[0].get("shortage_cost")) > 0:
                self.assertGreater(int(period[0].get("backlog")), 0)

    def test_po_quantity_zero(self):
        """Ensures a purchase order is raised if the closing stock is 0. """

        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis, runs=1, period_length=12)
        for period in sim[0]:
            if int(period[0].get("closing_stock")) == 0:
               # print(period[0].get("po_quantity"))
                self.assertGreater(int(period[0].get("po_quantity")), 0)



    def test_po_raised_regex(self):

        po_regex = re.compile('[P][O] \d+')

        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis, runs=1, period_length=12)
        for period in sim[0]:
            if int(period[0].get("closing_stock")) == 0 and int(period[0].get("backlog")) > 0:
                self.assertRegex(period[0].get("po_raised"), expected_regex=po_regex, msg='True')


    def test_backlog(self):
        for period in self.sim[0]:
            if int(period[0].get("backlog")) < 0 and int(period[0].get("closing_stock")) == 0:
                backlog =(int(period[0].get("opening_stock")) + int(period[0].get("delivery"))) - int(period[0].get("demand"))
                self.assertAlmostEqual(int(period[0].get("backlog")),backlog,delta=1)

    def quick_test(self):
        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis,
                                       runs=100, period_length=12)
        sim_window = simulate.summarize_window(simulation_frame=sim, period_length=12)

        #for item in sim:
        #    for s in item:
        #        if s[0].get('sku_id')=='KR202-209':
        #            print(s)
        #print(sim_window)
        frame_summary = simulate.summarise_frame(sim_window)
        #print(frame_summary)
        #for item in frame_summary:
        #    if item.get('sku_id')=='KR202-209':
        #        print(item)
        print(frame_summary)

if __name__ == "__main__":
    unittest.main()
