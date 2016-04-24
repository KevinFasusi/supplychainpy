import os
import re
from unittest import TestCase
from decimal import Decimal

from supplychainpy import simulate
from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file


class TestSimulate(TestCase):
    # if backlog is zero then shortage cost is zero as well
    def test_shortage_cost_zero(self):

        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'

        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

        orders_analysis = analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                          reorder_cost=Decimal(5000), file_type="csv")

        sim = simulate.run_monte_carlo(orders_analysis=orders_analysis,
                                       runs=1, period_length=12)
        for period in sim:
            if int(period[0].get("backlog")) == 0:
                self.assertEqual(int(period[0].get("shortage_cost")), 0)

                # if shortage_cost is zero then backlog should be zero
                # def test_backlog_cost_zero(self):

                #     app_dir = os.path.dirname(__file__, )
                #     rel_path = 'supplychainpy/data.csv'
                #     abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

                #     sim = simulate.run_monte_carlo(file_path=abs_file_path, z_value=Decimal(1.28), runs=3,
                #                                    reorder_cost=Decimal(4000), file_type="csv", period_length=12)
                #     for period in sim:
                #         print(period)
                #         if int(period[0].get("shortage_cost")) == 0:
                #             self.assertEqual(int(period[0].get("backlog")), 0)

    # if shortage_cost greater than zero the back must also be greater than zero
    def test_shortage_cost(self):

        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

        orders_analysis = analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                          reorder_cost=Decimal(5000), file_type="csv")

        sim = simulate.run_monte_carlo(orders_analysis=orders_analysis, runs=1, period_length=12)
        for period in sim:
            if int(period[0].get("shortage_cost")) > 0:
                self.assertGreater(int(period[0].get("backlog")), 0)

    # if closing stock is zero then po_quantity is greater than zero
    def test_po_quantity_zero(self):

        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

        orders_analysis = analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                          reorder_cost=Decimal(5000), file_type="csv")

        sim = simulate.run_monte_carlo(orders_analysis=orders_analysis, runs=1, period_length=12)
        for period in sim:
            if int(period[0].get("closing_stock")) == 0:
                self.assertGreater(int(period[0].get("po_quantity")), 0)

    # po not raised in first period
    def test_po_raised_regex(self):

        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

        po_regex = re.compile('[P][O] \d+')
        orders_analysis = analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                          reorder_cost=Decimal(5000), file_type="csv")

        sim = simulate.run_monte_carlo(orders_analysis=orders_analysis, runs=1, period_length=12)
        for period in sim:
            if int(period[0].get("closing_stock")) == 0 and int(period[0].get("backlog")) > 0:
                self.assertRegex(period[0].get("po_raised"), expected_regex=po_regex, msg='True')
