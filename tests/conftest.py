import pytest


@pytest.fixture(scope='session')
def app():
    from oracles.server import app
    return app


@pytest.fixture
def client():
    from oracles.server import app
    with app.test_client() as client:
        yield client


@pytest.fixture
def main():
    from oracles.main import main
    return main


@pytest.fixture
def text():
    return 'diminishment of faerieland kills civilization'


@pytest.fixture
def reversal():
    return 'diminishment of civilization kills faerieland'


@pytest.fixture
def invalid():
    return 'is not a valid choice'
