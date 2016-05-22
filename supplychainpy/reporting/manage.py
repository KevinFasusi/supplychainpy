from flask.ext.script import Manager
from flask.ext.script import Server
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand
from report import app
from report import db, InventoryAnalysis

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, InventoryAnalysis=InventoryAnalysis)


if __name__ == '__main__':
    manager.run()
