
import json
import pathlib

from valet.gui import appdirs, notifications
from valet.lib import strings as i18n

class AppStore:
    """
    Interacts with persisted app state.

    The purpose of this class is to store app state in a way that persists even after the app is restarted.
    This allows users to avoid repeating steps they previously did.

    Examples:
        app_store = AppStore()
        app_store.set('theme', 'dark')
        print(app_store.get('theme'))  # Output: dark

        # Get a value with a default if it doesn't exist
        print(app_store.get('theme', 'light'))  # Output: dark

    """
    def __init__(self):
        this_app = appdirs.AppDirs(i18n.APP_SLUG, i18n.APP_AUTHOR, i18n.APP_VERSION)
        app_config_dir = pathlib.Path(this_app.user_config_dir)
        try:
            app_config_dir.mkdir(parents=True, exist_ok=True)
        except FileExistsError as e:
            notifications.toast(f'Tried to store app settings in "{self.app_config_dir}" but that path exists and is not a readable directory.')
            raise(e)

        self.settings_file = app_config_dir / 'settings.json'
        self.settings_file.touch(exist_ok=True)

        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except json.JSONDecodeError:
            self.settings = {}

    def set(self, key, value):
        self.settings[key] = value
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def get(self, key, default=None):
        return self.settings.get(key, default)
