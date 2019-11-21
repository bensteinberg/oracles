import pytest


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv('ORACLES', 'data_sample')
