import datetime
import os
from decimal import Decimal

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


from supplychainpy.reporting.config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)



def load(InventoryAnalysis, DataUpload):

    app_dir = os.path.dirname(__file__, )
    rel_path = '../supplychainpy/data2.csv'
    abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

    import supplychainpy
    ia = [analysis.orders_summary() for analysis in
          supplychainpy.model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path, z_value=Decimal(1.28),
                                                          reorder_cost=Decimal(5000), file_type="csv",
                                                          length=12)]
    date_now = datetime.datetime.now()





    for item in ia:

        i_up = InventoryAnalysis()
        d_up = DataUpload()
        d_up.data = str("data2")

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
        i_up.data_upload_id = d_up.id
        i_up.sku_id = item['sku']
        db.session.add(d_up)
        db.session.add(i_up)
    db.session.commit()



if __name__ == '__main__':
    load()
