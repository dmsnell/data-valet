import pathlib
import platform
import tkinter as tk
from tkinter import filedialog

from valet.lib import strings as i18n
import valet.gui.platform_compat
from valet.gui import app_store


class ValetApp(tk.Frame):
    master: tk.Tk
    store: app_store.AppStore

    def __init__(self, master):
        self.master = master
        self.store = app_store.AppStore()
        super().__init__(self.master)
        self.setup_app()

    def setup_app(self):
        self.master.title(i18n.APP_TITLE)
        self.master.geometry('800x600')
        self.main_window = tk.Frame(master=self.master)
        self.main_window.pack()

        match platform.system():
            case 'Darwin':
                self.replace_system_menu_on_osx()

        def choose_project_directory():
            selected_directory = filedialog.askdirectory(
                initialdir=self.store.get('project_directory', valet.gui.platform_compat.get_user_data_directory()),
                title='Choose a project directory'
            )
            if '' != selected_directory:
                self.project_directory = selected_directory
                self.store.set('project_directory', selected_directory)

            self.master.focus_set()

        button = tk.Button(master=self.main_window, text="Choose Project Directory", command=choose_project_directory)
        button.pack()

    def command_quit(self):
        self.event_quit(None)

    def event_quit(self, event):
        self.quit()

    def quit(self):
        self.master.destroy()

    def replace_system_menu_on_osx(self):
        menu = tk.Menu()
        python_menu = tk.Menu(menu, name='apple')
        menu.add_cascade(menu=python_menu)
        self.master['menu'] = menu
        python_menu.destroy()

        # App-name menu
        app_menu = tk.Menu(menu)
        menu.add_cascade(menu=app_menu, label=i18n.APP_TITLE)
        app_menu.add_command(label='About {i18n.APP_TITLE}')
        app_menu.add_separator()
        app_menu.add_command(label='Settings…')
        app_menu.add_separator()
        app_menu.add_command(label=f'Quit {i18n.APP_TITLE}', command=self.command_quit)
        # File menu
        file_menu = tk.Menu(menu)
        menu.add_cascade(menu=file_menu, label='File')
        file_menu.add_command(label='New…')
        file_menu.add_command(label='Open…')
        # Help menu
        help_menu = tk.Menu(menu)
        menu.add_cascade(menu=help_menu, label='Help')
        help_menu.add_command(label=f'{i18n.APP_TITLE} Help')

        self.master.bind('<Command-q>', self.event_quit)
        self.main_window.focus()


def run_valet_app():
    root_window = tk.Tk()
    ValetApp(root_window)
    root_window.mainloop()


if __name__ == '__main__':
    run_valet_app()
