import threading
import tkinter as tk
from tkinter import ttk

import sys

from supplychainpy.launch_reports import load_db, launch_report_server


class StdoutPipe():
    def __init__(self, text_widget):
        self.text_output = text_widget
        self.flush = sys.stdout.flush

    def write(self, string):
        self.text_output.insert('end', string)
        self.text_output.see('end')


class Launcher(threading.Thread):
    """Launches reporting lauch panel """

    def __init__(self, user_entered_path, database_dir, port_num, host_address):
        threading.Thread.__init__(self)
        self.user_entered_path = user_entered_path
        self.database_dir = database_dir
        self.port_num = port_num
        self.host_address = host_address

    def print_message(self):
        pass
        """Prints launch message"""

    def run(self):
        load_db(file=self.user_entered_path, location=self.database_dir)
        launch_report_server(location=self.database_dir, port=self.port_num, host=self.host_address)


class StdoutWindow:
    """Creates report launcher gui, to launch browser and using flask local server. Allows port
    number to be changed."""

    def __init__(self, master, user_entered_path, database_dir, port_num, host_address):
        master.title('SUPPLYCHAINPY')
        master.resizable(False, False)

        self.spawn = Launcher(user_entered_path, database_dir, port_num, host_address)
        self.parent = master
        self.main_frame = ttk.Frame(master, relief=tk.FLAT, height=320)
        self.main_frame.grid(column=0, row=0, columnspan=2, sticky='NSWE', padx=5, pady=5)
        self.stdout = tk.Text(self.main_frame, wrap='word', height=320)
        self.stdout.grid(column=0, row=0, columnspan=2, sticky='NSWE', padx=5, pady=5)
        sys.stdout = StdoutPipe(self.stdout)
