import tkinter as tk
from valet.lib import strings as i18n

class AboutDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About")
        self.geometry("180x140")
        self.resizable(False, False)
        self.transient(parent)  # Make the dialog a child of the main window
        self.grab_set()  # Make the dialog modal

        # Calculate the position of the dialog
        x = parent.winfo_x() + (parent.winfo_width() - 140) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 200) // 2
        self.geometry(f"+{x}+{y}")

        name_label = tk.Label(self, text=i18n.APP_TITLE)
        name_label.pack(pady=10)

        # Create a label to display the version number
        version_label = tk.Label(self, text=f"Version: {i18n.APP_VERSION}")
        version_label.pack(pady=10)

        # Create a text box to display the dedication paragraph
        dedication_text = tk.Label(self, text="For Val")
        dedication_text.pack(pady=10)

        # Focus on the dialog
        self.focus_set()
        self.wait_window()
