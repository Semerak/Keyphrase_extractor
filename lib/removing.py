import os

from flask import current_app


def delete_all_saves():
    """Delete all saved files"""

    path = current_app.config["TEXT_PATH"]
    _, _, list_names = next(os.walk(path))
    list_files = []

    for file_name in list_names:
        if ".txt" in file_name:
            list_files.append(os.path.join(path, file_name))

    path = current_app.config["KEY_PATH"]
    _, _, list_names = next(os.walk(path))
    list_files_key = []

    for file_name in list_names:
        if ".json" in file_name:
            list_files_key.append(os.path.join(path, file_name))

    list_files.extend(list_files_key)

    for path in list_files:
        os.remove(path)
