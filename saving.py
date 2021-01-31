from config_data import textpath, keypath
import glob


def get_last_number():
    list_files = glob.glob(textpath() + "*.txt")
    if len(list_files) == 0:
        return -1
    last_str = list_files[-1]
    str_number = last_str.split('\\')[1].split(".")[0]
    last_number = int(str_number)
    return last_number


def get_full_file_name(name):
    path = textpath() + name + ".txt"
    return path


def get_full_keywords_name(name):
    path = keypath() + name + ".json"
    return path


def save_new(text, keywords_raw):
    name = str(get_last_number() + 1)
    with open(get_full_file_name(name), 'w', encoding='utf-8') as text_file:
        text_file.write(text)
    with open(get_full_keywords_name(name), 'w', encoding='utf-8') as key_file:
        key_file.write(keywords_raw)