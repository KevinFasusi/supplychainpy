from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from supplychainpy.reporting.report import app
from supplychainpy.reporting.report import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()