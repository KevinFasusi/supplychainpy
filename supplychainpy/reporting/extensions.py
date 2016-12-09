from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension


debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()