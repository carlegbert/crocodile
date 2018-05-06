from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    render_template,
    request
)
from subprocess import Popen

from crocodile import auth
from crocodile.hooks import hooks


app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return 'Stub of the dashboard part of the application- TODO much later.'


@app.route('/build', methods=['POST'])
@auth.signature_required
@auth.github_ip_required
def build():
    hook_type = request.headers['X-GitHub-Event']
    action_hooks = hooks.get(hook_type)
    if not action_hooks:
        abort(404)

    data = request.get_json()
    ref = data['ref']
    branch_hook = action_hooks.get(ref)
    if not branch_hook:
        abort(404)

    Popen(branch_hook, shell=True)
    return make_response('success', 200)


@app.errorhandler(404)
def not_found(e):
    if request.method == 'GET':
        return render_template('404.html'), 404

    return make_response(jsonify({'message': 'Not found.'}), 404)


@app.errorhandler(500)
def server_error(e):
    if request.method == 'GET':
        return render_template('500.html'), 404

    return make_response(jsonify({'message': 'An unexpected error occurred.'}),
                         404)


@app.errorhandler(401)
def authentication_failed(e):
    return make_response(jsonify({'message': 'Authorization denied.'}), 401)
