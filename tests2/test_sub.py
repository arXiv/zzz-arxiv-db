from modapi.auth import user_jwt

SUB_ID_1 = 1137914


def test_auth(client):
    res = client.get(f"/submission/{SUB_ID_1}")
    assert res.status_code == 401  # Should be auth protected

    res = client.get("/submissions")
    assert res.status_code == 401  # Should be auth protected


def test_subs(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/submissions", cookies=cookies)
    assert (
        res.status_code != 401
    )  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None
    sub = res.json()
    assert type(sub) == list


def test_sub(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get(f"/submission/{SUB_ID_1}", cookies=cookies)
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None
    sub = res.json()

    assert "status" in sub
    assert type(sub["status"]) == str

    assert sub["submitter"]["name"] == "Brandon Barker"

    assert "classifier_scores" in sub["categories"]
    assert sub["categories"]["classifier_scores"]
    assert sub["comment_count"]

    assert sub["categories"]["new_crosses"] == []
    assert sub["categories"]["submission"]["secondary"] == []
    assert sub["categories"]["submission"]["primary"] == 'q-bio.CB'


def test_cross(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get(f"/submission/3400", cookies=cookies)
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None
    sub = res.json()
    assert sub["type"] == 'cross'
    new_cross = 'hep-ph'
    assert sub["categories"]["new_crosses"] == [new_cross]
    assert new_cross not in sub["categories"]["submission"]["secondary"]
    assert sub["categories"]["submission"]["secondary"] == ['cs.DD']


def test_rep(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get(f"/submission/3401", cookies=cookies)
    assert res.status_code == 200
    sub = res.json()
    assert sub["type"] == 'rep'
    assert sub["categories"]["submission"]["primary"] == 'hep-ph'
    assert sub["categories"]["submission"]["secondary"] == ['hep-ex']


def test_not_found(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC

    res = client.get("/submission/0", cookies=cookies)
    assert (
        res.status_code != 200
    )  # look for a missing SUB id in the test data (FYI, this exists in the real data)
    assert res.status_code != 500
