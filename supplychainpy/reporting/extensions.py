from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension


debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
manager = APIManager(flask_sqlalchemy_db=db)
