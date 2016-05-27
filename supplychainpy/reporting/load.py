import datetime
import os
from decimal import Decimal

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from supplychainpy.reporting.config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


def load():
    from supplychainpy import model_inventory
    from supplychainpy.inventory.summarise import OrdersAnalysis
    app_dir = os.path.dirname(__file__, )
    rel_path = '../supplychainpy/data2.csv'
    abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                                      z_value=Decimal(1.28),
                                                                      reorder_cost=Decimal(5000),
                                                                      file_type="csv", length=12)

    ia = [analysis.orders_summary() for analysis in
                          model_inventory.analyse_orders_abcxyz_from_file(file_path="data2.csv", z_value=Decimal(1.28),
                                                                          reorder_cost=Decimal(5000), file_type="csv",length=12)]
    date_now = datetime.datetime.now()
    analysis_summary = OrdersAnalysis(analysed_orders=orders_analysis)

    for item in ia:
        skus_description = [summarised for summarised in analysis_summary.describe_sku(item['sku'])]
        from supplychainpy.reporting.report import InventoryAnalysis
        i_up = InventoryAnalysis()
        i_up.abc_xyz_classification = item['ABC_XYZ_Classification']
        i_up.standard_deviation = item['standard_deviation']
        i_up.safety_stock = item['safety_stock']
        i_up.reorder_level = item['reorder_level']
        i_up.economic_order_quantity = item['economic_order_quantity']
        i_up.demand_variability = item['demand_variability']
        i_up.average_orders = item['average_orders']
        i_up.shortages = item['shortages']
        i_up.excess_stock = item['excess_stock']
        i_up.reorder_quantity = item['reorder_quantity']
        i_up.economic_order_variable_cost = item['economic_order_variable_cost']
        i_up.unit_cost = item['unit_cost']
        i_up.revenue = item['revenue']
        i_up.date = date_now
        i_up.sku_id = item['sku']
        i_up.sa = skus_description[0]['safety_stock_rank']
        i_up.safety_stock_rank = skus_description[0]['shortage_rank']
        i_up.excess_cost = skus_description[0]['excess_cost']
        i_up.percentage_contribution_revenue = skus_description[0]['percentage_contribution_revenue']
        i_up.excess_rank = skus_description[0]['excess_rank']
        i_up.retail_price = skus_description[0]['retail_price']
        i_up.gross_profit_margin = skus_description[0]['gross_profit_margin']
        i_up.min_order = skus_description[0]['min_order']
        i_up.safety_stock_cost = skus_description[0]['safety_stock_cost']
        i_up.revenue_rank = skus_description[0]['revenue_rank']
        i_up.markup_percentage = skus_description[0]['markup_percentage']
        i_up.max_order = skus_description[0]['max_order']
        i_up.shortage_cost = skus_description[0]['shortage_cost']
        i_up.quantity_on_hand = item['quantity_on_hand']
        db.session.add(i_up)
    db.session.commit()


#if __name__ == '__main__':
#    load()
