from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    render_template,
    request
)

from crocodile import auth, consumers, errorhandlers
from crocodile.extensions import init_extensions
from crocodile.logging import log_request
from crocodile.task import celery_build


def create_app(settings_override=None):
    app = Flask(__name__)
    init_extensions(app)

    app.config.from_pyfile('config.py')

    if settings_override is not None:
        app.config.update(settings_override)

    consumers.load_consumers(app.config['HOOKSFILE'])

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
        data = request.get_json()
        ref = data['ref']
        event_type = request.headers.get('X-GitHub-Event')

        consumer = consumers.find_consumer(event_type, ref)
        if not consumer:
            abort(404)

        if not app.config['TESTING']:
            app.logger.info('Build initiated for %s:%s:%s'
                            % (event_type, ref, consumer))
            celery_build.delay(consumer)

        return make_response(jsonify({'message': 'Hook consumed.'}), 202)

    return app
