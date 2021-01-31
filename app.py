import os
from flask import Flask, request, render_template
from flask.blueprints import Blueprint
from lib.keywords_extractor import keywords
from lib.saving import save_new
from lib import top_keys, wikipedia_search
import json

blp = Blueprint("Main", __name__)


@blp.route("/")
@blp.route("/add/", methods=["post", "get"])
def add():
    """First enter to page add"""
    message = "Insert text"

    return render_template(
        "add.html", message=message, save_flag=False, wiki_flag=False
    )


@blp.route("/add/find", methods=["post", "get"])
def add_find():
    """Extract keywords."""
    message = "You can make a wikipedia search for keywords (may take a while)."
    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("input_text")

    if input_text != "":
        table = keywords(input_text)

    return render_template(
        "add.html",
        message=message,
        save_flag=True,
        wiki_flag=True,
        text=input_text,
        table=table,
        table_json=json.dumps(table),
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
    table = []

    if request.method == "POST":
        input_text = request.form.get("input_text")
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
    )


@blp.route("/top_key/", methods=["get"])
def top_keys_page():
    """Make a list of top-used keywords."""
    table = top_keys.list_top_keys()
    return render_template("top.html", table=table)


def create_app():
    secret = os.urandom(32)
    _app = Flask(__name__)
    _app.config["SECRET_KEY"] = secret
    _app.register_blueprint(blp)
    return _app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=80, host="127.0.0.1")
