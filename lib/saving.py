from flask import current_app
import os


def get_last_number() -> int:
    """Return last number of file in directory with saved files."""

    path = current_app.config["TEXT_PATH"]
    _, _, list_names = next(os.walk(path))
    list_files_text = []

    for file_name in list_names:
        if ".txt" in file_name:
            list_files_text.append(file_name)

    if len(list_files_text) == 0:
        return -1

    last_str = list_files_text[-1]
    str_number = last_str.split(".")[0]
    last_number = int(str_number)

    return last_number


def get_full_file_name(name: str) -> str:
    """Return full path of file with text."""

    return os.path.join(current_app.config["TEXT_PATH"], name + ".txt")


def get_full_keywords_name(name: str) -> str:
    """Return full path of file with keywords."""

    return os.path.join(current_app.config["KEY_PATH"], name + ".json")


def save_new(text: str, keywords_raw: str):
    """Save text and keywords (must be as str format, for example as json)."""
    name = str(get_last_number() + 1)

    with open(get_full_file_name(name), "w", encoding="utf-8") as text_file:
        text_file.write(text)

    with open(get_full_keywords_name(name), "w", encoding="utf-8") as key_file:
        key_file.write(keywords_raw)
