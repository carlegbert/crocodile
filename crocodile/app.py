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
    hook_name = request.headers['X-GitHub-Event']
    hook = hooks.get(hook_name)
    if not hook:
        abort(404)

    Popen(hook, shell=True)
    return make_response('success', 200)
