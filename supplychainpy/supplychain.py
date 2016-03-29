#!/usr/bin/env python3
import os
from _decimal import Decimal

import time

from supplychainpy import simulate
from supplychainpy import model_inventory

__author__ = 'kevin'


def main():
    start_time = time.time()

    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path="data.csv", z_value=1.28,
                                                                      reorder_cost=5000, file_type="csv")

    # print(orders_analysis.abcxyz_summary)

    # for sku in orders_analysis.orders:
    #    print('Sku: {} Economic Order Quantity: {:.0f} Sku Revenue: {:.0f} ABCXYZ Classification: {}'.format(sku.sku_id,
    #                                                                                                         sku.economic_order_qty,
    #                                                                                                         sku.revenue,
    #                                                                                                        sku.abcxyz_classification))

    # for sku in orders_analysis.orders:
    #    print(sku.orders_summary())
    #
    # end_time = time.time()
    # end_secs = end_time - start_time
    # print(end_secs)

    sim = simulate.run_monte_carlo(orders_analysis=orders_analysis.orders, file_path="data.csv", z_value=Decimal(1.28),
                                   runs=100,
                                   reorder_cost=Decimal(4000), file_type="csv", period_length=12)

    # inter_time = time.time()
    # secs = inter_time - start_time
    # print(secs)
    #
    sim_window = simulate.summarize_window(simulation_frame=sim, period_length=12)

    sim_frame = simulate.summarise_frame(sim_window)

    for sku in sim_frame:
        print(sku)

    end_time = time.time()
    end_secs = end_time - start_time
    print(end_secs)

    optimised = simulate.optimise_service_level(service_level=95.0, frame_summary=sim_frame,
                                                orders_analysis=orders_analysis.orders, runs=100)

    # end_time = time.time()
    # end_secs = end_time - start_time
    # print(end_secs)


if __name__ == '__main__': main()
