import pytest


@pytest.fixture
def app():
    from server import app
    return app
