from flask import jsonify, make_response, render_template, request


def register(app):
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
