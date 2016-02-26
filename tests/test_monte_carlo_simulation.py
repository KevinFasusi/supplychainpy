import os
from unittest import TestCase
import numpy as np
from decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy.simulations import monte_carlo


class TestMonteCarlo(TestCase):
    def test_normal_distribution_mean(self):
        """ Verifies mean and variance for random normal distribution.
        """
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                                          z_value=Decimal(1.28),
                                                                          reorder_cost=Decimal(5000),
                                                                          file_type="csv")

        sim = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders, period_length=1)
        for sku in orders_analysis.orders:
            item = sku.orders_summary()
            if item['sku'] == 'KR202-209':
                # assert
                self.assertLess(
                    abs(float(item['average_order']) - np.mean(sim.normal_random_distribution[0]['KR202-209'][0][0])),
                    float(item['standard_deviation']))

    def test_normal_distribution_variance(self):
        """ Verifies mean and variance for random normal distribution.
        """
        # arrange
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        # act
        orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                                          z_value=Decimal(1.28),
                                                                          reorder_cost=Decimal(5000),
                                                                          file_type="csv")

        sim = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders, period_length=1)

        for sku in orders_analysis.orders:
            item = sku.orders_summary()
            if item['sku'] == 'KR202-209':
                self.assertEqual(
                    abs(Decimal(item['standard_deviation']) - Decimal(
                        np.std(sim.normal_random_distribution[0]['KR202-209'][0][0],
                               ddof=1))), Decimal(item['standard_deviation']))