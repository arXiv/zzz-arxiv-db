import pytest
from typing import Optional

from pytest_mock import mocker

from fastapi.testclient import TestClient

from modapi.auth import auth_user
from modapi.rest.rest_app import fast_app
from modapi.collab.lockstore import Lock

@pytest.fixture
def the_app():

    async def override_auth(rawauth: Optional[str] = None):
        return {'override_auth': 'this is mocked'}
    fast_app.dependency_overrides[auth_user] = override_auth

    return TestClient(fast_app)


def test_locked(mocker, the_app):
    mocked_cil_fn = mocker.patch('modapi.rest.islocked.check_if_locked')
    mocked_cil_fn.return_value = Lock(username='Vivian',sid=1234)

    resp = the_app.get('/submission/1234/is_locked')
    assert resp
    data = resp.json()
    assert data
    assert data['is_locked'] is True
    assert data['username'] == 'Vivian'


def test_not_locked(mocker, the_app):
    resp = the_app.get('/submission/1234/is_locked')
    assert resp
    data = resp.json()
    assert data
    assert data['is_locked'] is False

