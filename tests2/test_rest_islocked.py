from typing import Optional

import pytest
from pytest_mock import mocker

from modapi.auth import auth_user
from modapi.collab.lockstore import Lock


@pytest.fixture
def lock_client(no_db_client):
    async def override_auth(rawauth: Optional[str] = None):
        return {'override_auth': 'this is mocked'}
    
    no_db_client.add_override(auth_user, override_auth)
    return no_db_client


def test_locked(mocker, lock_client):
    resp = lock_client.get('/submission/1234/is_locked')
    assert resp
    data = resp.json()
    assert data
    assert data['is_locked'] is False

    mocked_cil_fn = mocker.patch('modapi.rest.islocked.check_if_locked')
    mocked_cil_fn.return_value = Lock(username='Vivian', sid=1234)
    resp = lock_client.get('/submission/1234/is_locked')
    assert resp
    data = resp.json()
    assert data
    assert data['is_locked'] is True
    assert data['username'] == 'Vivian'
