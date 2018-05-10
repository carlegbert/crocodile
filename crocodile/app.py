from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    render_template,
    request
)
from os import environ
from subprocess import Popen

from crocodile import auth, hooks, errorhandlers, logger


def create_app(settings_override=None):
    app = Flask(__name__)

    if settings_override is not None:
        app.config.update(settings_override)
    else:
        secret = environ.get('CROCODILE_SECRET', '').encode('utf-8')
        app.config['CROCODILE_SECRET'] = secret
        app.config['TEST_MODE'] = False
        app.config['HOOKS'] = hooks.load_hooks()
        logger.register_logger(app)

    errorhandlers.register(app)

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    @logger.log_request
    def index():
        return render_template('index.html')

    @app.route('/build', methods=['POST'])
    @auth.signature_required
    @auth.valid_ip_required
    @logger.log_request
    def build():
        hook_type = request.headers['X-GitHub-Event']
        action_hooks = app.config['HOOKS'].get(hook_type)
        if not action_hooks:
            abort(404)

        data = request.get_json()
        ref = data['ref']
        branch_hook = action_hooks.get(ref)
        if not branch_hook:
            abort(404)

        if not app.config['TEST_MODE']:
            app.logger.info('Build initiated for %s:%s:%s'
                            % (hook_type, ref, branch_hook))
            Popen(branch_hook, shell=True)
        return make_response(jsonify({'message': 'Hook consumed.'}),
                             202)

    return app
