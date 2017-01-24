import os
from decimal import Decimal
from unittest import TestCase

import logging
import numpy as np

from supplychainpy import model_inventory
from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file
from supplychainpy.sample_data.config import ABS_FILE_PATH
from supplychainpy.simulations import monte_carlo
from supplychainpy import simulate
from supplychainpy.simulations.simulation_frame_summary import MonteCarloFrameSummary

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TestMonteCarlo(TestCase):
    """Tests the the monte carlo computations. """

    def setUp(self):
        self.__skus = ['KR202-209', 'KR202-210', 'KR202-211']

        self.__orders_analysis = analyse_orders_abcxyz_from_file(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
                                                                 z_value=Decimal(1.28),
                                                                 reorder_cost=Decimal(5000),
                                                                 file_type="csv",
                                                                 length=12)

        self.__sim = monte_carlo.SetupMonteCarlo(analysed_orders=self.__orders_analysis,
                                                 period_length=1)

        # def test_normal_distribution_mean(self):
        #    """ Verifies mean and variance for random normal distribution.
        #    """

    #
    #    for sku in self.__orders_analysis:
    #        item = sku.orders_summary()
    #        if item['sku'] == 'KR202-209':
    #            # assertd
    #            diff = abs(
    #                float(item['average_orders']) - float(
    #                    np.mean(self.__sim.normal_random_distribution[0]['KR202-209'][0][0])))
    #            print(item['average_orders'], float(np.mean(self.__sim.normal_random_distribution[0]['KR202-209'][0][0])),
    #                   diff, float(item['standard_deviation']))
    #            self.assertLess(diff, float(item['standard_deviation']))

    def test_demand_is_normally_distibuted(self):

        random_demand = [demand.get('KR202-209') for demand in self.__sim.normal_random_distribution][0][0][0]
        average_orders = [orders.orders_summary() for orders in self.__orders_analysis][0]['average_orders']
        standard_deviation = [orders.orders_summary() for orders in self.__orders_analysis][0]['standard_deviation']
        # print(standard_deviation, average_orders, random_demand)
        z_value = (random_demand - float(average_orders)) / float(standard_deviation)
        # print(z_value)

    def test_run_simulation(self):

        simulation_windows = simulate.run_monte_carlo(orders_analysis=self.__orders_analysis, runs=1)

        self.assertEqual(len(simulation_windows), 468)

    def test_summarize_simulation(self):
        orders_analysis = analyse_orders_abcxyz_from_file(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'], z_value=Decimal(1.28),
                                                          reorder_cost=Decimal(5000), file_type="csv")

        simulation_windows = simulate.run_monte_carlo(orders_analysis=orders_analysis, runs=1, period_length=12)
        collect_sim = []
        for i in simulate.summarize_window(simulation_frame=simulation_windows):
            collect_sim.append(i)
        self.assertEqual(len(collect_sim), 39)

    def test_build_window(self):
        sim_dict = {}
        period_length = 12
        sim_collection = []
        for k in range(0, 1):
            simulation = monte_carlo.SetupMonteCarlo(analysed_orders=self.__orders_analysis)
            random_demand = simulation.generate_normal_random_distribution(period_length=period_length)
            for sim_window in simulation.build_window(random_normal_demand=random_demand, period_length=period_length):
                sim_dict = {"index": "{:.0f}".format(sim_window.index), "period": "{:.0f}".format(sim_window.position),
                            "sku_id": sim_window.sku_id, "opening_stock": "{:.0f}".format(sim_window.opening_stock),
                            "demand": "{:.0f}".format(sim_window.demand),
                            "closing_stock": "{:.0f}".format(sim_window.closing_stock),
                            "delivery": "{:.0f}".format(sim_window.purchase_order_receipt_qty),
                            "backlog": "{:.0f}".format(sim_window.backlog)}
            sim_collection.append([sim_dict])
            self.assertEqual(len(sim_collection), 1)

    def test_closing_stock_stockout_err(self):

            simulation_frame = [23, 45]
            closing_stock = []
            summary = MonteCarloFrameSummary
            period_length = 12
            for x in range(1, len(simulation_frame)):
                for f in simulation_frame:
                    if int(f[0]['index']) == x:
                        closing_stock.append(int(f[0]['closing_stock']))
                    if len(closing_stock) == period_length:
                        cls = summary.closing_stockout_percentage(closing_stock=closing_stock,
                                                                  period_length=period_length)
                        summarize = {'sku_id': f[0]['sku_id'], 'stockout_percentage': cls, 'index': f[0]['index']}
                        yield summarize
                        closing_stock = []

                        # def test_normal_distribution_variance(self):
                        #     """ Verifies mean and variance for random normal distribution.
                        #    """
                        #     # arrange
                        #     app_dir = os.path.dirname(__file__, )
                        #     rel_path = 'supplychainpy/data.csv'
                        #     abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
                        #     # act
                        #     orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                        #                                                                       z_value=Decimal(1.28),
                        #                                                                       reorder_cost=Decimal(5000),
                        #                                                                       file_type="csv")
                        #
                        #     sim = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders, period_length=1)
                        #
                        #     for sku in orders_analysis.orders:
                        #         item = sku.orders_summary()
                        #         if item['sku'] == 'KR202-209':
                        #             self.assertLess(
                        #                 (abs(float(item['standard_deviation']) - float(
                        #                     np.std(sim.normal_random_distribution[0]['KR202-209'][0][0],ddof=0)))), Decimal(item['standard_deviation']))
