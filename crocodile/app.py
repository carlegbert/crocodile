from flask import Flask, abort, make_response, redirect, request, url_for
from util import check_signature


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))

    if check_signature(request):
        return make_response('Accepted', 200)

    abort(404)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return 'Stub of the dashboard part of the application- TODO much later.'
