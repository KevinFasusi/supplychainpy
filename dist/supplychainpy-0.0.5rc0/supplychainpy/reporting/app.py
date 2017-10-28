import os

import flask
import jinja2
from flask import Flask

from supplychainpy.reporting.blueprints.contact.views import contact_blueprint
from supplychainpy.reporting.blueprints.dashboard.views import dashboard_blueprint, DASHBOARD_TEMPLATE_DIR
from supplychainpy.reporting.blueprints.bot.views import bot_blueprint
from supplychainpy.reporting.blueprints.rawdata.views import rawdata_blueprint
from supplychainpy.reporting.blueprints.recommendations.views import recommendations_blueprint
from supplychainpy.reporting.blueprints.simulation.views import simulation_blueprint

from supplychainpy.reporting.config.settings import ProdConfig, DevConfig
from supplychainpy.reporting.extensions import db, manager
from flask import abort


def create_app(settings_override=None):
    """
    Create flask application using the application factory pattern.

    Returns:
        Flask: Application

    """
    #here = os.path.dirname(os.path.abspath(__file__))
   # static_path = os.path.join(here,'static')
    #print(static_path)

    app = Flask(__name__, instance_relative_config=True, static_folder='static',)

    app.config.from_object(ProdConfig)

    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template('404.html'), 404

    if settings_override:
        app.config.update(settings_override)
    try:
        with app.app_context():
            app.register_blueprint(dashboard_blueprint)
            app.register_blueprint(bot_blueprint)
            app.register_blueprint(rawdata_blueprint)
            app.register_blueprint(recommendations_blueprint)
            app.register_blueprint(contact_blueprint)
            app.register_blueprint(simulation_blueprint)
            extensions(app)
    except OSError:
        abort(404)

    return app



def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).


    """
    db.init_app(app)
    manager.init_app(app)
    return None
