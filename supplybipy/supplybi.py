#!/usr/bin/env python3

import time

from build_model import analyse_orders_abcxyz_from_file, analyse_orders_from_file_row

__author__ = 'kevin'


def main():
    r = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
         'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}

    # start_time = time.time()
    # summary = model_orders(r, 'RX983-90', 3, 50.99, 400, 1.28)
    # print(summary)
    # end_time = time.time()
    # secs = end_time - start_time
    # print('model_orders took {} seconds to run', secs)

    # summary = analyse_orders_from_file_col('test.txt', 'RX9887-90', 4, 45, 400, 1.28)
    # print(summary)

    start_time = time.time()
    big_summary = analyse_orders_from_file_row('test_row_small.txt', 1.28, 400)
    print(big_summary)
    end_time = time.time()
    secs = end_time - start_time
    print('model_orders took {} seconds to run', secs)

    start_time = time.time()
    abc = analyse_orders_abcxyz_from_file('test_row_small.txt', 1.28, 400)
    for sku in abc:
        print(sku.eoq.economic_order_quantity)
    end_time = time.time()
    secs = end_time - start_time
    print('model_orders took {} seconds to run', secs)



if __name__ == '__main__': main()
