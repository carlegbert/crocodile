from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    render_template,
)

from crocodile import auth, errorhandlers
from crocodile.consumer import Consumer
from crocodile.extensions import init_extensions
from crocodile.logging import log_request


def create_app(settings_override=None):
    app = Flask(__name__)
    init_extensions(app)

    app.config.from_pyfile('config.py')

    if settings_override is not None:
        app.config.update(settings_override)

    Consumer.load(app.config['CONSUMERSFILE'])

    errorhandlers.register(app)

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    @log_request
    def index():
        return render_template('index.html')

    @app.route('/build', methods=['POST'])
    @log_request
    @auth.signature_required
    @auth.valid_ip_required
    def build():
        consumer = Consumer.find_from_request()
        if not consumer:
            abort(404)

        if not app.config['TESTING']:
            consumer.run()

        return make_response(jsonify({'message': 'Hook consumed.'}), 202)

    return app
