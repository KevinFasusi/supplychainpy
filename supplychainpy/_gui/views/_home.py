import threading
import tkinter as tk
from tkinter import ttk

import os

import pickle

import sys

import time

from supplychainpy._gui.controller.validate import port, host
from supplychainpy._gui.views._error import ErrorWindow
from supplychainpy._gui.views._stdout import StdoutWindow, StdoutPipe
from supplychainpy._helpers._config_file_paths import ABS_FILE_PICKLE, ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._pickle_config import serialise_config
from supplychainpy.launch_reports import launch_report_server, load_db, launch_report


class MainWindow(tk.Tk):
    CACHED_FILE_PATHS = 'cached_paths'

    def __init__(self, master: tk.Tk, *args, **kwargs):
        # launches second pane
        master.title('SUPPLYCHAINPY (Community Edition)')
        master.resizable(True, True)
        self.parent = master
        master.option_add('*tearoff', False)
        self.menubar = tk.Menu(master)
        master.config(menu=self.menubar)
        self.parent.config(background='black')

        # creating menubar
        self.file_menu = tk.Menu(self.menubar)
        self.edit_menu = tk.Menu(self.menubar)
        self.help_menu = tk.Menu(self.menubar)

        # add to the menubar
        self.menubar.add_cascade(menu=self.file_menu, label='File')
        self.menubar.add_cascade(menu=self.edit_menu, label='Edit')
        self.menubar.add_cascade(menu=self.help_menu, label='Help')

        # adding commands to menu
        self.file_menu.add_command(label='New Project', command=lambda: print("Testing"))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Open...', command=lambda: print("Testing"))
        self.file_menu.add_command(label='Save', command=lambda: print("Testing"))
        self.file_menu.add_command(label='Close', command=lambda: print("Testing"))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Settings', command=lambda: print("Testing"))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Synchronise', command=lambda: print("Testing"))

        # adding accelerators based on operating system
        self.file_menu.entryconfig(index='New Project', accelerator='Command-n')
        self.menubar.bind_all('<Command-N>', lambda e: self.data_source_entry(e))

        # header frame
        self.frame_header = ttk.Frame(master, relief=tk.FLAT, )
        self.frame_header.config()
        self.frame_header.pack()
        app_dir = os.path.dirname(__file__, )
        rel_path = '../reporting/static/images/logo.gif'
        logo_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        logo = tk.PhotoImage(file=logo_path)
        self.style = ttk.Style()
        self.style.configure('TCheckbutton', background='black')
        self.style.configure('Horizontal.TProgressbar', troughcolor='black', focus='#000000', background='#000000')

        # adding main panes
        self.source_file_pane = ttk.PanedWindow(master, orient=tk.HORIZONTAL, )
        self.source_file_pane.pack(fill=tk.BOTH, expand=True)
        self.source_file_frame = ttk.Frame(self.source_file_pane, width=200)
        self.source_file_pane.add(self.source_file_frame)
        self.source_file_frame.config(relief=tk.SUNKEN, )

        # create list from config file
        cached_paths = self.read_source_file_path_cache()
        if cached_paths is None:
            cached_paths = ()
        else:
            cached_paths = [i[1] for i in cached_paths.items()]

        self.config_info = cached_paths
        self.listbox = tk.Listbox(self.source_file_frame, relief=tk.SUNKEN)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        # insert values to listbox
        # self.listbox.insert(tk.END, "Previous analysis")
        for item in self.config_info:
            self.listbox.insert(tk.END, item)

        self.main_panel = ttk.PanedWindow(master, orient=tk.VERTICAL)
        self.main_frame = ttk.Frame(self.main_panel, relief=tk.FLAT, height=320)
        self.main_frame.config(padding=(10, 30))
        self.main_panel.add(self.main_frame)
        self.source_file_pane.add(self.main_panel)
        self.image = tk.Label(self.frame_header, image=logo)
        self.image.image = logo
        self.image.config(background='black')
        self.image.grid(row=0, column=1, columnspan=2)
        self.image.config(compound=tk.CENTER)
        self.main_frame.config(relief=tk.RAISED)
        self.source_file_path_entered = tk.BooleanVar()
        self.source_file_path_entered.set(False)
        # the top left frame
        # self.path_selection_frame = ttk.Frame(self.top_panel, relief=tk.FLAT)

        p_bar = ttk.Style()
        p_bar.theme_use('clam')
        p_bar.configure("black.Horizontal.TProgressbar", foreground='Green', background='Black')

        # binding to listbox
        self.listbox.bind('<<ListboxSelect>>', lambda e: self.data_source_entry(e))
        self.progress_frame = ttk.Frame(master)
        self.progress_frame.pack(side=tk.RIGHT)

        self.progressbar = ttk.Progressbar(self.progress_frame, style='black.Horizontal.TProgressbar',
                                           orient=tk.HORIZONTAL, length=200)
        self.progressbar.pack()
        self.progressbar.config(mode='indeterminate')
        self.progressbar.state(['disabled'])
        # self.progressbar.start()

        # adding frames and labels to the main_frame

        self.data_lbl_frm = ttk.Labelframe(self.main_frame, text='Data Source', padding=(5, 10, 5, 5))
        self.data_lbl_frm.grid(column=0, columnspan=12, row=0, sticky='nsew')

        self.settings_lbl_frm = ttk.Labelframe(self.main_frame, text='Settings', padding=(5, 10, 5, 5))
        self.settings_lbl_frm.grid(column=0, columnspan=12, row=4, sticky='nsew', pady=(20, 20))

        source_rel_path = '../reporting/static/images/source.gif'
        source_logo_path = os.path.abspath(os.path.join(app_dir, '..', source_rel_path))
        self.data_source_img = tk.PhotoImage(file=source_logo_path)

        self.data_source_lbl = ttk.Label(self.data_lbl_frm, text='Source File:')
        self.data_source_lbl.img = self.data_source_img
        self.data_source_lbl.img = self.data_source_lbl.img.subsample(2, 2)
        self.data_source_lbl.config(image=self.data_source_lbl.img, compound='left')

        self.data_source_lbl.grid(row=0, column=1, pady=(0, 10))
        self.data_entry = ttk.Entry(self.data_lbl_frm, width=30)
        self.data_entry.bind('<FocusOut>', lambda e: self.data_source_focusout())
        self.data_entry.grid(row=0, column=2, columnspan=2, pady=(0, 10))

        db_rel_path = '../reporting/static/images/db.gif'
        db_logo_path = os.path.abspath(os.path.join(app_dir, '..', db_rel_path))
        self.db_source_img = tk.PhotoImage(file=db_logo_path)

        self.database_lbl = ttk.Label(self.data_lbl_frm, text='Database:')
        self.database_lbl.img = self.db_source_img
        self.database_lbl.img = self.database_lbl.img.subsample(2, 2)
        self.database_lbl.config(image=self.database_lbl.img, compound='left')
        self.database_lbl.grid(row=1, column=1, pady=(0, 10))
        self.database_entry = ttk.Entry(self.data_lbl_frm, width=30)
        self.database_entry.grid(row=1, column=2, columnspan=2, pady=(0, 10))
        self.database_entry.state(['disabled'])

        socket_rel_path = '../reporting/static/images/socket.gif'
        socket_logo_path = os.path.abspath(os.path.join(app_dir, '..', socket_rel_path))
        self.socket_source_img = tk.PhotoImage(file=socket_logo_path)

        self.port_lbl = ttk.Label(self.settings_lbl_frm, text='Port:')
        self.port_lbl.img = self.socket_source_img
        self.port_lbl.config(image=self.port_lbl.img, compound='left')

        self.port_lbl.grid(row=0, column=1, pady=(0, 10))
        self.port_entry = ttk.Entry(self.settings_lbl_frm, width=30)
        self.port_entry.grid(row=0, column=2, columnspan=2, pady=(0, 10))

        host_rel_path = '../reporting/static/images/server.gif'
        host_logo_path = os.path.abspath(os.path.join(app_dir, '..', host_rel_path))
        self.host_img = tk.PhotoImage(file=host_logo_path)

        self.host_lbl = ttk.Label(self.settings_lbl_frm, text='Host:')
        self.host_lbl.img = self.host_img
        self.host_lbl.img = self.host_lbl.img.subsample(2, 2)
        self.host_lbl.config(image=self.host_lbl.img, compound='left')
        self.host_lbl.grid(row=1, column=1, pady=(0, 10))
        self.host_entry = ttk.Entry(self.settings_lbl_frm, width=30, text='127.0.0.1')
        self.host_entry.grid(row=1, column=2, columnspan=2, pady=(0, 10))

        self.analysis_var = tk.BooleanVar()
        self.analysis_var.set(True)
        self.analysis_btn = ttk.Checkbutton(self.settings_lbl_frm, onvalue=True, offvalue=False,
                                            variable=self.analysis_var,
                                            command=self.toggle_analysis_check, text='Run Analysis')
        self.analysis_btn.grid(row=2, column=2, pady=(10, 10))

        self.launch_var = tk.BooleanVar()
        self.launch_var.set(True)
        self.launch_btn = ttk.Checkbutton(self.settings_lbl_frm, onvalue=True, offvalue=False, variable=self.launch_var,
                                          command=self.toggle_launch_check, text='Launch Reports')
        self.launch_btn.grid(row=2, column=3, pady=(10, 10))

        self.reset_btn = ttk.Button(self.main_frame, text='Reset')
        self.reset_btn.grid(row=5, column=9)
        self.reset_btn.config(command=self.reset_data_entry)

        self.finished_btn = ttk.Button(self.main_frame, text='Finished')
        self.finished_btn.config(command=self.finished)
        self.finished_btn.grid(row=5, column=11, )

        self.error_window_live = tk.BooleanVar()
        self.error_window_live.set(value=False)

    def toggle_analysis_check(self):
        if not self.analysis_var.get():
            self.analysis_var.set(False)
        else:
            self.analysis_var.set(True)

    def toggle_launch_check(self):
        if not self.launch_var.get():
            self.launch_var.set(False)
        else:
            self.launch_var.set(True)

    def show_frame(self, page_name):
        """ Show a frame for the given page name

        Args:
            page_name:

        Returns:

        """
        frame = self.frames[page_name]
        frame.tkraise()

    def data_source_entry(self, e):
        """ Populates data_entry widget form current selection in list selection

        Args:
            e:

        Returns:

        """
        try:
            selection = self.listbox.get(self.listbox.curselection()[0])
            if len(selection) > 0:
                self.data_entry.delete(0, tk.END)
                self.data_entry.insert(0, selection)
                self.source_file_path_entered.set(True)
                self.update_db_path(selection)
            else:
                self.auto_populate_db_path()
        except IndexError as err:
            pass

    def update_db_path(self, selected_path: str):
        """ Updates the database path entry widget and disables input from user.

        Args:
            selected_path (str):  path entered by user

        Returns:

        """
        database_path = self.db_path(selected_path)
        self.database_entry.state(['!disabled'])
        self.database_entry.delete(0, tk.END)
        self.database_entry.insert(0, database_path)
        self.database_entry.state(['disabled'])

    def reset_data_entry(self):
        self.data_entry.delete(0, tk.END)
        self.database_entry.state(['!disabled'])
        self.database_entry.delete(0, tk.END)
        self.database_entry.state(['disabled'])
        self.host_entry.delete(0, tk.END)
        self.port_entry.delete(0, tk.END)
        self.analysis_var.set(True)
        self.launch_var.set(True)

    def _set_db_path(self):
        if self.source_file_path_entered.set(True):
            pass

    def data_source_focusout(self, ):
        print(self.data_entry.get())
        self.check_valid_path(self.data_entry.get())

    def check_valid_path(self, path: str) -> bool:
        if not self.error_window_live:
            print('path not present')
            ErrorWindow(self.parent)
            self.error_window_live.set(True)
            return False

        if os.path.exists(os.path.dirname(path)):
            print('path present')
            self.update_db_path(path)
            return True

            # launch dialog box explaining that path does not exist and requesting if the user would like the path to be created.
            # use the path without the reporting.db at the end.

    def finished(self):
        start_pbar = threading.Thread(target=self.start_progressbar)
        start_pbar.start()
        start_validate = threading.Thread(target=self.validate_completed_form)
        start_validate.start()

    def validate_completed_form(self):
        user_entered_path = self.data_entry.get()
        port_num = self.port_entry.get()
        host_address = self.host_entry.get()
        launch_check = self.launch_var.get()
        report_check = self.analysis_var.get()
        filename = self.file_name(user_entered_path)

        if not port(port_num) and not self.error_window_live.get():
            self.error_window_live.set(True)
            ErrorWindow(self.parent, window_live=self.error_window_live, msg='Enter a valid port number')
        elif not host(host_address):
            self.error_window_live.set(True)
            ErrorWindow(self.parent, window_live=self.error_window_live, msg='Enter a valid host address')
        elif not launch_check and not report_check:
            self.error_window_live.set(True)
            ErrorWindow(self.parent, window_live=self.error_window_live,
                        msg='Select a valid option, \'Lanuch Reports\' or \'Run Analysis\'')
        elif self.check_valid_path(user_entered_path) and self.cache_unique():
            self.write_source_file_path_cache()

        database_dir = self.db_dir(user_entered_path)
        print(database_dir)

        # address currency selection
        app_settings = {
            'database_path': database_dir,
            'host': self.host_entry.get(),
            'currency': 'USD'
        }
        serialise_config(app_settings, ABS_FILE_PATH_APPLICATION_CONFIG)

        if report_check:
            #self.stdout = tk.Text(self.main_panel, wrap='word', height=320)
            #self.stdout.grid(column=0, row=0, columnspan=2, sticky='NSWE', padx=5, pady=5)
            #sys.stdout = StdoutPipe(self.stdout)
            #sys.stderr = StdoutPipe(self.stdout)
            start_load_db = threading.Thread(target=self.load_database, args=(user_entered_path, database_dir))
            start_load_db.start()
            start_load_db.join()
            self.progressbar.stop()
            launch_report_server(location=database_dir, port=port_num, host=host_address)
            #start_nav = threading.Thread(target=self.launch_nav)
            #start_nav.start()
            #launcher = tk.Tk()
            #app_launch = StdoutWindow(launcher, user_entered_path, database_dir, port_num, host_address)
            #app_launch.spawn.run()

    #def lauch_nav(self):
    #    launch_report()

    def start_progressbar(self):
        self.progressbar.state(['!disabled'])
        self.progressbar.start()

    def load_database(self,user_entered_path, database_dir):
        load_db(file=user_entered_path, location=database_dir)

    # def check_reporting_db(self):
       # pass

    # check if reporting database already exists if so inform user move to an archieve directory in the same directory and continue
    # append date. In future version add the ability to search archive of reporting databases.
    # if user choses no to archieving the database then only offer lanuching the reports and disable the analyse the reports checkbutton



    @staticmethod
    def file_name(path: str) -> str:
        """ Creates path to database in the same folder as source file.

        Args:
            path (str):

        Returns:
            str:    Path to create database

        """
        split_path = path.split(os.sep)
        path_components = [i for i in split_path if len(i) > 0]
        return path_components[-1:][0]

    @staticmethod
    def db_dir(path: str) -> str:
        """ Creates path to database in the same folder as source file.

        Args:
            path (str):

        Returns:
            str:    Path to create database

        """
        split_path = path.split(os.sep)
        path_components = [i for i in split_path if len(i) > 0]
        path_stem = ['{}{}'.format(os.sep, i) for i in path_components[:-1]]
        reconstituted_path = ''.join(path_stem)
        return reconstituted_path

    @staticmethod
    def db_path(path: str) -> str:
        """ Creates path to database in the same folder as source file.

        Args:
            path (str):

        Returns:
            str:    Path to create database

        """
        split_path = path.split(os.sep)
        path_components = [i for i in split_path if len(i) > 0]
        path_stem = ['{}{}'.format(os.sep, i) for i in path_components[:-1]]
        reconstituted_path = ''.join(path_stem)
        database_path = '{}/reporting.db'.format(reconstituted_path)
        return database_path

    def write_source_file_path_cache(self):
        user_entered_path = self.data_entry.get()

        cache_me = {}
        path = os.path.abspath(os.path.join(ABS_FILE_PICKLE, self.CACHED_FILE_PATHS))

        try:
            if self.listbox.get(0, tk.END) is not None:
                for i, k in enumerate(self.listbox.get(0, tk.END)):
                    cache_me.update({int(i): k})
                cache_me.update({len(cache_me): user_entered_path})
                # log.log(logging.INFO, 'Pickled file created at: {}'.format(path)))
            else:
                cache_me.update({len(cache_me): user_entered_path})
            with open(path, "wb") as cache:
                pickle.dump(cache_me, cache)
        except OSError as err:
            pass

    def read_source_file_path_cache(self) -> dict:
        try:
            with open(os.path.join(ABS_FILE_PICKLE, self.CACHED_FILE_PATHS), "r+b") as cache:
                retrieved_cache = pickle.load(cache)
                return retrieved_cache
        except OSError as err:
            pass

    def cache_unique(self) -> bool:
        """Checks path is not already stored in cache.

        Returns:

        """
        try:
            current_cache = self.read_source_file_path_cache().items()
            user_entered_path = self.data_entry.get()
            current_cache = [i[1] for i in current_cache]
            print(current_cache, user_entered_path)
            if user_entered_path in current_cache:
                return False
            else:
                return True
        except AttributeError as err:
            return True
        except OSError as err:
            pass

    def stop_progressbar(self):
        pass

    def verify_source_file(self):
        pass
        # checks source file is still present before populating the listbox


# make sure tkinter theme is aware of mac vs windows and linux.
