from supplychainpy.reporting.views import app, db


def launch_report():
    from supplychainpy.reporting import load
    #db.create_all()
    #load.load()
    app.run()
