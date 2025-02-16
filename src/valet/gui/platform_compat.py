from pathlib import Path

def get_user_data_directory():
    return Path.home() / 'Documents'
