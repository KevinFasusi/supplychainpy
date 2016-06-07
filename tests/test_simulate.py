import os
import re
from unittest import TestCase
from decimal import Decimal

from supplychainpy import simulate
from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file


class TestSimulate(TestCase):
    """ Test for simulation logic"""

    def setUp(self):
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

        self.__skus = ['KR202-209', 'KR202-210', 'KR202-211']

        self.__orders_analysis = analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                                 z_value=Decimal(1.28),
                                                                 reorder_cost=Decimal(5000),
                                                                 file_type="csv",
                                                                 length=12)

    # if backlog is zero then shortage cost is zero as well
    def test_shortage_cost_zero(self):

        """ Ensures that there is 0 shortage cost when a backlog has not been recorded."""

        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis,
                                       runs=1, period_length=12)
        for period in sim:
            print(period)
            if int(period[0].get("backlog")) == 0:
                self.assertEqual(int(period[0].get("shortage_cost")), 0)

    def test_shortage_cost(self):

        """ Test shortage cost when a backlog has been recorded. """

        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis, runs=1, period_length=12)
        for period in sim:
            if int(period[0].get("shortage_cost")) > 0:
                self.assertGreater(int(period[0].get("backlog")), 0)

    def test_po_quantity_zero(self):

        """Ensures a purchase order is raised if the closing stock is 0. """

        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis, runs=1, period_length=12)
        for period in sim:
            if int(period[0].get("closing_stock")) == 0:
                print(period[0].get("po_quantity"))
                self.assertGreater(int(period[0].get("po_quantity")), 0)



    def test_po_raised_regex(self):

        po_regex = re.compile('[P][O] \d+')

        sim = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis, runs=1, period_length=12)
        for period in sim:
            if int(period[0].get("closing_stock")) == 0 and int(period[0].get("backlog")) > 0:
                self.assertRegex(period[0].get("po_raised"), expected_regex=po_regex, msg='True')
