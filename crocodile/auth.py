from hashlib import sha1
import hmac
from os import environ

"""
Helpers for security and authentication.
"""

secret = environ['CROCODILE_SECRET'].encode('utf-8')


def check_signature(req):
    try:
        signature = req.headers.get('X-Hub-Signature').split('=')[1]
        data = req.data
    except (AttributeError, IndexError):
        return False
    digest = hmac.new(secret, data, sha1).hexdigest()
    return hmac.compare_digest(signature, digest)
