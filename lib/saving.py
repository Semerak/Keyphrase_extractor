from lib.config_data import textpath, keypath
import glob


def get_last_number() -> int:
    """Return last number of file in directory with saved files."""
    list_files = glob.glob(textpath() + "*.txt")

    if len(list_files) == 0:
        return -1

    last_str = list_files[-1]
    str_number = last_str.split("\\")[1].split(".")[0]
    last_number = int(str_number)

    return last_number


def get_full_file_name(name: str) -> str:
    """Return full path of file with text."""

    return textpath() + name + ".txt"


def get_full_keywords_name(name: str) -> str:
    """Return full path of file with keywords."""

    return keypath() + name + ".json"


def save_new(text: str, keywords_raw: str):
    """Save text and keywords (must be as str format, for example as json)."""
    name = str(get_last_number() + 1)

    with open(get_full_file_name(name), "w", encoding="utf-8") as text_file:
        text_file.write(text)

    with open(get_full_keywords_name(name), "w", encoding="utf-8") as key_file:
        key_file.write(keywords_raw)
