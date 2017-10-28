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
import logging
from flask import Blueprint
from flask import Flask
from flask import send_from_directory

from sqlalchemy import func, desc, asc

from supplychainpy.reporting.blueprints.models import (InventoryAnalysis,
                                                       Currency,
                                                       MasterSkuList, Recommendations, TransactionLog, Orders,
                                                       ForecastBreakdown, Forecast,
                                                       ForecastStatistics)
from supplychainpy.reporting.config.settings import ProdConfig
from supplychainpy.reporting.extensions import db, manager

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

app_dir = os.path.dirname(__file__, )
rel_path = '../uploads'
abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
UPLOAD_FOLDER = abs_file_path
app = Flask(__name__)
app.config.from_object(ProdConfig)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DASHBOARD_TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='templates')

manager.create_api(InventoryAnalysis, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True,
                   results_per_page=10, max_results_per_page=500)
manager.create_api(Currency, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(Orders, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(Forecast, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(ForecastStatistics, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(ForecastBreakdown, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(MasterSkuList, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)
manager.create_api(Recommendations, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_functions=True)



@dashboard_blueprint.route('/', methods=['GET'])
def dashboard():
    top_ten_shortages = db.session.query(InventoryAnalysis).order_by(desc(InventoryAnalysis.shortage_cost)).limit(10)
    largest_shortage = db.session.query(InventoryAnalysis).order_by(asc(InventoryAnalysis.shortage_rank)).first()
    total_shortages = db.session.query(InventoryAnalysis).order_by(desc(InventoryAnalysis.shortage_cost)).limit(10)
    total_shortages = total_shortages.with_entities(func.sum(InventoryAnalysis.shortage_cost)).scalar
    top_ten_excess = db.session.query(InventoryAnalysis).order_by(desc(InventoryAnalysis.excess_cost)).limit(10)
    largest_excess = db.session.query(InventoryAnalysis).order_by(asc(InventoryAnalysis.excess_rank)).first()
    total_excess = db.session.query(InventoryAnalysis).order_by(desc(InventoryAnalysis.excess_cost)).limit(10)
    total_excess = total_excess.with_entities(func.sum(InventoryAnalysis.excess_cost)).scalar
    currency = db.session.query(Currency).all()

    return flask.render_template('dashboard.html', shortages=top_ten_shortages, currency=currency,
                                 largest= largest_shortage, shortage= total_shortages, excess=top_ten_excess,
                                 largest_excess=largest_excess, total_excess=total_excess)


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


@dashboard_blueprint.route('/reporting/api/v1.0/sku_detail', methods=['GET'])
@dashboard_blueprint.route('/reporting/api/v1.0/sku_detail/<string:sku_id>', methods=['GET'])
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


@dashboard_blueprint.route('/sku_detail', methods=['GET'])
@dashboard_blueprint.route('/sku_detail/<string:sku_id>', methods=['GET'])
def sku(sku_id: str = None):
    """route for restful sku detail, whole content limited by most recent date or individual sku"""
    if sku_id is not None:
        current_transaction = db.session.query(TransactionLog).order_by(desc(TransactionLog.id)).first()
        sku = db.session.query(MasterSkuList).filter(MasterSkuList.id == sku_id).first()
        inventory = db.session.query(InventoryAnalysis).filter(InventoryAnalysis.transaction_log_id == current_transaction.id, InventoryAnalysis.sku_id == sku.id).all()
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


@dashboard_blueprint.route('/reporting/api/v1.0/abc_summary', methods=['GET'])
@dashboard_blueprint.route('/reporting/api/v1.0/abc_summary/<string:classification>', methods=['GET'])
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


@dashboard_blueprint.route('/abcxyz/<string:classification>')
def abxyz(classification: str = None):
    abc = db.session.query(InventoryAnalysis
                           ).filter(
        InventoryAnalysis.abc_xyz_classification == classification).all()

    msk = db.session.query(MasterSkuList).all()
    cur = db.session.query(Currency).all()

    return flask.render_template('abcxyz.html', inventory=abc, mks=msk, currency=cur)


@dashboard_blueprint.route('/reporting/api/v1.0/top_shortages', methods=['GET'])
@dashboard_blueprint.route('/reporting/api/v1.0/top_shortages/<int:rank>', methods=['GET'])
@dashboard_blueprint.route('/reporting/api/v1.0/top_shortages/<string:classification>', methods=['GET'])
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
                                                  InventoryAnalysis.shortage_rank,
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
                                                  InventoryAnalysis.shortage_rank,
                                                  InventoryAnalysis.average_orders,
                                                  InventoryAnalysis.safety_stock,
                                                  InventoryAnalysis.reorder_level
                                                  ).order_by(desc(InventoryAnalysis.shortage_cost)).limit(rank)

    return flask.jsonify(json_list=[i for i in revenue_classification])


@dashboard_blueprint.route('/reporting/api/v1.0/top_excess', methods=['GET'])
@dashboard_blueprint.route('/reporting/api/v1.0/top_excess/<int:rank>', methods=['GET'])
@dashboard_blueprint.route('/reporting/api/v1.0/top_excess/<string:classification>', methods=['GET'])
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


@dashboard_blueprint.route('/api/total_inventory', methods=['GET'])
def total_inventory():
    revenue_classification = db.session.query(
        InventoryAnalysis.sku_id,
        InventoryAnalysis.unit_cost,
        InventoryAnalysis.quantity_on_hand,
        InventoryAnalysis.transaction_log_id).all()

    return flask.jsonify(json_list=[i for i in revenue_classification])


@dashboard_blueprint.route('/reporting/api/v1.0/currency', methods=['GET'])
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



@dashboard_blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)




if __name__ == '__main__':
    app.run()
