from flask import Flask
from config import Ripple
from config.app_config import init_config


def _initialize_flask_app(env):

    if Ripple.Config.ENV in ['development', 'test']:
        # Here we are using flask to serve static files locally.
        # Not necessary in prod because nginx serves static files
        # rather than flask
        app = Flask(
            __name__,
            static_url_path='',
            static_folder='../client/dist/'
        )

        def index():
            return app.send_static_file('index.html')

        app.add_url_rule('/', 'index', index)
        return app
    else:
        return Flask(__name__)


def create_app(env):
    init_config(env)

    app = _initialize_flask_app(env)
    return app
