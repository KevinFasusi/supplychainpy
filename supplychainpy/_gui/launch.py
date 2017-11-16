import tkinter as tk

from supplychainpy._gui.views._home import MainWindow


def home():
    launcher = tk.Tk()
    app_launch = MainWindow(launcher)
    screen_width = app_launch.parent.winfo_screenwidth()
    screen_height = app_launch.parent.winfo_screenheight()
    app_height = 640
    app_width = 480
    app_x_pos = int((screen_width - app_width) / 3)
    app_y_pos = int((screen_height - app_height) / 2)
    app_launch.parent.geometry('{}x{}+{}+{}'.format(app_height, app_width, app_x_pos, app_y_pos))

    app_launch.parent.configure()
    launcher.mainloop()


if __name__ == '__main__':
    home()
