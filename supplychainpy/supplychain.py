##!/usr/bin/env python3
import os
from _decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy.simulations import monte_carlo

__author__ = 'kevin'


def main():
    app_dir = os.path.dirname(__file__, )
    rel_path = 'supplychainpy/data.csv'
    abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                                      z_value=Decimal(1.28),
                                                                      reorder_cost=Decimal(5000),
                                                                      file_type="csv")

    simulation = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders)
    random_demand = simulation.generate_normal_random_distribution(period_length=2)
    simulation.build_window(random_normal_demand=random_demand, period_length=2)


    list_random_orders = []
    #for i in range(0, 10):
    #    simulation = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders)
    #    list_random_orders.append(simulation.normal_random_distribution#)
    #    del simulation
    # each sku in the csv file has generated a random normally distributed order for the simulation. A list is prefered
    # the order is preserved.
    #rnd_order=[]
    #by_sku = {}
    #for r in orders_analysis.orders:
    #    for item in list_random_orders:
    #        for t in item:
    #                rnd_order.append([t[r.sku_id]])
    #        by_sku[r.sku_id] = rnd_order
    #



if __name__ == '__main__': main()
