from modapi.rest.holds.domain import SendToAdminOther
import pytest
from datetime import datetime

from modapi.auth import user_jwt
from .test_publish_time import WithJson

SUB_ID_1 = 1137914

LEGACY_AUTO_HOLD_ID ='441708'

@pytest.fixture
def brandon():      # Brandon, mod of q-bio.CB and q-bio.NC
    return  {"ARXIVNG_SESSION_ID": user_jwt(246231)}


@pytest.fixture
def mod_b():   # Other moderator releases hold
    return {"ARXIVNG_SESSION_ID": user_jwt(246232)}

@pytest.fixture
def franky():   # Franky, mod of hep-ph
    return {"ARXIVNG_SESSION_ID": user_jwt(246232)}

@pytest.fixture()
def saratheadmin():
    return {"ARXIVNG_SESSION_ID": user_jwt(21)}

def test_no_auth(client):
    res = client.get("/holds")
    assert res.status_code == 401  # Should be auth protected


def test_make(mocker, client, brandon, saratheadmin):
    mocked_fn = mocker.patch('modapi.rest.publish_time._get_timepage')
    mocked_fn.return_value = WithJson(
        data={
            "arxiv_tz": "EDT",
            "next_freeze": "2021-05-12T18:00:00+00:00",
            "next_mail": "2021-05-13T00:00:00+00:00",
            "subsequent_mail": "2021-05-14T00:00:00+00:00"
        })

    mocked_anno_time = mocker.patch('modapi.rest.holds.routes.earliest_announce')
    mocked_anno_time.return_value = datetime.fromisoformat("2010-05-14T00:00:00+00:00")
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
    print(res)
    assert res.status_code == 200

    res = client.get("/holds", cookies=brandon)

    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count + 1
    holds = res.json()
    assert [str(SUB_ID_1), str(246231), "mod", "discussion"] in holds

    res = client.get(f"/submission/{SUB_ID_1}", cookies=brandon)
    assert res.status_code == 200
    assert res.json()['hold_type'] == "mod"
    assert res.json()['hold_reason'] == "discussion"

    res = client.get(f"/holds/{SUB_ID_1}", cookies=brandon)
    assert res.status_code == 200
    assert [str(SUB_ID_1), str(246231), 'mod', 'discussion'] in res.json()

    res = client.get("/holds", cookies=brandon)
    assert res.status_code == 200
    print( res.json())
    assert  [str(SUB_ID_1), str(246231), 'mod', 'discussion'] in res.json()

    # Can saratheadmin see this hold?
    res = client.get(f"/submission/{SUB_ID_1}", cookies=saratheadmin)
    assert res.status_code == 200
    assert res.json()['hold_type'] == "mod"
    assert res.json()['hold_reason'] == "discussion"

    res = client.get("/holds", cookies=saratheadmin)
    assert res.status_code == 200
    assert [str(SUB_ID_1), str(246231), 'mod', 'discussion'] in res.json()

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


def test_can_see_legacy_holds(client, brandon, saratheadmin):
    # Can saratheadmin see this hold?
    res = client.get(f"/submission/{LEGACY_AUTO_HOLD_ID}", cookies=saratheadmin)
    assert res.json()['status'] == 'on hold'

    res = client.get("/holds", cookies=saratheadmin)
    assert [True for hold in res.json() if LEGACY_AUTO_HOLD_ID in hold]

    res = client.get(f"/holds/{LEGACY_AUTO_HOLD_ID}", cookies=saratheadmin)
    assert [True for hold in res.json() if LEGACY_AUTO_HOLD_ID in hold]

    # Can a mod user see legacy holds?
    res = client.get("/holds", cookies=brandon)
    assert [True for hold in res.json() if LEGACY_AUTO_HOLD_ID in hold]

    res = client.get(f"/submission/{LEGACY_AUTO_HOLD_ID}", cookies=brandon)
    assert res.json()['status'] == 'on hold'

    res = client.get(f"/holds/{LEGACY_AUTO_HOLD_ID}", cookies=brandon)
    assert [True for hold in res.json() if LEGACY_AUTO_HOLD_ID in hold]

    res = client.get(f"/holds/{LEGACY_AUTO_HOLD_ID}", cookies=brandon)
    assert [True for hold in res.json() if LEGACY_AUTO_HOLD_ID in hold]


def test_admin_hold(mocker, client, brandon, saratheadmin, franky):
    mocked_fn = mocker.patch('modapi.rest.publish_time._get_timepage')
    mocked_fn.return_value = WithJson(
        data={
            "arxiv_tz": "EDT",
            "next_freeze": "2021-05-12T18:00:00+00:00",
            "next_mail": "2021-05-13T00:00:00+00:00",
            "subsequent_mail": "2021-05-14T00:00:00+00:00"
        })

    mocked_anno_time = mocker.patch('modapi.rest.holds.routes.earliest_announce')
    mocked_anno_time.return_value = datetime.fromisoformat("2010-05-14T00:00:00+00:00")

    res = client.get(f"/submission/{SUB_ID_1}", cookies=brandon)
    assert res.json()['status'] != 'on hold'
    # add admin hold
    res = client.post(
        f"/submission/{SUB_ID_1}/hold",
        json={"type": "admin", "reason": "other", "comment":f"test hold {__file__}", "sendback": False},
        cookies=brandon,
    )
    assert res.status_code == 200

    res = client.get(f"/submission/{SUB_ID_1}", cookies=brandon)
    assert res.json()['status'] == 'on hold'
    assert res.json()['hold_type'] == "admin"
    assert res.json()['hold_reason'] == "other"

    # Can saratheadmin see this hold?
    res = client.get(f"/submission/{SUB_ID_1}", cookies=saratheadmin)
    assert res.json()['status'] == 'on hold'
    res = client.get("/holds", cookies=saratheadmin)
    assert [True for hold in res.json() if str(SUB_ID_1) in hold]
    res = client.get(f"/holds/{SUB_ID_1}", cookies=saratheadmin)
    assert [True for hold in res.json() if str(SUB_ID_1) in hold]

    # Can brandon the mod in this sub's category see legacy holds?
    res = client.get("/holds", cookies=brandon)
    assert [True for hold in res.json() if str(SUB_ID_1) in hold]
    res = client.get(f"/submission/{SUB_ID_1}", cookies=brandon)
    assert res.json()['status'] == 'on hold'
    res = client.get(f"/holds/{SUB_ID_1}", cookies=brandon)
    assert [True for hold in res.json() if str(SUB_ID_1) in hold]
    res = client.get(f"/holds/{SUB_ID_1}", cookies=brandon)
    assert [True for hold in res.json() if str(SUB_ID_1) in hold]

    # Can franky a mod NOT in this sub's category see legacy holds?
    # res = client.get("/holds", cookies=franky)
    # assert [True for hold in res.json() if str(SUB_ID_1) in hold]
    res = client.get(f"/submission/{SUB_ID_1}", cookies=franky)
    assert res.json()['status'] == 'on hold'
    res = client.get(f"/holds/{SUB_ID_1}", cookies=franky)
    assert [True for hold in res.json() if str(SUB_ID_1) in hold]
    res = client.get(f"/holds/{SUB_ID_1}", cookies=franky)
    assert [True for hold in res.json() if str(SUB_ID_1) in hold]

    res = client.post(f"/submission/{SUB_ID_1}/hold/release", cookies=saratheadmin)


def test_multi_mod(mocker, client, brandon, mod_b):
    mocked_anno_time = mocker.patch('modapi.rest.holds.routes.earliest_announce')
    mocked_anno_time.return_value = datetime.fromisoformat("2010-05-14T00:00:00+00:00")

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
    print(res)
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

def test_comments():
    from modapi.rest.holds.biz_logic import _hold_comments
    from modapi.rest.holds.domain import ModHoldIn, Reject, RejectOther, SendToAdminOther

    assert _hold_comments(ModHoldIn(type='mod',reason='discussion'))
    assert _hold_comments(Reject(type='admin',reason= 'scope'))
    assert _hold_comments(RejectOther(type='admin',reason='reject-other',comment='this paper lacks math'))
    assert _hold_comments(SendToAdminOther(type='admin',reason='other',comment='This is some kind of comment',sendback=False))
    assert _hold_comments(SendToAdminOther(type='admin',reason='other',comment='This is some kind of comment',sendback=True))

def test_published(client, brandon):
    payload =  {'type':'admin',
                        'reason':'other',
                        'comment':'Only some of the highlighting has been fixed.',
                        'sendback':True}
    res=client.post("/submission/4024428/hold", cookies=brandon,
                json= payload)
    assert res.status_code > 299
