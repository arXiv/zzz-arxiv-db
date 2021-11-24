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



def test_sub_with_proposals(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/submission/4400", cookies=cookies)
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None
    sub = res.json()

    assert "status" in sub
    assert type(sub["status"]) == str

    sys_prop = [prop for prop in sub["categories"]["proposals"]["resolved"] if prop["proposal_id"] == 203909]
    assert sys_prop
    assert sys_prop[0]["is_system_proposal"]


def test_cross(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/submission/3400", cookies=cookies)
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None
    sub = res.json()
    assert sub["type"] == 'cross'
    new_cross = 'hep-ph'
    assert sub["categories"]["new_crosses"] == [new_cross]
    assert new_cross in sub["categories"]["submission"]["secondary"] # ARXIVNG-4216
    assert 'hep-ph' in sub["categories"]["submission"]["secondary"]
    assert 'cs.DD'  in sub["categories"]["submission"]["secondary"]


def test_rep(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/submission/3401", cookies=cookies)
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


def test_classifier_json(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/submission/1234888", cookies=cookies)
    assert res.status_code == 200
    assert 'error' in res.json()['categories']['classifier_scores'][0]


def test_working(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/submission/888", cookies=cookies)
    assert res.status_code == 200


def test_problem(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/submission/4024428", cookies=cookies)
    assert res.status_code == 200

