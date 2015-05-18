from flask import Flask
from config import Ripple
from config.app_config import init_config, init_cassandra


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


def _register_blueprints(app):
    from api.videos_api import videos
    app.register_blueprint(videos, url_prefix='/api/v1/videos')
    return app


def create_app(env):
    init_config(env)
    init_cassandra(env)

    app = _initialize_flask_app(env)
    app = _register_blueprints(app)
    return app
