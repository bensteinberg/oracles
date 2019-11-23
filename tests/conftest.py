import pytest


@pytest.fixture
def app():
    from server import app
    return app


@pytest.fixture
def client():
    from server import app
    with app.test_client() as client:
        yield client


@pytest.fixture
def text():
    return 'diminishment of faerieland kills civilization'


@pytest.fixture
def reversal():
    return 'diminishment of civilization kills faerieland'


@pytest.fixture
def invalid():
    return 'is not a valid choice'
