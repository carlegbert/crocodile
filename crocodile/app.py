from flask import Flask, abort, make_response, request
from subprocess import Popen

from crocodile import auth
from crocodile.hooks import hooks


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Stub of the dashboard part of the application- TODO much later.'


@app.route('/build', methods=['POST'])
@auth.signature_required
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
