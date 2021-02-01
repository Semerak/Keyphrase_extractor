import os, glob
from lib.config_data import textpath, keypath


def delete_all_saves():
    list_files = glob.glob(textpath() + "*.txt")
    list_files.extend(glob.glob(keypath() + "*.json"))
    for path in list_files:
        os.remove(path)
