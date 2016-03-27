#!/usr/bin/env python3
import os
from _decimal import Decimal

import time

from supplychainpy import simulate

__author__ = 'kevin'


def main():
    start_time = time.time()
    sim = simulate.run_monte_carlo(file_path="data.csv", z_value=Decimal(1.28), runs=1,
                                   reorder_cost=Decimal(4000), file_type="csv", period_length=12)
    for line in sim:
        print(line)

    inter_time = time.time()
    secs = inter_time - start_time
    print(secs)

    i = simulate.summarize_window(simulation_frame=sim, period_length=12)
    #for r in i:
    #    print(r)

    a = simulate.summarise_frame(i)
    for s in a:
       print(s)

    end_time = time.time()
    end_secs = end_time - start_time
    print(end_secs)


if __name__ == '__main__': main()
