# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import time
from decimal import Decimal
import logging

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.mlab as mlab
from sklearn.datasets import fetch_california_housing
from sklearn.datasets import load_boston
from pandas import Series, DataFrame

# logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')
from supplychainpy import model_inventory
from supplychainpy._csv_management._model._db_setup import transaction_type, metadata
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG, \
    ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import deserialise_config
from supplychainpy.bi._analytical_heirachy_process import _PairwiseComparison
from supplychainpy.demand._forecast_demand import Forecast
from supplychainpy.model_demand import simple_exponential_smoothing_forecast, \
    holts_trend_corrected_exponential_smoothing_forecast_from_file
from supplychainpy.model_inventory import analyse, analyse_orders
from supplychainpy.sample_data.config import ABS_FILE_PATH
from supplychainpy.model_decision import analytical_hierarchy_process


def main():
    pass
    # pp = np.array([[1,2,7,9],[0.5,1,5.0,5.0],[0.1429,0.2,1.0,5.0],[0.1111, 0.2,  0.2, 1.0]])
    # sq = pp*pp
    # np.set_printoptions(precision=3, suppress=True)
    # print(sq)
    #lorry_cost = {'scania': 55000, 'iveco': 79000, 'volvo': 59000, 'navistar': 66000}
    #criteria = ('style', 'reliability', 'comfort', 'fuel_economy')
    #criteria_scores = [(1 / 1, 2 / 1, 7 / 1, 9 / 1), (1 / 2, 1 / 1, 5 / 1, 5 / 1), (1 / 7, 1 / 5, 1 / 1, 5 / 1),
    #                   (1 / 9, 1 / 5, 1 / 5, 1 / 1)]
#
    #options = ('scania', 'iveco', 'navistar', 'volvo' )
    #option_scores = {
    #    'style': [(1 / 1, 1 / 3, 5 / 1, 1 / 5), (3 / 1, 1 / 1, 2 / 1, 3 / 1), (1 / 3, 1 / 5, 1 / 1, 1 / 5),
    #              (5 / 1, 1 / 3, 5 / 1, 1 / 1)],
    #    'reliability': [(1 / 1, 1 / 3, 3 / 1, 1 / 7), (3 / 1, 1 / 1, 5 / 1, 1 / 5), (1 / 3, 1 / 5, 1 / 1, 1 / 5),
    #                    (7 / 1, 5 / 1, 5 / 1, 1 / 1)],
    #    'comfort': [(1 / 1, 5 / 1, 5 / 1, 1 / 7), (1 / 5, 1 / 1, 2 / 1, 1 / 7), (1 / 3, 1 / 5, 1 / 1, 1 / 5),
    #                (7 / 1, 7 / 1, 5 / 1, 1 / 1)],
    #    'fuel_economy': (11, 9, 10, 12)}
    #lorry_decision = analytical_hierarchy_process(criteria=criteria, criteria_scores=criteria_scores, options=options,
    #                                              option_scores=option_scores, quantitative_criteria=('fuel_economy',),
    #                                              item_cost=lorry_cost)
    #print(lorry_decision)
    # metadata.create_all(engine)
    ##print(deserialise_config(ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG),'\n')
    # print(deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG))
    # inventory_analysis = [i.orders_summary() for i in
    #                      model_inventory.analyse(file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
    #                                                                      z_value=Decimal(1.28),
    #                                                                      reorder_cost=Decimal(500),
    #                                                                      file_type='csv')]
    # print(inventory_analysis[0])
    #

    # raw_df = pd.read_csv(ABS_FILE_PATH['COMPLETE_CSV_SM'])
    # # print(raw_df)
    # analysis_df = analyse(df=raw_df, start=1, interval_length=12, interval_type='months')
    # # print(analysis_df[['sku', 'quantity_on_hand', 'excess_stock', 'shortages', 'ABC_XYZ_Classification']])


#
# row_ds = raw_df[raw_df['Sku'] == 'KR202-212'].squeeze()
# print(row_ds[1:12])
# d = simple_exponential_smoothing_forecast(ds=row_ds[1:12], length=12, smoothing_level_constant=0.5)
# print(d)
# htces_forecast = [i for i in holts_trend_corrected_exponential_smoothing_forecast_from_file(
#                           file_path=ABS_FILE_PATH['COMPLETE_CSV_SM'],
#                           file_type='csv',
#                           length=12,
#                           alpha=0.2,
#                           gamma=0.2,
#                           smoothing_level_constant=0.5,
#                           optimise=True)]
#
# for i in htces_forecast:
#    for k in i.values():
#        k.get('standard_error')
# start_time = time.time()
# app_dir = os.path.dirname(__file__, )
# rel_path = 'supplychainpy/data_col.csv'
# abs_file_path = os.path.abspa§th(os.path.join(app_dir, '..', rel_path))

## orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
##                                                                z_value=Decimal(1.28),
###                                                                reorder_cost=Decimal(5000),
##                                                                file_type="csv", length=12)
## for i in orders_analysis:
##    print(i.orders_summary())

## ia = [analysis.orders_summary() for analysis in
##      model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
##                                                      reorder_cost=Decimal(5000), file_type="csv",
##                                                      length=12)]

# orders = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147, 188, 161, 162, 169, 185,
#          188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218, 264, 304]
#
# total_orders = 0
# avg_orders = 0
#
# for order in orders[:12]:
#    total_orders += order
#
# avg_orders = total_orders / 12
# f = Forecast(orders)
# alpha = [0.2, 0.3, 0.4, 0.5, 0.6]
# s = [i for i in f.simple_exponential_smoothing(*alpha)]
#   p = [i for i in f.holts_trend_corrected_exponential_smoothing(0.5, 0.5, 155.88, 0.8369)]
#   print(p)
# holts_forecast = f.holts_trend_corrected_forecast(forecast=p, forecast_length=4)
# print(holts_forecast)
##sas = holts_trend_corrected_exponential_smoothing_forecast(orders,0.5,0.5,forecast_length=4, initial_period=18,
##                                                           optimise=True)
##print(sas)
##sum_squared_error = f.sum_squared_errors(p, 0.5)
##print(sum_squared_error)
# sum_squared_error = f.sum_squared_errors(s, 0.5)
# standard_error = f.standard_error(sum_squared_error, len(orders), 0.5, 2)
# print(standard_error)
# standard_error = f.standard_error(sum_squared_error, len(orders), 0.5)
#
# evo_mod = OptimiseSmoothingLevelGeneticAlgorithm(orders=orders,
#                                                 average_order=avg_orders,
#                                                 population_size=10,
#                                                 standard_error=standard_error,
#                                                 recombination_type='single_point')
#
# optimal_alpha = evo_mod.initial_population(individual_type='htces')
#
# print(optimal_alpha)
# forecast = [i for i in f.simple_exponential_smoothing(optimal_alpha[1])]
# s = LinearRegression(forecast)
# w = s.least_squared_error()
# mape = f.mean_aboslute_percentage_error_opt(forecast)
# sim = evo_mod.simple_exponential_smoothing_evo(0.5, 12, 'two_point')
# print(sim)
## evo_mod.run_smoothing_level_evolutionary_algorithm(parents=evo_mod.initial_population,

#                                                  standard_error=standard_error,
#                                                  smoothing_level=0.5)

# print([i['orders'].values() for i in ia])
# orders = [i['orders'].values() for i in ia]
# orders1 = [i for i in orders[0]]
# orders2 = [i for i in orders1[0]]
# vector = np.array(orders2)
##print(vector)
# row_vector = vector.reshape((12, 1))
# #print(row_vector)
# column_vector = vector.reshape((1, 12))
# #print(column_vector)
# single_feature_matrix = vector.reshape((1, 12))
# print(single_feature_matrix)
# pd_data = pd.Series(orders2, name='orders')
# print(pd_data)
# mean_expected_value = np.mean(pd_data)

# print(pd_data[0])

# squared_errors_pd = pd.Series(mean_expected_value - pd_data[0])  **2

# print(pd_data)
# print(np.mean(pd_data))
# pd.set_option('display.float_format', lambda x: '%.3f' % x)
# dataset = pd.DataFrame(data=row_vector)
# print(dataset[0].mean())
#
# mean_expected_value = dataset.mean()
#
##squared_error =  pd.Series([mean_expected_value - (x ** 2) for x in dataset[0].astype(float)])
## print(squared_error)
# boston = load_boston()
##california = fetch_california_housing()
# dataset2 = pd.DataFrame(boston.data, columns=boston.feature_names)
# dataset2['target'] = boston.target
# print(dataset2['target'])
##print(dataset2['target'].mean())
# squared_error =  pd.Series(mean_expected_value - dataset['target']) ** 2
# print(squared_error)
# sse = sum(squared_error)
# density_plot = squared_error.plot('hist')
##mean_expected_value = np.mean(dataset2)
##print(mean_expected_value)
#
## launch_report()
# analysis_summary = OrdersAnalysis(analysed_orders=orders_analysis)
# skus = ['KR202-209', 'KR202-210', 'KR202-211']

# skus_description = [summarised for summarised in analysis_summary.describe_sku(*[i['sku'] for i in ia])]
# print(skus_description)

# top_ten_shortages = [item for item in analysis_summary.rank_summary(attribute="shortages", count=10, reverse=True)]

# print(top_ten_shortages)

# simple_forecast  = {analysis.sku_id: analysis.simple_exponential_smoothing_forecast for analysis in
#       model_inventory.analyse_orders_abcxyz_from_file(file_path="data2.csv", z_value=Decimal(1.28),
#                                                       reorder_cost=Decimal(5000), file_type="csv",
#                                                       length=12)}


#
# for p, i in enumerate(simple_forecast, 1):
#    print(simple_forecast.get(i)['forecast'][p-1])

# holts_forecast = {analysis.sku_id: analysis.holts_trend_corrected_forecast for analysis in
#                 model_inventory.analyse_orders_abcxyz_from_file(file_path="data2.csv", z_value=Decimal(1.28),
#                                                                  reorder_cost=Decimal(5000), file_type="csv",
#                                                                length=12)}

# ses_forecast = {analysis.sku_id: analysis.simple_exponential_smoothing_forecast for analysis in
#                 model_inventory.analyse_orders_abcxyz_from_file(file_path="data2.csv", z_value=Decimal(1.28),
#                                                                 reorder_cost=Decimal(5000), file_type="csv",
#                                                                  length=12)}

# for i in holts_forecast:
#   print(holts_forecast.get(i))

# for i in holts_forecast:
#    for g in holts_forecast.get(i)['forecast_breakdown']:
#        print(g)

# for orders in inventory_analysis:
#  print(orders)


#
# summary = OrdersAnalysis(analysed_orders=inventory_analysis)
# abc_raw = summary.abc_xyz_raw
# print(abc_raw.ay)
#
# for analysis in summary.abc_xyz_summary():
#    print(analysis.get("AX"))  # print(analysis.get("AX")["revenue"] for entering cell
#
# ar = [analysis.get("AZ")['revenue'] for analysis in summary.abc_xyz_summary() if analysis.get("AZ")]
# print(ar)
#
# ax_d = abc_raw.ay
#
# for sku in ax_d:
#    print("stuff", sku.get("safety_stock"))
#
# print("AX stuff", ax_d)
#
## for top_shortages in summary.top_sku(attribute="shortages", count=10, reverse=False):
##    print(top_shortages)
## get sku keys from category analysis and unpack_sku_detail for describe sku
# questions = ['KR202-209', 'KR202-210', 'KR202-211']
# for summarised in summary.describe_sku('KR202-217'):
#    print(summarised)
##
# s = [summarised for summarised in summary.describe_sku('KR202-217')]
# print("\n", "new one", s)
##
#
# print("keys {}".format(list(ax_shortages.keys())))
# print("values {}".format(list(ax_shortages.values())))

# top_ten_shortages = [item for item in
#                     SKU(analysed_orders=orders_analysis.orders).top_sku(attribute="shortage", count=10,
#                                                                         reverse=True)]
#
# top_ten_excess = [item for item in
#                  SKU(analysed_orders=orders_analysis.orders).top_sku(attribute="excess_stock", count=10,
#                                                                      reverse=True)]
#
# for order in SKU(analysed_orders=orders_analysis.orders).top_sku(attribute="shortage", count=10, reverse=False):
#    print(order)
#
#
#

# sim_window = simulate.summarize_window(simulation_frame=sim, period_length=12)
#
# sim_frame = simulate.summarise_frame(sim_window)
#
# optimised_orders = simulate.optimise_service_level(service_level=95.0, frame_summary=sim_frame,
#                                                   orders_analysis=orders_analysis.orders, runs=100,
#                                                   percentage_increase=1.30)
#
# sim_frame = simulate.summarise_frame(sim_window)
#
# optimised_orders = simulate.optimise_service_level(service_level=95.0, frame_summary=sim_frame,
#                                                   orders_analysis=orders_analysis.orders, runs=100,
#                                                   percentage_increase=1.30)
# end = time.time()
#
# secs = end - start_time
# print(secs)


if __name__ == '__main__':
    main()
