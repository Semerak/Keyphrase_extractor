from config_data import keypath
import glob
import json
from Prefix_tree import PrefixTree


def top_keys():
    top = PrefixTree()
    list_files = glob.glob(keypath() + "*.json")
    for file_path in list_files:
        table = []
        with open(file_path, 'r', encoding='utf-8') as file:
            table = json.loads(file.read())
        for line in table:
            top.inc(line['word'])
    return top.list(True)
