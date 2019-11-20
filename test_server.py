import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_redirects(client):
    rv = client.get('/oracles', follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get('/oracles/angst', follow_redirects=True)
    assert rv.status_code == 200


def test_root(client):
    rv = client.get('/')
    assert rv.status_code == 404


def test_roll(client):
    rv = client.get('/oracles/angst/1/1/1/1/1/1')
    assert rv.status_code == 200
    assert b'diminishment of faerieland kills civilization' in rv.data
