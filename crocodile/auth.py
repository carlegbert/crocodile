from hashlib import sha1
import hmac
from flask import abort, current_app, request
from functools import wraps
import ipaddress
import requests


_valid_networks = None


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


def _get_valid_networks():
    global _valid_networks

    if current_app.config['TESTING']:
        return [ipaddress.ip_network('127.0.0.1')]

    if not _valid_networks:
        ips = requests.get('https://api.github.com/meta').json()['hooks']
        _valid_networks = [ipaddress.ip_network(ip) for ip in ips]
    return _valid_networks


def _ip_from_request():
    #  remote_addr is not present on request when using nginx proxy, and
    #  uwsgi turns HTTP_X_REAL_IP into `<ip>, <ip>`
    if current_app.config['TESTING']:
        return request.remote_addr
    return request.environ['HTTP_X_REAL_IP'].split(',')[0]


def _has_valid_ip():
    valid_networks = _get_valid_networks()
    ip = ipaddress.ip_address(_ip_from_request())

    for nw in valid_networks:
        if ip in nw:
            return True
    return False


def valid_ip_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if _has_valid_ip():
            return fn(*args, **kwargs)

        abort(401)
    return wrapper
