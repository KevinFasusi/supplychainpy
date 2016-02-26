##!/usr/bin/env python3
import os
from _decimal import Decimal

from supplychainpy import simulate

__author__ = 'kevin'


def main():
    simulation = simulate.run_monte_carlo(file_path="data.csv", z_value=Decimal(1.28), runs=1,
                                          reorder_cost=Decimal(4000), file_type="csv")



if __name__ == '__main__': main()
