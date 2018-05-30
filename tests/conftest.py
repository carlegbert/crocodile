import json
from hashlib import sha1
import hmac
from os import path
import pytest

from crocodile.app import create_app

TEST_SECRET = 'test_secret'


@pytest.fixture
def app():
    test_config = {
        'CROCODILE_SECRET': TEST_SECRET,
        'TESTING': True,
        'CONSUMERSFILE': path.join(path.dirname(__file__), 'consumers.yml')
    }
    app = create_app(test_config)
    return app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def secret():
    return TEST_SECRET.encode('utf-8')


@pytest.fixture
def request_json():
    return json.dumps({
        'ref': 'test_branch',
        'repository': {'full_name': 'test_consumer'}
    })


@pytest.fixture
def signature(secret, request_json):
    return hmac.new(secret, request_json.encode('utf-8'), sha1).hexdigest()


@pytest.fixture
def headers(signature):
    return {'X-Hub-Signature': 'sha1=' + signature,
            'X-Github-Event': 'test_event'}
