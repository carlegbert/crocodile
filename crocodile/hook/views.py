from subprocess import Popen
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
from .util import get_hooks


hook = Blueprint('hook', __name__)


@hook.route('/build', methods=['POST'])
@log_request
@auth.signature_required
@auth.valid_ip_required
def build():
    hook_type = request.headers['X-GitHub-Event']
    action_hooks = get_hooks().get(hook_type)
    if not action_hooks:
        abort(404)

    data = request.get_json()
    ref = data['ref']
    branch_hook = action_hooks.get(ref)
    if not branch_hook:
        abort(404)

    if not current_app.config['TESTING']:
        current_app.logger.info('Build initiated for %s:%s:%s'
                                % (hook_type, ref, branch_hook))
        Popen(branch_hook, shell=True)

    return make_response(jsonify({'message': 'Hook consumed.'}), 202)
