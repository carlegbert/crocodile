from hashlib import sha1
import hmac
from flask import abort, request
from functools import wraps
from os import environ


"""
Helpers for security and authentication.
"""

secret = environ['CROCODILE_SECRET'].encode('utf-8')


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
