from os import path
import pytest

from crocodile.app import create_app


@pytest.fixture
def app():
    test_config = {
        'CROCODILE_SECRET': 'test_secret'.encode('utf-8'),
        'TESTING': True,
        'HOOKSFILE': path.join(path.dirname(__file__), 'test_hooks.yml')
    }
    app = create_app(test_config)
    return app


@pytest.fixture
def client(app):
    yield app.test_client()
