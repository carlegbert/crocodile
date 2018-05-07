from hashlib import sha1
import hmac
from flask import abort, current_app, request
from functools import wraps
import ipaddress
import requests


"""
Helpers for security and authentication.
"""

_github_hook_ips = requests.get('https://api.github.com/meta').json()['hooks']
_github_hook_networks = [ipaddress.ip_network(ip) for ip in _github_hook_ips]


def _check_signature(req, secret):
    try:
        signature = req.headers.get('X-Hub-Signature').split('=')[1]
        data = req.data
    except (AttributeError, IndexError):
        return False
    digest = hmac.new(secret, data, sha1).hexdigest()
    return hmac.compare_digest(signature, digest)


def signature_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        secret = current_app.config.get('CROCODILE_SECRET')
        if not _check_signature(request, secret):
            abort(401)
        return fn(*args, **kwargs)

    return wrapper


def _has_github_ip(req):
    # Can't use req.remote_addr when using nginx proxy
    ip = ipaddress.ip_address(req.environ['HTTP_X_REAL_IP'])
    for nw in _github_hook_networks:
        if ip in nw:
            return True
    return False


def github_ip_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        allow_all_ips = current_app.config.get('TEST_MODE')
        if allow_all_ips or _has_github_ip(request):
            return fn(*args, **kwargs)

        abort(401)
    return wrapper
