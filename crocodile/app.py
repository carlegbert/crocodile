from os import path
from flask import Flask, render_template

from crocodile import errorhandlers, logger
from crocodile.hook import hook, load_hooks

YAML_PATH = path.join(path.dirname(__file__), 'hooks.yml')


def create_app(settings_override=None):
    app = Flask(__name__)
    logger.register_logger(app)

    app.config.from_pyfile('application.cfg')
    app.config['HOOKS'] = load_hooks(YAML_PATH)

    if settings_override is not None:
        app.config.update(settings_override)

    errorhandlers.register(app)
    app.register_blueprint(hook)

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    @logger.log_request
    def index():
        return render_template('index.html')

    return app
