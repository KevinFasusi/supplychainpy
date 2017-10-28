import flask
from flask import Blueprint
from flask import Flask

from supplychainpy.reporting.blueprints.models import InventoryAnalysis, Currency
from supplychainpy.reporting.config.settings import DevConfig
from supplychainpy.reporting.extensions import db

rawdata_blueprint = Blueprint('rawdata', __name__, template_folder='templates')


app = Flask(__name__)
app.config.from_object(DevConfig)

@rawdata_blueprint.route('/data')
def rawdata():
    """Route for the raw data from the analysis.

    Returns:

    """
    inventory = db.session.query(InventoryAnalysis).all()
    cur = db.session.query(Currency).all()

    return flask.render_template('rawdata.html', inventory=inventory, currency=cur)

