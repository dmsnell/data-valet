import platform
import tkinter as tk

from valet.lib import strings as i18n


class ValetApp(tk.Frame):
    master: tk.Tk

    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        self.setup_app()

    def setup_app(self):
        self.master.title(i18n.APP_TITLE)
        self.main_window = tk.Frame(master=self.master)
        label = tk.Label(master=self.main_window, text="Valet")
        label.pack()
        self.main_window.pack()

        match platform.system():
            case 'Darwin':
                self.replace_system_menu_on_osx()

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
        app_menu.add_command(label=f'About {i18n.APP_TITLE}')
        app_menu.add_separator()
        app_menu.add_command(label=f'Settings…')
        app_menu.add_separator()
        app_menu.add_command(label=f'Quit {i18n.APP_TITLE}', command=self.event_quit)
        # File menu
        file_menu = tk.Menu(menu)
        menu.add_cascade(menu=file_menu, label=f'File')
        file_menu.add_command(label=f'New…')
        file_menu.add_command(label=f'Open…')
        # Help menu
        help_menu = tk.Menu(menu)
        menu.add_cascade(menu=help_menu, label='Help')
        help_menu.add_command(label=f'{i18n.APP_TITLE} Help')

        self.master.bind('<Command-q>', self.event_quit)
        self.main_window.focus()


def run_valet_app():
    root_window = tk.Tk()
    app = ValetApp(root_window)
    root_window.mainloop()


if __name__ == '__main__':
    run_valet_app()
