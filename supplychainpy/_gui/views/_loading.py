import tkinter as tk
from tkinter import ttk


class LoadingFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.top = ttk.Label(self.controller, text="Enter path to file: ").grid(row=0, column=0, padx=5, pady=5,
                                                                                ipadx=5, ipady=5)
        self.path_input = ttk.Entry(self.controller, width=25)
        # always split into two lines otherwise unable to retrieve value.
        self.path_input.grid(row=0, column=1, columnspan=3)
        self.cancel_btn = ttk.Button(self.controller, text='Cancel').grid(row=1, column=2, pady=(5, 10), padx=(15, 0))
        self.select_button = ttk.Button(self.controller, text='Select',)
        self.select_button.grid(row=1, column=3, pady=(5, 10), padx=(15, 5))
