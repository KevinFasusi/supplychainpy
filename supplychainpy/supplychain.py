#!/usr/bin/env python3
import os
from decimal import Decimal
from supplychainpy.demand.summarise import SKU
import time

from supplychainpy import simulate
from supplychainpy import model_inventory

__author__ = 'kevin'


def main():
    start_time = time.time()

    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=Decimal(1.28),
                                                                      reorder_cost=Decimal(5000), file_type="csv",
                                                                      length=12)

    for order in orders_analysis.orders:
        print(order.orders_summary())

    sim = simulate.run_monte_carlo(orders_analysis=orders_analysis.orders, runs=30, period_length=12)

    sim_window = simulate.summarize_window(simulation_frame=sim, period_length=12)

    sim_frame= simulate.summarise_frame(sim_window)

   # optimised_orders = simulate.optimise_service_level(service_level=95.0, frame_summary=sim_frame,
    #                                          orders_analysis=orders_analysis.orders, runs=100, percentage_increase=1.30)
    end = time.time()

    secs = end -start_time
    print(secs)
if __name__ == '__main__':
    main()
