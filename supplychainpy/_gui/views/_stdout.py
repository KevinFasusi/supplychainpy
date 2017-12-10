# Copyright (c) 2015-207, The Authors and Contributors
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


import sys
import threading
import tkinter as tk
from tkinter import ttk

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