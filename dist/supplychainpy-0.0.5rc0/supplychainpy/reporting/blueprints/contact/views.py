import flask
from flask import Blueprint


contact_blueprint = Blueprint('contact', __name__, template_folder='templates')


@contact_blueprint.route('/about', methods=['GET'])
def about():
    return flask.render_template('contact/about.html')
