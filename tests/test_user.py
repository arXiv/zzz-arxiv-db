import requests
import os
from modapi.auth import user_jwt

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

USER_ID = 246231  # Brandon, mod of q-bio.CB and q-bio.NC


def test_auth():
    res = requests.get(BASE_URL + "/me")
    assert res.status_code == 401  # Should be auth protected

    cookies = {'ARXIVNG_SESSION_ID': user_jwt(0)}
    res = requests.get(
        BASE_URL + "/me",
        cookies = cookies
    )
    assert res.status_code == 401  # should not get even with bogus SESSION_ID


def test_holds():
    cookies = {'ARXIVNG_SESSION_ID': user_jwt(USER_ID)}
    res = requests.get(
        BASE_URL + "/me",
        cookies = cookies
        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None    
    user = res.json()
    assert user is not None
    assert 'name' in user and user['name'] == "Brandon Barker"
    assert 'is_moderator' in user and user['is_moderator']
    assert 'is_admin' in user
    assert 'moderated_archives' in user
    assert 'moderated_categories' in user
    

