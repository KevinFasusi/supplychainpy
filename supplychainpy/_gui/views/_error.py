import tkinter as tk
from tkinter import ttk

import os


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

        self.hello_world_lbl = ttk.Label(self.parent, text=kwargs.get('msg'))
        self.hello_world_lbl.pack()

        self.close_btn =tk.Button(self.parent, text='Close')
        self.close_btn.config(command = self.close)
        self.close_btn.pack()

    def close(self):
        self.window_live.set(False)
        self.parent.destroy()
