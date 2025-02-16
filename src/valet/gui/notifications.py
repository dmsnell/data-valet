import os
import ctypes
import subprocess
import shlex
import platform

def toast(message):
    match platform.system():
        case 'Darwin':  # macOS
            subprocess.run(["osascript", "-e", f'display notification "{shlex.quote(message)}"'])
        case 'Windows':  # Windows
            ctypes.windll.user32.MessageBoxW(0, message, "Notification", 0)
        case 'Linux':  # Linux
            subprocess.run(["notify-send", "Notification", message])
