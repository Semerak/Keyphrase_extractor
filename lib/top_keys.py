import json
import os
from flask import current_app

from lib.prefix_tree import PrefixTree


def list_top_keys() -> list:
    """Return list of top-used saved keywords"""
    top = PrefixTree()

    path = current_app.config["KEY_PATH"]
    _, _, list_files = next(os.walk(path))

    for file_name in list_files:
        if ".json" in file_name:
            table = []
            file_path = os.path.join(path, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                table = json.loads(file.read())
            for line in table:
                top.inc(line["word"])

    return top.list(True)
