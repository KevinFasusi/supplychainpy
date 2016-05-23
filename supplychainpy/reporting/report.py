import os
from datetime import datetime

import flask

from flask import Flask, request, redirect, send_from_directory, url_for
from werkzeug.contrib.jsrouting import render_template

from supplychainpy.reporting import load
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


class DataUpload(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer(), primary_key=True)
    data = db.Column(db.String(255))
    analysis_id = db.relationship('InventoryAnalysis', backref='DataUpload', lazy='dynamic')
    date = db.Column(db.DateTime())


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


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
    unit_cost = db.Column(db.Float())
    revenue = db.Column(db.Float())
    date = db.Column(db.DateTime())
    data_upload_id = db.Column(db.Integer(), db.ForeignKey('data_upload.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.sku_id,
            'revenue': self.revenue,
            'classification': self.abc_xyz_classification,
            'Date': dump_datetime(self.date)

        }


@app.route('/')
def hello_world():
    inventory = db.session.query(InventoryAnalysis).filter(InventoryAnalysis.sku_id != None).all()

    return flask.render_template('index.html', inventory=inventory)


@app.route('/upload/', methods=['POST', 'GET'])
def upload_file():
    target = UPLOAD_FOLDER
    form = DataForm()
    if request.method == 'POST':
        upload(request=request)
        return "{}".format(request)

    return flask.render_template('upload.html', form=form)


@app.route('/reporting/api/v1.0/revenue', methods=['GET'])
def get_tasks():
    inventory = db.session.query(InventoryAnalysis).filter(InventoryAnalysis.sku_id != None).all()

    return flask.jsonify(json_list=[i.serialize for i in inventory])


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
    db.create_all()
    #load.load(InventoryAnalysis, DataUpload)
    app.run()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run()
