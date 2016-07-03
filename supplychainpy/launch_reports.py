import os
import threading

from supplychainpy.reporting.views import app, db
import tkinter as tk
from tkinter import ttk


class ReportsLauncher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.message = "launching reports"
        self.name = "reports"

    def print_message(self):
        print(self.message)

    def run(self):
        app.run()


def exit_report():
    exit()


class SupplychainpyReporting:
    def __init__(self, master):
        self.spawn = ReportsLauncher()
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/reporting/static/logo.gif'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        logo = tk.PhotoImage(file=abs_file_path)
        self.image = ttk.Label(master, image=logo)
        self.image.image = logo
        self.image.config(background='darkgrey')
        self.image.grid(row=0, column=0, columnspan=3)

        self.instruction_label = ttk.Label(master, text='Launch supplychainpy reports')
        self.instruction_label.grid(row=1, column=0, columnspan=2)

        self.port_label = ttk.Label(master, text='Port:')
        self.port_label.grid(row=2, column=0, columnspan=1)

        # self.port_input = ttk.
        ttk.Button(master, text='Launch Reporting', command=lambda: self.spawn_reports()).grid(row=3, column=0)
        ttk.Button(master, text='Exit Reporting', command=lambda: exit_report()).grid(row=3, column=1)

    def spawn_reports(self):
        self.spawn.daemon = True
        self.spawn.start()


def launch_report():
    from supplychainpy.reporting import load
    # db.create_all()
    # load.load()
    launcher = tk.Tk()
    app = SupplychainpyReporting(launcher)
    launcher.mainloop()
