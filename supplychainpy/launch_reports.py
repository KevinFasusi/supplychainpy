# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import threading
import webbrowser

from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import deserialise_config, serialise_config
from supplychainpy.reporting.views import db, app
import tkinter as tk
from tkinter import ttk


class ReportsLauncher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.message = "launching reports"
        self.name = "reports"
        self.port = 5000
        self.host = '127.0.0.1'

    def print_message(self):
        print(self.message)

    def run(self):
        config = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
        config['port'] = self.port
        config['host'] = self.host
        serialise_config(config, ABS_FILE_PATH_APPLICATION_CONFIG)
        # print(self.port)
        app.run(host= self.host,port=self.port)


def exit_report():
    exit()


def launch_browser(event, url: str):
    webbrowser.open_new(str(url))


class SupplychainpyReporting:
    """Creates report launcher gui, to launch browser and using flask local server. Allows port number to be
        changed.
    """

    def __init__(self, master):
        master.title('Supplychainpy')
        master.resizable(False, False)

        self.spawn = ReportsLauncher()
        self.parent = master
        self.hyperlink = ''
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/reporting/static/logo.gif'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        logo = tk.PhotoImage(file=abs_file_path)
        self.style = ttk.Style()
        self.style.configure('TCheckbutton', background='black')
        self.style.configure('TLabel', background='black')

        # set supplychainpy logo for report launcher gui
        self.image = tk.Label(master, image=logo)
        self.image.image = logo
        self.image.config(background='black')
        self.image.grid(row=0, column=1, columnspan=2)

        self.instruction_label = tk.Label(master, text='Launch supplychainpy reports')
        self.instruction_label.grid(row=1, column=1, columnspan=6)
        self.instruction_label.config(background='black', foreground='white')

        self.hyperlink_label = tk.Label(master)
        self.hyperlink_label.config(background='black', foreground='#8dc53e', text='click to open browser:',
                                    font=('system', 10, 'bold'))

        self.validation_label = tk.Label(master)
        self.validation_label.config(background='black', foreground='red',
                                     text='Incorrect port! Please enter correct port number',
                                     font=('system', 10, 'bold'))

        self.runtime_validation_label = tk.Label(master)
        self.runtime_validation_label.config(background='black', foreground='red',
                                             text='The reports are already running @ {}'.format(self.hyperlink),
                                             font=('system', 10, 'bold'))

        self.port_label = tk.Label(master, text='Change port (default :5000):')
        self.port_label.config(background='black', foreground='white', justify=tk.RIGHT)

        self.port_text = tk.Entry(master, width=10)

        self.change_port = tk.BooleanVar()
        self.change_port.set(False)
        if os.name in ['posix', 'mac']:
            # sort out the checkbutton in ttk not tk
            s = ttk.Style()
            s.configure('Mac.TCheckbutton', focus='#000000', background='#000000', foreground='#FFFFFF')
            self.change_port_checkbutton = ttk.Checkbutton(master, variable=self.change_port, style='Mac.TCheckbutton',
                                                           text='Change default port (default :5000)',
                                                           command=lambda: self.show_port_entry())

        elif os.name == 'nt':
            print('nt')
            self.change_port_checkbutton = tk.Checkbutton(master, variable=self.change_port, activebackground='black',
                                                          activeforeground='white',
                                                          bg='black', fg='white', relief='solid', selectcolor='blue',
                                                          text='Change default port (default :5000)',
                                                          command=lambda: self.show_port_entry())

        self.change_port_checkbutton.config(onvalue=True)
        self.change_port_checkbutton.grid(row=2, column=1, columnspan=2, pady=(0, 10))

        self.hyperlink_text = tk.Label(master)
        self.hyperlink_text.config(background='black', foreground='lightblue', font=('courier', 11, 'underline'))
        self.hyperlink_text.bind("<Button-1>", lambda e, url=str(self.hyperlink): launch_browser(e, url))

        self.launcher_button = tk.Button(master, bg='black', fg='grey', text='Launch Reporting',
                                          command=lambda: self.spawn_reports()).grid(
            row=6, column=1, pady=(5, 10),
            padx=(15, 5))

        tk.Button(master, bg='black', fg='grey', text='Exit Reporting', command=lambda: exit_report()).grid(row=6,
                                                                                                            column=2,
                                                                                                            pady=(
                                                                                                                5, 10),
                                                                                                            padx=(
                                                                                                                5, 15))

    def spawn_reports(self):
        """Checks if port number is specified, then validates port number."""

        # if port specified check port is numeric
        try:

            if self.port_text.get() is not '' and isinstance(int(self.port_text.get()), int) and self.hyperlink == '':
                self.hyperlink = 'http://{}:{}'.format(self.spawn.host,self.port_text.get())
                self.validation_label.grid_forget()
                self.hyperlink_text.config(text=self.hyperlink)
                self.hyperlink_text.bind("<Button-1>", lambda e, url=str(self.hyperlink): launch_browser(e, url))
                self.hyperlink_text.grid(row=4, column=1, columnspan=2)
                self.hyperlink_label.grid(row=3, column=1, columnspan=2)
                self.spawn.daemon = True
                self.spawn.port = self.port_text.get()
                self.spawn.start()
            elif self.port_text.get() is '':
                self.validation_label.grid_forget()
                self.hyperlink = 'http://{}:{}'.format(self.spawn.host,self.spawn.port)
                self.hyperlink_text.config(text=self.hyperlink)
                self.hyperlink_text.bind("<Button-1>", lambda e, url=str(self.hyperlink): launch_browser(e, url))
                self.hyperlink_text.grid(row=4, column=1, columnspan=2)
                self.hyperlink_label.grid(row=3, column=1, columnspan=2)
                self.spawn.daemon = True
                self.spawn.start()
            else:
                self.hyperlink_label.grid_forget()

        except ValueError:
            self.validation_label.grid(row=3, column=1, columnspan=2)
            self.hyperlink_label.grid_forget()
        except RuntimeError:
            self.runtime_validation_label.grid(row=3, column=1, columnspan=2)

    def show_port_entry(self):
        if self.change_port.get():
            self.port_label.grid(row=5, column=1, columnspan=1, padx=(15, 0), pady=(10, 10))
            self.port_text.grid(row=5, column=2, columnspan=1, padx=(0, 15), pady=(10, 10))
        else:
            self.port_text.forget()
            self.port_label.forget()


def launch_load_report(file: str, location: str = None):
    from supplychainpy.reporting import load

    if location is not None and os.name in ['posix', 'mac']:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/reporting.db'.format(location)

    elif location is not None and os.name == 'nt':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\reporting.db'.format(location)

    db.create_all()
    if location is not None:
        load.load(file, location)
    else:
        load.load(file)

    launcher = tk.Tk()
    app_launch = SupplychainpyReporting(launcher)
    app_launch.parent.configure(background='black')
    launcher.mainloop()


def launch_report(location: str = None, port: int = 5000, host:str ='127.0.0.1'):
    if location is not None and os.name in ['posix', 'mac']:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/reporting.db'.format(location)

    elif location is not None and os.name == 'nt':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\reporting.db'.format(location)

    db.create_all()
    launcher = tk.Tk()
    app_launch = SupplychainpyReporting(launcher)
    app_launch.spawn.host = host
    app_launch.spawn.port = port

    app_launch.parent.configure(background='black')
    launcher.mainloop()


def load_db(file: str, location: str = None):
    from supplychainpy.reporting import load

    if location is not None and os.name in ['posix', 'mac']:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/reporting.db'.format(location)

    elif location is not None and os.name == 'nt':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\reporting.db'.format(location)

    db.create_all()
    if location is not None:
        load.load(file, location)
    else:
        load.load(file)


def launch_report_server(location: str = None, port: int = 5000, host:str ='127.0.0.1'):
    if location is not None and os.name in ['posix', 'mac']:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/reporting.db'.format(location)
    elif location is not None and os.name == 'nt':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}\\reporting.db'.format(location)
    db.create_all()
    app_launch = ReportsLauncher()
    app_launch.port = port
    app_launch.host = host
    app_launch.run()
