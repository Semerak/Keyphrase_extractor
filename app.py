import os
from flask import Flask, request, render_template
from flask.blueprints import Blueprint
from endpoints import *




def create_app():
    secret = os.urandom(32)
    _app = Flask(__name__)
    _app.config["SECRET_KEY"] = secret
    _app.register_blueprint(blp)
    return _app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=80, host="127.0.0.1")
