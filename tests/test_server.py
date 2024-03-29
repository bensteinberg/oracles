from flask import json


def test_redirects(client):
    rv = client.get('/oracles', follow_redirects=True)
    assert rv.status_code == 200
    rv = client.get('/oracles/angst', follow_redirects=True)
    assert rv.status_code == 200


def test_root(client):
    rv = client.get('/')
    assert rv.status_code == 404


def test_roll(client, text):
    rv = client.get('/oracles/angst/1/1/1/1/1/1')
    assert rv.status_code == 200
    assert bytes(text, 'utf8') in rv.data


def test_bad_oracle(client, invalid):
    rv = client.get('/oracles/x', follow_redirects=True)
    assert rv.status_code == 400
    assert bytes(invalid, 'utf8') in rv.data


def test_api(client, text):
    rv = client.get('/oracles/api/v1/angst/1/1/1/1/1/1')
    assert rv.status_code == 200
    assert json.loads(rv.data)['text'] == text


def test_api_random_roll(client):
    rv = client.get('/oracles/api/v1/angst', follow_redirects=True)
    assert rv.status_code == 200
    assert 'text' in json.loads(rv.data)


def test_api_random_oracle(client):
    rv = client.get('/oracles/api/v1', follow_redirects=True)
    assert rv.status_code == 200
    assert 'text' in json.loads(rv.data)


def test_api_bad_oracle(client, invalid):
    rv = client.get('/oracles/api/v1/x', follow_redirects=True)
    assert rv.status_code == 400
    assert invalid in json.loads(rv.data)['error']


def test_api_bad_roll(client):
    rv = client.get('/oracles/api/v1/angst/1/1/1/1/1/7', follow_redirects=True)
    assert rv.status_code == 400
    assert json.loads(rv.data)['error'] == 'You must use 6d6.'
