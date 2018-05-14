from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    make_response,
    request
)

from crocodile import auth
from crocodile.logging import log_request
from .task import celery_build
from crocodile.consumers import find_consumer


hook = Blueprint('hook', __name__)


@hook.route('/build', methods=['POST'])
@log_request
@auth.signature_required
@auth.valid_ip_required
def build():
    data = request.get_json()
    ref = data['ref']
    event_type = request.headers.get('X-GitHub-Event')

    consumer = find_consumer(event_type, ref)
    if not consumer:
        abort(404)

    if not current_app.config['TESTING']:
        current_app.logger.info('Build initiated for %s:%s:%s'
                                % (event_type, ref, consumer))
        celery_build.delay(consumer)

    return make_response(jsonify({'message': 'Hook consumed.'}), 202)
