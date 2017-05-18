import os

from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import deserialise_config
from supplychainpy.reporting.app import create_app
from supplychainpy.reporting.extensions import db

config = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
app = create_app()

if os.name in ['posix', 'mac']:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/reporting.db'.format(config.get('database_path'))
elif os.name == 'nt':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\reporting.db'.format(config.get('database_path'))
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()