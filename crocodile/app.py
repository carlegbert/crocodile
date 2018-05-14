from flask import Flask, render_template

from crocodile import errorhandlers
from crocodile.consumers import load_consumers
from crocodile.extensions import init_extensions
from crocodile.hook import hook
from crocodile.logging import log_request


def create_app(settings_override=None):
    app = Flask(__name__)
    init_extensions(app)

    app.config.from_pyfile('config.py')

    if settings_override is not None:
        app.config.update(settings_override)

    load_consumers(app.config['HOOKSFILE'])

    errorhandlers.register(app)
    app.register_blueprint(hook)

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    @log_request
    def index():
        return render_template('index.html')

    return app
