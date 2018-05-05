from flask import Flask, make_response, request

from crocodile import auth, hooks


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Stub of the dashboard part of the application- TODO much later.'


@app.route('/build', methods=['POST'])
@auth.signature_required
def build():
    return 'wahee'
