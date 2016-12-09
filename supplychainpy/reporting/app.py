import os

from flask import Flask
from flask.ext.restless import APIManager


from supplychainpy.reporting.blueprints.contact.views import contact_blueprint
from supplychainpy.reporting.blueprints.dashboard.views import dashboard_blueprint
from supplychainpy.reporting.blueprints.bot.views import bot_blueprint
from supplychainpy.reporting.blueprints.rawdata.views import rawdata_blueprint
from supplychainpy.reporting.blueprints.recommendations.views import recommendations_blueprint

from supplychainpy.reporting.config.settings import ProdConfig
from supplychainpy.reporting.extensions import debug_toolbar, db

def create_app(settings_override=None):
    """
    Create flask application using the application factory pattern.

    Returns:
        Flask: Application

    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(ProdConfig)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(bot_blueprint)
    app.register_blueprint(rawdata_blueprint)
    app.register_blueprint(recommendations_blueprint)
    app.register_blueprint(contact_blueprint)

    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).


    """
    debug_toolbar.init_app(app)
    db.init_app(app)
    return None
