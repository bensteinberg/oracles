import pytest


@pytest.fixture
def app():
    from app.server import app
    return app


@pytest.fixture
def client():
    from app.server import app
    with app.test_client() as client:
        yield client


@pytest.fixture
def main():
    from app.oracles import main
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


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--headless')
    return chrome_options
