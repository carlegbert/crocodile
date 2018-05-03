import pytest

from crocodile.app import app as _app


@pytest.fixture
def app():
    yield _app


@pytest.fixture
def client(app):
    yield app.test_client()
