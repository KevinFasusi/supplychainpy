#!/usr/bin/env python3
import os
from _decimal import Decimal

import time

from supplychainpy import simulate, model_inventory

__author__ = 'kevin'


def main():
    # start_time = time.time()
    # sim = simulate.run_monte_carlo(file_path="data.csv", z_value=Decimal(1.28), runs=42,
    #                                reorder_cost=Decimal(4000), file_type="csv", period_length=12)
    # for s in sim:
    #     print(s)
    # inter_time = time.time()
    # secs = inter_time - start_time

    # print(secs)
    # i = simulate.run(simulation_frame=sim, period_length=12)
    # for r in i:
    #     print(r)
    # end_time = time.time()
    # end_secs = end_time - start_time
    # print(end_secs)

    app_dir = os.path.dirname(__file__, )
    rel_path = 'supplychainpy/data.csv'
    abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
    # act
    abc = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                          reorder_cost=Decimal(400), file_type="csv")
    for sku in abc.orders:
        print(sku.orders_summary())

  #  d = {}
   # for x in model_inventory.summarise_analysis(abcxyz=abc, qauntity_on_hand=d):
    #    print(x)


if __name__ == '__main__': main()
