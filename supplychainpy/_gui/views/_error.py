# Copyright (c) 2015-2017, The Authors and Contributors
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


import tkinter as tk
from tkinter import ttk


class ErrorWindow(tk.Tk):
    def __init__(self, master: tk.Tk, *args, **kwargs):
        self.parent = tk.Toplevel(master)
        self.parent.resizable(False,False)
        self.window_live = kwargs.get('window_live')
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        app_height = 150
        app_width = 300
        app_x_pos = int((screen_width - app_width) / 3)
        app_y_pos = int((screen_height - app_height) / 2)
        self.parent.geometry('{}x{}+{}+{}'.format(app_width,app_height, app_x_pos, app_y_pos))
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack()

        self.hello_world_lbl = tk.Text(self.parent, wrap="word", height=10)
        self.hello_world_lbl.insert('0.0', kwargs.get('msg'))
        self.hello_world_lbl.pack()

        self.close_btn =tk.Button(self.parent, text='Close')
        self.close_btn.config(command = self.close)
        self.hello_world_lbl.window_create('insert',  window=self.close_btn)

    def close(self):
        self.window_live.set(False)
        self.parent.destroy()
