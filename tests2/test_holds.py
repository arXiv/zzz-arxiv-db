import pytest
from modapi.auth import user_jwt

SUB_ID_1 = 1137914


@pytest.fixture
def brandon():      # Brandon, mod of q-bio.CB and q-bio.NC
    return  {"ARXIVNG_SESSION_ID": user_jwt(246231)}


@pytest.fixture
def mod_b():   # Other moderator releases hold
    return {"ARXIVNG_SESSION_ID": user_jwt(246232)}


def test_no_auth(client):
    res = client.get("/holds")
    assert res.status_code == 401  # Should be auth protected


def test_make(client, brandon):
    res = client.get("/holds", cookies=brandon)
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None
    pre_add_count = len(res.json())

    # add hold
    res = client.post(
        f"/submission/{SUB_ID_1}/hold",
        json={"type": "mod", "reason": "discussion"},
        cookies=brandon,
    )
    
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200

    res = client.get("/holds", cookies=brandon)
    
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count + 1
    holds = res.json()
    assert [str(SUB_ID_1), "246231", "mod", "discussion"] in holds

    # try to add duplicate hold
    res = client.post(f"/submission/{SUB_ID_1}/hold",
                      json={"type": "mod", "reason": "discussion"},
                      cookies=brandon)
    
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    # should not be success, it's a duplicate
    assert res.status_code >= 300 or res.status_code < 200

    res = client.get("/holds", cookies=brandon)
    
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count + 1

    # release hold
    res = client.post(f"/submission/{SUB_ID_1}/hold/release", cookies=brandon)
    
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code >= 200 and res.status_code < 300

    res = client.get("/holds", cookies=brandon)
    
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count


def test_multi_mod(client, brandon, mod_b):
    # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/holds", cookies=brandon)
    
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert res.json() is not None
    pre_add_count = len(res.json())

    # add hold
    res = client.post(
        f"/submission/{SUB_ID_1}/hold",
        json={"type": "mod", "reason": "discussion"},
        cookies=brandon,
    )
    assert res.status_code != 401
    assert res.status_code == 200

    res = client.get("/holds", cookies=brandon)
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count + 1  # Hold should have been added

    # Other moderator releases hold
    res = client.post(f"/submission/{SUB_ID_1}/hold/release", cookies=mod_b)    
    assert res.status_code != 401
    assert res.status_code >= 200 and res.status_code < 300

    res = client.get("/holds", cookies=brandon)
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count


def test_locked(client, brandon):
    sub_locked = 100430
    res = client.post(f"/submission/{sub_locked}/hold", cookies=brandon,
                      json={"type": "mod", "reason": "discussion"})
    assert res.status_code == 403  # locked is forbidden
    res = client.post(f"/submission/{sub_locked}/hold/release", cookies=brandon)
    assert res.status_code == 403  # locked is forbidden

def test_no_sub(client, brandon):
    res=client.post("/submission/99999999/hold", cookies=brandon,
                    json={"type": "mod", "reason": "discussion"})
    assert res.status_code == 404

    res=client.post("/submission/99999999/hold/release", cookies=brandon)
    assert res.status_code == 404

    
def test_earliest_ann_down(mocker, client, brandon):
    mocked_earliest_anno = mocker.patch('modapi.rest.holds.earliest_announce')
    mocked_earliest_anno.return_value = 404
    
    cookies_mod_a = {"ARXIVNG_SESSION_ID": user_jwt(246231)}  # Brandon
    sub_locked = 100430
    res = client.post(f"/submission/{sub_locked}/hold/release",
                      json={"type": "mod", "reason": "discussion"},
                      cookies=brandon)
    assert res.status_code == 502


def test_comments():
    from modapi.rest.holds import _hold_comments
    from modapi.rest.holds import ModHoldIn, Reject, RejectOther, SendToAdminOther
    
    assert _hold_comments(ModHoldIn(type='mod',reason='discussion'))
    assert _hold_comments(Reject(type='admin',reason= 'scope'))
    assert _hold_comments(RejectOther(type='admin',reason='reject-other',comment='this paper lacks math'))
    assert _hold_comments(SendToAdminOther(type='admin',reason='other',comment='This is some kind of comment',sendback=False))
    assert _hold_comments(SendToAdminOther(type='admin',reason='other',comment='This is some kind of comment',sendback=True))
