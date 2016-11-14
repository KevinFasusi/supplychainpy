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

import flask
from flask import Flask, send_from_directory
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, asc
from supplychainpy.bot.dash import ChatBot
from supplychainpy.reporting.config import DevConfig


app_dir = os.path.dirname(__file__, )
rel_path = '../uploads'
abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
UPLOAD_FOLDER = abs_file_path
app = Flask(__name__)
app.config.from_object(DevConfig)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
db.create_all()


def convert_datetime(value):
    """Deserialize datetime object into string"""
    if value is None:
        return None
    return [value.strftime("%d-%m-%y"), value.strftime("%H:%M:%S")]


class MasterSkuList(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    sku_id = db.Column(db.String(255))
    analysis = db.relationship("InventoryAnalysis", backref='sku', lazy='dynamic')


class Currency(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    fx = db.relationship("InventoryAnalysis", backref='currency', lazy='dynamic')
    currency_code = db.Column(db.String(3))
    country = db.Column(db.String(255))
    symbol = db.Column(db.String(255))


class TransactionLog(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    transaction = db.relationship("InventoryAnalysis", backref='log', lazy='dynamic')
    profile_recommendation = db.relationship("ProfileRecommendation", backref='profile', lazy='dynamic')


class InventoryAnalysis(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    sku_id = db.Column(db.Integer, db.ForeignKey('master_sku_list.id'))
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
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    transaction_log_id = db.Column(db.Integer, db.ForeignKey('transaction_log.id'))
    orders_id = db.relationship("Orders", backref='demand', lazy='dynamic')
    forecast_id = db.relationship("Forecast", backref='forecasts', lazy='dynamic')
    forecast_breakdown_id = db.relationship("ForecastBreakdown", backref='estimates', lazy='dynamic')
    inventory_turns = db.Column(db.Float())
    traffic_light = db.Column(db.String(6))
    recommendation_id = db.relationship("Recommendations", backref='rec', lazy='dynamic')
    backlog = db.Column(db.Integer())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.sku_id,
            'revenue': self.revenue,
            'classification': self.abc_xyz_classification,
            'eoq': self.economic_order_quantity,
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
            'quantity_on_hand': self.quantity_on_hand,
            'inventory_turns': self.inventory_turns
        }


class Orders(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    order_quantity = db.Column(db.Integer())
    rank = db.Column(db.Integer())


class ForecastType(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(10))
    forecast_id = db.relationship("Forecast", backref='type', lazy='dynamic')
    forecast_statistic_id = db.relationship("ForecastStatistics", backref='details', lazy='dynamic')
    forecast_breakdown_id = db.relationship("ForecastBreakdown", backref='breakdown', lazy='dynamic')


class Forecast(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    forecast_quantity = db.Column(db.Integer())
    forecast_type_id = db.Column(db.Integer, db.ForeignKey('forecast_type.id'))
    period = db.Column(db.Integer())
    create_date = db.Column(db.DateTime())


class ForecastStatistics(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    forecast_type_id = db.Column(db.Integer, db.ForeignKey('forecast_type.id'))
    slope = db.Column(db.Float())
    p_value = db.Column(db.Float())
    test_statistic = db.Column(db.Float())
    slope_standard_error = db.Column(db.Float())
    intercept = db.Column(db.Float())
    standard_residuals = db.Column(db.Float())
    trending = db.Column(db.Boolean)
    mape = db.Column(db.Float())
    optimal_alpha = db.Column(db.Float())
    optimal_gamma = db.Column(db.Float())


class ForecastBreakdown(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    period = db.Column(db.Integer())
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    forecast_type_id = db.Column(db.Integer, db.ForeignKey('forecast_type.id'))
    level_estimates = db.Column(db.Float())
    trend = db.Column(db.Float())
    one_step_forecast = db.Column(db.Float())
    forecast_error = db.Column(db.Float())
    squared_error = db.Column(db.Float())
    regression = db.Column(db.Float())


class Recommendations(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    statement = db.Column(db.Text())


class ProfileRecommendation(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction_log.id'))
    statement = db.Column(db.Text())


manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(InventoryAnalysis, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True,
                   results_per_page=10, max_results_per_page=500)
manager.create_api(Currency, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(Orders, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(Forecast, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(ForecastStatistics, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(ForecastBreakdown, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(MasterSkuList, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(Recommendations, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)


@app.route('/')
def dashboard():
    top_ten_shortages = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                         InventoryAnalysis.id,
                                         InventoryAnalysis.shortage_cost,
                                         InventoryAnalysis.quantity_on_hand,
                                         InventoryAnalysis.percentage_contribution_revenue,
                                         InventoryAnalysis.revenue_rank,
                                         InventoryAnalysis.shortages,
                                         InventoryAnalysis.average_orders,
                                         InventoryAnalysis.safety_stock,
                                         InventoryAnalysis.reorder_level,
                                         InventoryAnalysis.currency_id
                                         ).order_by(desc(InventoryAnalysis.shortage_cost)).limit(10)
    currency = db.session.query(Currency).all()

    return flask.render_template('index.html', shortages=top_ten_shortages, currency=currency)


@app.route('/bot')
def bot():
    """the route for Dash the chat bot."""
    return flask.render_template('bot.html')


@app.route('/lexicon')
def lexicon():
    """The route for displaying examples for interacting with the chat bot.

    Returns:
        html

    """
    return flask.render_template('lexicon.html')


@app.route('/chat/<string:message>', methods=['GET'])
def chat(message: str = None):
    """ Rest api for chat bot

    Args:
        message: User query to chat bot.

    Returns:
        json:   Response from chat bot.

    """
    dash = ChatBot()
    response = dash.chat_machine(message=message)

    return flask.jsonify(json_list=response)


@app.route('/recommended/<string:sku_id>', methods=['GET'])
def recommended(sku_id: str = None):
    """The route to the rest api for retrieving recommendations for a SKU.

    Args:
        sku_id:     The SKU ID for a product.
    Returns:

    """
    """Rest api for sku level recommendations."""
    sku = db.session.query(MasterSkuList).filter(MasterSkuList.id == sku_id).first()
    inventory = db.session.query(InventoryAnalysis.id).filter(InventoryAnalysis.sku_id == sku.id).first()
    recommend = db.session.query(Recommendations.statement).filter(Recommendations.analysis_id == inventory.id).all()
    return flask.jsonify(json_list=recommend)


@app.route('/about', methods=['GET'])
def about():
    return flask.render_template('about.html')


@app.route('/feed', methods=['GET'])
def feed():
    recommend = db.session.query(Recommendations).all()
    profile = db.session.query(ProfileRecommendation).all()
    inventory = db.session.query(InventoryAnalysis).all()
    return flask.render_template('feed.html', inventory=inventory, profile=profile, recommendations=recommend)


@app.route('/data')
def raw_data():
    """Route for the raw data from the analysis.

    Returns:

    """
    inventory = db.session.query(InventoryAnalysis).all()
    cur = db.session.query(Currency).all()

    return flask.render_template('rawdata.html', inventory=inventory, currency=cur)


#@app.route('/upload/', methods=['POST', 'GET'])
#def upload_file():
#    """
#
#    Returns:
#
#    """
#    target = UPLOAD_FOLDER
#    form = DataForm()
#    if request.method == 'POST':
#        upload(request=request)
#        return "{}".format(request)
#
#    return flask.render_template('upload.html', form=form)


#@app.route('/settings', methods=['POST', 'GET'])
#def settings():
#    """Route to settings view.
#
#    Returns:
#
#    """
#    form = SettingsForm()
#    return flask.render_template('settings.html', form=form)


@app.route('/reporting/api/v1.0/sku_detail', methods=['GET'])
@app.route('/reporting/api/v1.0/sku_detail/<string:sku_id>', methods=['GET'])
def sku_detail(sku_id: str = None):
    """Route for restful sku detail, whole content limited by most recent date or individual sku

    Args:
        sku_id:

    Returns:

    """
    if sku_id is not None:
        inventory = db.session.query(InventoryAnalysis).filter(InventoryAnalysis.sku_id == sku_id).all()
    else:
        transaction_sub = db.session.query(db.func.max(TransactionLog.date))
        transaction_id = db.session.query(TransactionLog).filter(TransactionLog.date == transaction_sub).first()
        inventory = db.session.query(InventoryAnalysis).all()

    return flask.jsonify(json_list=[i.serialize for i in inventory])


@app.route('/sku_detail', methods=['GET'])
@app.route('/sku_detail/<string:sku_id>', methods=['GET'])
def sku(sku_id: str = None):
    """route for restful sku detail, whole content limited by most recent date or individual sku"""
    if sku_id is not None:
        sku = db.session.query(MasterSkuList).filter(MasterSkuList.id == sku_id).first()
        inventory = db.session.query(InventoryAnalysis).filter(InventoryAnalysis.sku_id == sku.id).all()
        inven = db.session.query(InventoryAnalysis.id).filter(InventoryAnalysis.sku_id == sku.id).first()
        orders = db.session.query(Orders).filter(Orders.analysis_id == inven.id).order_by(
            asc(Orders.rank)).all()
        forecast_breakdown = db.session.query(ForecastBreakdown).filter(ForecastBreakdown.analysis_id == inven.id)
        forecast = db.session.query(Forecast).filter(Forecast.analysis_id == inven.id).all()
        forecast_statistics = db.session.query(ForecastStatistics).filter(ForecastStatistics.analysis_id == inven.id)
        recommend = db.session.query(Recommendations.statement).filter(
            Recommendations.analysis_id == inven.id).all()
        cur = db.session.query(Currency).all()

    return flask.render_template('sku.html', inventory=inventory, orders=orders, breakdown=forecast_breakdown,
                                 forecast=forecast, statistics=forecast_statistics, recommendations=recommend,
                                 currency=cur)


@app.route('/reporting/api/v1.0/abc_summary', methods=['GET'])
@app.route('/reporting/api/v1.0/abc_summary/<string:classification>', methods=['GET'])
def get_classification_summary(classification: str = None):
    """route for restful summary of costs by abcxyz classifications"""
    if classification is not None:
        revenue_classification = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                                  InventoryAnalysis.currency_id,
                                                  Currency.currency_code,
                                                  func.sum(InventoryAnalysis.revenue).label('total_revenue'),
                                                  func.sum(InventoryAnalysis.shortage_cost).label('total_shortages'),
                                                  func.sum(InventoryAnalysis.excess_cost).label('total_excess')
                                                  ).join(Currency).filter(
            InventoryAnalysis.abc_xyz_classification == classification).group_by(
            InventoryAnalysis.abc_xyz_classification).all()
    else:
        revenue_classification = db.session.query(InventoryAnalysis.abc_xyz_classification,
                                                  InventoryAnalysis.currency_id,
                                                  Currency.currency_code,
                                                  func.sum(InventoryAnalysis.revenue).label('total_revenue'),
                                                  func.sum(InventoryAnalysis.shortage_cost).label('total_shortages'),
                                                  func.sum(InventoryAnalysis.excess_cost).label('total_excess')
                                                  ).join(Currency).group_by(
            InventoryAnalysis.abc_xyz_classification).all()

    return flask.jsonify(json_list=[i for i in revenue_classification])


@app.route('/abcxyz/<string:classification>')
def abxyz(classification: str = None):
    abc = db.session.query(InventoryAnalysis
                           ).filter(
        InventoryAnalysis.abc_xyz_classification == classification).all()

    msk = db.session.query(MasterSkuList).all()
    cur = db.session.query(Currency).all()

    return flask.render_template('abcxyz.html', inventory=abc, mks=msk, currency=cur)


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


@app.route('/api/total_inventory', methods=['GET'])
def total_inventory():
    revenue_classification = db.session.query(
        InventoryAnalysis.sku_id,
        InventoryAnalysis.unit_cost,
        InventoryAnalysis.quantity_on_hand,
        InventoryAnalysis.transaction_log_id).all()

    return flask.jsonify(json_list=[i for i in revenue_classification])


@app.route('/reporting/api/v1.0/currency', methods=['GET'])
def currency():
    pass
    #  currency_code = db.session.query(Currency.id).filter(Currency.currency_code == item['currency']).first()


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



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run()
