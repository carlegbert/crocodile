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

from crocodile import auth, hooks


def create_app(settings_override=None):
    app = Flask(__name__)

    if settings_override is not None:
        app.config.update(settings_override)
    else:
        secret = environ.get('CROCODILE_SECRET').encode('utf-8')
        app.config['CROCODILE_SECRET'] = secret
        app.config['TEST_MODE'] = False
        app.config['HOOKS'] = hooks.load_hooks()

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    def index():
        return 'TODO: this'

    @app.route('/build', methods=['POST'])
    @auth.signature_required
    @auth.valid_ip_required
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
            Popen(branch_hook, shell=True)
        return make_response(jsonify({'message': 'Hook consumed.'}),
                             202)

    @app.errorhandler(404)
    def not_found(e):
        if request.method == 'GET':
            return render_template('404.html'), 404

        return make_response(jsonify({'message': 'Not found.'}), 404)

    @app.errorhandler(500)
    def server_error(e):
        if request.method == 'GET':
            return render_template('500.html'), 404

        return make_response(jsonify({'message':
                                      'An unexpected error occurred.'}), 404)

    @app.errorhandler(401)
    def authentication_failed(e):
        return make_response(jsonify({'message': 'Authorization denied.'}),
                             401)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return make_response(jsonify({'message': 'Method not allowed.'}), 405)

    return app
