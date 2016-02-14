##!/usr/bin/env python3

import time
from decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy.model_inventory import analyse_orders_abcxyz_from_file, analyse_orders_from_file_row, analyse_orders, \
    analyse_orders_from_file_col, analyse_orders_np
from supplychainpy.demand import summarise_demand
from supplychainpy.demand import forecast_demand
from supplychainpy.enum_formats import PeriodFormats
import numpy as np
from supplychainpy.model_inventory import analyse_orders

__author__ = 'kevin'


def main():
    # end_time = time.time()
    # secs = end_time - start_time
    # print("model_orders took {:.5f} seconds to run".format(secs))
    # summary = analyse_orders_from_file_col('test.txt', 'RX9887-90', 4, 45, 400, 1.28)
    # print(summary)
    # start_time = time.time()
    # big_summary = analyse_orders_from_file_row('data.csv', 1.28, 400, file_type="csv")
    # print(big_summary)
    # end_time = time.time()
    # secs = end_time - start_time
    # print('model_orders took {:.5f} seconds to run'.format(secs))
    # start_time = time.time()
    # abc = analyse_orders_abcxyz_from_file('data.csv', 1.28, 5000, file_type="csv")
    # for sku in abc.orders:
    #     print(sku.orders_summary())
    # print(abc.abcxyz_summary)
    # end_time = time.time()
    # secs = end_time - start_time
    # print('model_orders took {:.5f} seconds to run'.format(secs))
    # orders = [1, 3, 5, 67, 4, 65, 242, 50, 48, 24, 34, 20]
    # orders2 = [4, 5, 7, 33, 45, 53, 55, 35, 53, 53, 43, 34]
    # weights = [.3, .5, .2]
    #  d = forecast_demand.Forecast(orders)
    # print(d.calculate_moving_average_forecast(forecast_length=6, base_forecast=True, start_position=1))
    # k = forecast_demand.Forecast(orders2)
    # k.calculate_moving_average_forecast(forecast_length=6)
    # moving_average = d.moving_average_forecast
    # moving_average2 = k.moving_average_forecast
    # result_array = k.calculate_mean_absolute_deviation(moving_average, orders2, base_forecast=True)
    # print(result_array)
    #s = np.array([200, 300, 343, 553, 356, 455, 264, 252, 264, 635, 677, 755, 887])
    #analyse_orders_np(unit_cost=300, period=PeriodFormats.months.name, z_value=1.28, orders=s, lead_time=9.00)
    yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
                      'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}

    summary = model_inventory.analyse_orders(yearly_demand, 'RX983-90', 3, 50.99, 400, 1.28)

    print(summary)

if __name__ == '__main__': main()
