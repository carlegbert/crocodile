from hashlib import sha1
import hmac
from flask import abort, request
from functools import wraps
import ipaddress
from os import environ
import requests


"""
Helpers for security and authentication.
"""

secret = environ['CROCODILE_SECRET'].encode('utf-8')
_github_hook_ips = requests.get('https://api.github.com/meta').json()['hooks']
_github_hook_networks = [ipaddress.ip_network(ip) for ip in _github_hook_ips]


def _check_signature(req):
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
        if not _check_signature(request):
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
        if not _has_github_ip(request):
            abort(401)

        return fn(*args, **kwargs)

    return wrapper
