import os
from ctypes import cast
from datetime import datetime

import flask

from flask import Flask, request, send_from_directory

from sqlalchemy import func, desc

from supplychainpy.reporting.config import DevConfig
from flask.ext.sqlalchemy import SQLAlchemy

from supplychainpy.reporting.forms import DataForm, upload

app_dir = os.path.dirname(__file__, )
rel_path = '../uploads'
abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
UPLOAD_FOLDER = abs_file_path
app = Flask(__name__)
app.config.from_object(DevConfig)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)


class InventoryAnalysis(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    sku_id = db.Column(db.String(255))
    abc_xyz_classification = db.Column(db.String(2))
    standard_deviation = db.Column(db.Integer())
    safety_stock = db.Column(db.Integer())
    reorder_level = db.Column(db.Integer())
    economic_order_quantity = db.Column(db.Integer())
    demand_variability = db.Column(db.Integer())
    average_orders = db.Column(db.Float())
    shortages = db.Column(db.Integer())
    excess_stock = db.Column(db.Integer())
    reorder_quantity = db.Column(db.Integer())
    economic_order_variable_cost = db.Column(db.Float())
    unit_cost = db.Column(db.Numeric(12, 2))
    revenue = db.Column(db.Float())
    date = db.Column(db.DateTime())
    safety_stock_rank = db.Column(db.Integer())
    shortage_rank = db.Column(db.Integer())
    excess_cost = db.Column(db.Numeric(12, 2))
    percentage_contribution_revenue = db.Column(db.Float)
    excess_rank = db.Column(db.Integer())
    retail_price = db.Column(db.Numeric(18, 2))
    gross_profit_margin = db.Column(db.Numeric(12, 2))
    min_order = db.Column(db.Integer())
    safety_stock_cost = db.Column(db.Numeric(18, 2))
    revenue_rank = db.Column(db.Integer())
    markup_percentage = db.Column(db.Float())
    max_order = db.Column(db.Integer())
    shortage_cost = db.Column(db.Numeric(18, 2))
    quantity_on_hand = db.Column(db.Integer())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.sku_id,
            'revenue': self.revenue,
            'classification': self.abc_xyz_classification,
            'eoq': self.economic_order_quantity,
            'safe'
            'Date': convert_datetime(self.date),
            'standard_deviation': self.standard_deviation,
            'safety_stock': self.safety_stock,
            'reorder_level': self.reorder_level,
            'economic_order_quantity': self.economic_order_quantity,
            'demand_variability': self.demand_variability,
            'average_orders': round(self.average_orders),
            'shortages': self.shortages,
            'excess_stock': self.excess_stock,
            'reorder_quantity': float(self.reorder_quantity),
            'economic_order_variable_cost': float(self.economic_order_variable_cost),
            'unit_cost': float(self.unit_cost),
            'safety_stock_rank': self.safety_stock_rank,
            'shortage_rank': self.shortage_rank,
            'excess_cost': float(self.excess_cost),
            'percentage_contribution_revenue': float(self.percentage_contribution_revenue),
            'excess_rank': self.excess_rank,
            'retail_price': float(self.retail_price),
            'gross_profit_margin': float(self.gross_profit_margin),
            'min_order': self.min_order,
            'safety_stock_cost': float(self.safety_stock_cost),
            'revenue_rank': self.revenue_rank,
            'markup_percentage': self.markup_percentage,
            'max_order': self.max_order,
            'shortage_cost': float(self.shortage_cost),
            'quantity_on_hand': self.quantity_on_hand
        }


def convert_datetime(value):
    """Deserialize datetime object into string"""
    if value is None:
        return None
    return [value.strftime("%d-%m-%y"), value.strftime("%H:%M:%S")]


@app.route('/')
def hello_world():
    return flask.render_template('index.html')


@app.route('/data')
def raw_data():
    inventory = db.session.query(InventoryAnalysis).all()

    return flask.render_template('rawdata.html', inventory=inventory)


@app.route('/upload/', methods=['POST', 'GET'])
def upload_file():
    target = UPLOAD_FOLDER
    form = DataForm()
    if request.method == 'POST':
        upload(request=request)
        return "{}".format(request)

    return flask.render_template('upload.html', form=form)


@app.route('/reporting/api/v1.0/sku_detail', methods=['GET'])
@app.route('/reporting/api/v1.0/sku_detail/<string:sku_id>', methods=['GET'])
def sku_detail(sku_id: str = None):
    """route for restful sku detail, whole content limited by most recent date or individual sku"""
    if sku_id is not None:
        inventory = db.session.query(InventoryAnalysis).filter(InventoryAnalysis.sku_id == sku_id).all()
    else:
        inventory = db.session.query(InventoryAnalysis).all()
    return flask.jsonify(json_list=[i.serialize for i in inventory])


@app.route('/sku_detail', methods=['GET'])
@app.route('/sku_detail/<string:sku_id>', methods=['GET'])
def sku(sku_id: str = None):
    """route for restful sku detail, whole content limited by most recent date or individual sku"""
    if sku_id is not None:
        inventory = db.session.query(InventoryAnalysis).filter(InventoryAnalysis.sku_id == sku_id).all()
    else:
        inventory = db.session.query(InventoryAnalysis).all()
    return flask.render_template('sku.html', inventory=inventory)


@app.route('/reporting/api/v1.0/abc_summary', methods=['GET'])
@app.route('/reporting/api/v1.0/abc_summary/<string:classification>', methods=['GET'])
def get_classification_summary(classification: str = None):
    """route for restful summary of costs by abcxyz classifications"""
    if classification is not None:
        revenue_classification = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                                  func.sum(InventoryAnalysis.revenue).label('total_revenue'),
                                                  func.sum(InventoryAnalysis.shortage_cost).label('total_shortages')
                                                  ).filter(
            InventoryAnalysis.abc_xyz_classification == classification).group_by(
            InventoryAnalysis.abc_xyz_classification).all()
    else:
        revenue_classification = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                                  func.sum(InventoryAnalysis.revenue).label('total_revenue'),
                                                  func.sum(InventoryAnalysis.shortage_cost).label('total_shortages')
                                                  ).group_by(InventoryAnalysis.abc_xyz_classification).all()

    return flask.jsonify(json_list=[i for i in revenue_classification])


@app.route('/reporting/api/v1.0/top_shortages', methods=['GET'])
@app.route('/reporting/api/v1.0/top_shortages/<int:rank>', methods=['GET'])
@app.route('/reporting/api/v1.0/top_shortages/<string:classification>', methods=['GET'])
def top_shortages(rank: int = 10, classification: str = None):
    """ route for restful summary of top skus """
    if classification is not None:
        revenue_classification = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                                  InventoryAnalysis.sku_id,
                                                  InventoryAnalysis.shortage_cost,
                                                  InventoryAnalysis.quantity_on_hand,
                                                  InventoryAnalysis.percentage_contribution_revenue,
                                                  InventoryAnalysis.revenue_rank,
                                                  InventoryAnalysis.shortages,
                                                  InventoryAnalysis.average_orders,
                                                  InventoryAnalysis.safety_stock,
                                                  InventoryAnalysis.reorder_level
                                                  ).filter(
            InventoryAnalysis.abc_xyz_classification == classification).order_by(
            desc(InventoryAnalysis.shortage_cost)).limit(rank)
    else:
        revenue_classification = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                                  InventoryAnalysis.sku_id,
                                                  InventoryAnalysis.shortage_cost,
                                                  InventoryAnalysis.quantity_on_hand,
                                                  InventoryAnalysis.percentage_contribution_revenue,
                                                  InventoryAnalysis.revenue_rank,
                                                  InventoryAnalysis.shortages,
                                                  InventoryAnalysis.average_orders,
                                                  InventoryAnalysis.safety_stock,
                                                  InventoryAnalysis.reorder_level
                                                  ).order_by(desc(InventoryAnalysis.shortage_cost)).limit(rank)

    return flask.jsonify(json_list=[i for i in revenue_classification])


@app.route('/reporting/api/v1.0/top_excess', methods=['GET'])
@app.route('/reporting/api/v1.0/top_excess/<int:rank>', methods=['GET'])
@app.route('/reporting/api/v1.0/top_excess/<string:classification>', methods=['GET'])
def top_excess(rank: int = 10, classification: str = None):
    """ route for restful summary of top skus """
    if classification is not None:
        revenue_classification = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                                  InventoryAnalysis.sku_id,
                                                  InventoryAnalysis.excess_cost,
                                                  InventoryAnalysis.quantity_on_hand,
                                                  InventoryAnalysis.percentage_contribution_revenue,
                                                  InventoryAnalysis.revenue_rank,
                                                  InventoryAnalysis.excess_stock,
                                                  InventoryAnalysis.average_orders,
                                                  InventoryAnalysis.safety_stock,
                                                  InventoryAnalysis.reorder_level
                                                  ).filter(
            InventoryAnalysis.abc_xyz_classification == classification).order_by(
            desc(InventoryAnalysis.excess_cost)).limit(rank)
    else:
        revenue_classification = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                                  InventoryAnalysis.sku_id,
                                                  InventoryAnalysis.excess_cost,
                                                  InventoryAnalysis.quantity_on_hand,
                                                  InventoryAnalysis.percentage_contribution_revenue,
                                                  InventoryAnalysis.revenue_rank,
                                                  InventoryAnalysis.excess_stock,
                                                  InventoryAnalysis.average_orders,
                                                  InventoryAnalysis.safety_stock,
                                                  InventoryAnalysis.reorder_level
                                                  ).order_by(desc(InventoryAnalysis.excess_cost)).limit(rank)

    return flask.jsonify(json_list=[i for i in revenue_classification])


# @app.route('/upload/', methods=('GET', 'POST'))
# def upload():
#    form = DataForm()
#    upload_data = DataUpload()
#
#    if request.method == 'POST':
#        file = request.files['data']
#        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            # upload_data.data = filename
#            # upload_data.date = datetime.now()
#            # db.session.add(upload_data)
#            # db.session.commit()
#
#            return redirect(url_for('uploaded_file',
#                                    filename=filename))
#
#
#    return flask.render_template('upload.html', form=form)


def launch_report():
    from supplychainpy.reporting import load
    #db.create_all()
    #load.load()
    app.run()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run()
