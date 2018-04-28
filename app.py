from flask import Flask, make_response, redirect, request, url_for
import hmac
from hashlib import sha1
from os import environ


secret = environ['CROCODILE_SECRET']

app = Flask(__name__)


def check_signature(request):
    data = request.data
    signature = request.headers.get('X-Hub-Signature').split('=')[1]
    digest = hmac.new(secret, data, sha1).hexdigest()
    return hmac.compare_digest(signature, digest)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))

    if check_signature(request):
        make_response(200)

    return make_response(404)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return 'Stub of the dashboard part of the application- TODO much later.'
