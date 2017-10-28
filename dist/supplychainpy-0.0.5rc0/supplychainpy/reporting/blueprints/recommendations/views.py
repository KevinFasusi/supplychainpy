import flask
from flask import Blueprint
from flask import Flask

from supplychainpy.reporting.blueprints.models import InventoryAnalysis, MasterSkuList, \
    Recommendations, ProfileRecommendation
from supplychainpy.reporting.config.settings import ProdConfig
from supplychainpy.reporting.extensions import db

recommendations_blueprint = Blueprint('recommendations', __name__, template_folder='templates')


app = Flask(__name__)
app.config.from_object(ProdConfig)

@recommendations_blueprint.route('/recommended/<string:sku_id>', methods=['GET'])
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


@recommendations_blueprint.route('/feed', methods=['GET'])
def recommendations():
    recommend = db.session.query(Recommendations).all()
    profile = db.session.query(ProfileRecommendation).all()
    inventory = db.session.query(InventoryAnalysis).all()
    return flask.render_template('feed.html', inventory=inventory, profile=profile, recommendations=recommend)

