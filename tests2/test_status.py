import pytest

def test_status(client):
    assert client.get('/status').status_code == 200

def test_version(client):
    assert client.get('/version').status_code == 200
