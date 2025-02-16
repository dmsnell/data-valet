import pathlib
import platform
import tkinter as tk
from tkinter import filedialog

from valet.lib import strings as i18n
import valet.gui.platform_compat
from valet.gui import about_dialog, app_store


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

        self.modify_menu()

        # Check for existing project directory
        stored_dir = self.store.get('project_directory')
        project_path = pathlib.Path(stored_dir) if stored_dir else None

        if project_path and project_path.exists():
            live_project_path = self.store.bind('project_directory')
            status_label = tk.Label(self.main_window, text=f"Using project: {live_project_path.value}")
            status_label.pack()

            def update_label(new_path):
                status_label.config(text=f"Using project: {new_path}")

            live_project_path.on_change = update_label
            return  # Skip directory picker setup

        button = tk.Button(master=self.main_window, text="Open Directory", command=self.choose_project_directory)
        button.pack()

    def command_quit(self):
        self.event_quit(None)

    def choose_project_directory(self):
        selected_directory = filedialog.askdirectory(
            initialdir=self.store.get('project_directory', valet.gui.platform_compat.get_user_data_directory()),
            title='Choose a project directory'
        )
        if selected_directory:
            self.open_project(selected_directory)

        self.master.focus_set()

    def open_project(self, project_path):
        self.store.set('project_directory', project_path)
        
        recent_projects = set(self.store.get('recent_folders', []))
        recent_projects.discard(project_path)
        recent_projects = [project_path] + list(recent_projects)
        self.store.set('recent_folders', recent_projects)

    def event_quit(self, event):
        self.quit()

    def quit(self):
        self.master.destroy()

    def modify_menu(self):
        menu = tk.Menu()
        python_menu = tk.Menu(menu, name='apple')
        menu.add_cascade(menu=python_menu)
        self.master['menu'] = menu
        python_menu.destroy()

        # App-name menu
        app_menu = tk.Menu(menu)
        menu.add_cascade(menu=app_menu, label=i18n.APP_TITLE)
        app_menu.add_command(label=f'About {i18n.APP_TITLE}', command=lambda: about_dialog.AboutDialog(self.master))
        app_menu.add_separator()
        app_menu.add_command(label='Settings…')
        app_menu.add_separator()
        app_menu.add_command(label=f'Quit {i18n.APP_TITLE}', command=self.command_quit)

        # File menu
        file_menu = tk.Menu(menu)
        menu.add_cascade(menu=file_menu, label='File')
        file_menu.add_command(label='Open Folder…', command=self.choose_project_directory)
        self.master.bind('<Control-O>' if platform.system() == 'Windows' else '<Command-O>', lambda event: self.choose_project_directory())

        live_recent_folders = self.store.bind('recent_folders', [])
        recent_menu = tk.Menu(file_menu)

        def update_recent_folders(folders):
            recent_menu.delete(0, tk.END)

            for folder in folders:
                recent_menu.add_command(
                    label=folder,
                    command=lambda: self.open_project(folder)
                )

            recent_menu.add_command(
                label=i18n.CLEAR_RECENTLY_OPENED,
                command=lambda: self.store.set('recent_folders', [])
            )

        file_menu.add_cascade(menu=recent_menu, label='Open Recent')
        update_recent_folders(live_recent_folders.value)
        live_recent_folders.on_change = update_recent_folders

        # Help menu
        help_menu = tk.Menu(menu)
        menu.add_cascade(menu=help_menu, label='Help')
        help_menu.add_command(label=f'{i18n.APP_TITLE} Help')

        match platform.system():
            case 'Darwin':
                self.master.bind('<Command-q>', self.event_quit)

        self.main_window.focus()


def run_valet_app():
    root_window = tk.Tk()
    ValetApp(root_window)
    root_window.mainloop()


if __name__ == '__main__':
    run_valet_app()
