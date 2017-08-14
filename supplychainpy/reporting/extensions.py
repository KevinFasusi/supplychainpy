from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
manager = APIManager(flask_sqlalchemy_db=db)
