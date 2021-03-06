from flask import Flask, request, render_template
from lib.keywords_extractor import keywords
from lib.saving import save_new
from lib import top_keys, wikipedia_search
import json
from flask.blueprints import Blueprint
from lib.removing import delete_all_saves

blp = Blueprint("Main", __name__)


@blp.route("/")
@blp.route("/add/", methods=["post", "get"])
def add():
    """First enter to page add"""
    message = "Insert text"
    extractor_config = {"light_flag": False, "max_keys": 10, "alpha": 0.5}
    return render_template(
        "add.html",
        message=message,
        save_flag=False,
        wiki_flag=False,
        extractor_config=extractor_config,
    )


@blp.route("/add/find", methods=["post", "get"])
def add_find():
    """Extract keywords."""
    message = "You can make a wikipedia search for keywords (may take a while)."
    input_text = ""
    extractor_config = {"light_flag": False, "max_keys": 10, "alpha": 0.5}
    if request.method == "POST":
        input_text = request.form.get("input_text")
        extractor_config["light_flag"] = bool(request.form.get("light"))
        extractor_config["max_keys"] = int(request.form.get("max_keys"))
        extractor_config["alpha"] = float(request.form.get("alpha"))

    if input_text != "":
        table = keywords(input_text, extractor_config)

    return render_template(
        "add.html",
        message=message,
        save_flag=True,
        wiki_flag=True,
        text=input_text,
        table=table,
        table_json=json.dumps(table),
        extractor_config=extractor_config,
    )


@blp.route("/add/save", methods=["post", "get"])
def add_save():
    """Saving text and keywords."""
    message = ""
    keywords_raw = ""
    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("input_text")
        keywords_raw = request.form.get("keywords")

    if input_text != "":
        save_new(input_text, keywords_raw)
        message = "Saved successfully"

    return render_template(
        "add.html", message=message, save_flag=False, wiki_flag=False
    )


@blp.route("/add/wiki", methods=["post", "get"])
def add_wiki():
    """Make wiki search."""
    input_text = ""
    keywords_raw = ""
    extractor_config = {"light_flag": False, "max_keys": 10, "alpha": 0.5}
    table = []

    if request.method == "POST":
        input_text = request.form.get("input_text")
        extractor_config["light_flag"] = bool(request.form.get("light"))
        extractor_config["max_keys"] = int(request.form.get("max_keys"))
        extractor_config["alpha"] = float(request.form.get("alpha"))
        keywords_raw = request.form.get("keywords")
        keywords_list = json.loads(keywords_raw)
        table = wikipedia_search.list_summary(keywords_list)

    return render_template(
        "add.html",
        save_flag=True,
        wiki_flag=True,
        text=input_text,
        table=table,
        table_json=json.dumps(table),
        extractor_config=extractor_config,
    )


@blp.route("/top_key/", methods=["get", "post"])
def top_keys_page():
    """Make a list of top-used keywords."""
    if request.method == "POST" and request.form.get("order") == "delete":
        delete_all_saves()
    table = top_keys.list_top_keys()
    return render_template("top.html", table=table)
