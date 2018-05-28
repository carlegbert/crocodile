from hashlib import sha1
import hmac
from flask import abort, current_app, request
from functools import wraps
import ipaddress
import requests

from crocodile.extensions import redis_store


"""
Helpers for security and authentication.
"""


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
        secret = current_app.config.get('CROCODILE_SECRET').encode('utf-8')
        if not _check_signature(request, secret):
            abort(401)
        return fn(*args, **kwargs)

    return wrapper


def _fetch_github_networks():
    github_networks = redis_store.lrange('ghnetworks', 0, -1)
    if not github_networks:
        gh_ips = requests.get('https://api.github.com/meta').json()['hooks']
        github_networks = [ipaddress.ip_network(ip) for ip in gh_ips]
        redis_store.lpush('ghnetworks', github_networks)
    return github_networks


def _has_valid_ip(req):
    if current_app.config['TESTING']:
        return req.remote_addr == '127.0.0.1'

    github_networks = _fetch_github_networks()

    # Can't use req.remote_addr when using nginx proxy
    ip = ipaddress.ip_address(req.environ['HTTP_X_REAL_IP'])

    for nw in github_networks:
        if ip in nw:
            return True
    return False


def valid_ip_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if _has_valid_ip(request):
            return fn(*args, **kwargs)

        abort(401)
    return wrapper
