import logging
from config import Config
from endpoints import *


def create_app():
    logging.basicConfig(level=logging.INFO)
    _app = Flask(__name__)
    _app.config.from_object(Config())
    _app.register_blueprint(blp)
    return _app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, port=80, host="127.0.0.1")
