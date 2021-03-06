from flask import current_app, jsonify, make_response


def register(app):
    @app.errorhandler(404)
    def not_found(e):
        current_app.logger.warn('Not found')

        return make_response(jsonify({'message': 'Not found.'}), 404)

    @app.errorhandler(500)
    def server_error(e):
        current_app.logger.error(str(e))
        return make_response(jsonify({'message':
                                      'An unexpected error occurred.'}), 404)

    @app.errorhandler(401)
    def authentication_failed(e):
        current_app.logger.warn('Authentication failure')
        return make_response(jsonify({'message': 'Authorization denied.'}),
                             401)

    @app.errorhandler(405)
    def method_not_allowed(e):
        current_app.logger.warn('Method not allowed')
        return make_response(jsonify({'message': 'Method not allowed.'}), 405)
