from modapi.auth import user_jwt

USER_ID = 246231  # Brandon, mod of q-bio.CB and q-bio.NC


def test_auth(client):
    res = client.get("/me")
    assert res.status_code == 401  # Should be auth protected

    res = client.get("/me", cookies={'ARXIVNG_SESSION_ID': 'BOGUS'})
    assert res.status_code == 401  # should not get even with bogus SESSION_ID

    res = client.get("/me", cookies={'ARXIVNG_SESSION_ID': user_jwt(0)})
    assert res.status_code == 401  # should not get even with bogus SESSION_ID


def test_holds(client):
    res = client.get("/me", cookies={'ARXIVNG_SESSION_ID': user_jwt(USER_ID)})
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert res.json() is not None
    user = res.json()
    assert user is not None
    assert 'name' in user and user['name'] == "Brandon Barker"
    assert 'is_moderator' in user and user['is_moderator']
    assert 'is_admin' in user
    assert user['moderated_archives'] == ['q-bio']
    assert user['moderated_categories'] == ['q-bio.CB', 'q-bio.NC']
