#!/usr/bin/env python3
import os
import time
from decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy.inventory.summarise import OrdersAnalysis
from supplychainpy.reporting.load import load
from supplychainpy.launch_reports import launch_load_report, launch_report

__author__ = 'kevin'


def main():
    start_time = time.time()
    app_dir = os.path.dirname(__file__, )
    rel_path = 'supplychainpy/data2.csv'
    abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                                     z_value=Decimal(1.28),
                                                                     reorder_cost=Decimal(5000),
                                                                     file_type="csv", length=12)
   #for i in orders_analysis:
   #    print(i.orders_summary())

    ia = [analysis.orders_summary() for analysis in
         model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                         reorder_cost=Decimal(5000), file_type="csv",
                                                         length=12)]
    print(ia)

    #launch_report()
    analysis_summary = OrdersAnalysis(analysed_orders=orders_analysis)
    skus = ['KR202-209', 'KR202-210', 'KR202-211']

    skus_description = [summarised for summarised in analysis_summary.describe_sku(*skus)]
    print(skus_description)

    # top_ten_shortages = [item for item in analysis_summary.rank_summary(attribute="shortages", count=10, reverse=True)]

    # print(top_ten_shortages)

    # inventory_analysis = [analysis.orders_summary() for analysis in
    #                      model_inventory.analyse_orders_abcxyz_from_file(file_path="data2.csv", z_value=Decimal(1.28),
    #                                                                      reorder_cost=Decimal(5000), file_type="csv",
    #                                                                      length=12)]
    # print(inventory_analysis)
    # for orders in inventory_analysis:
    #    print(orders)


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
