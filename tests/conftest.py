import pytest

from crocodile.app import create_app


@pytest.fixture
def app():
    test_config = {
        'CROCODILE_SECRET': 'test_secret'.encode('utf-8'),
        'TESTING': True,
        'HOOKS': {
            'test_event': {'test_branch': 'test_script'}
        }
    }
    app = create_app(test_config)
    return app


@pytest.fixture
def client(app):
    yield app.test_client()
