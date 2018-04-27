from flask import Flask, make_response, redirect, request, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))

    return make_response(200)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return 'Stub of the dashboard part of the application- TODO much later.'
