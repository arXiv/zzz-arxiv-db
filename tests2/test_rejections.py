from unittest import mock
from modapi.auth import user_jwt
from modapi.util.email import build_reject_cross_email

SUB_ID_1 = 4401
SUB_ID_2 = 4402


def test_reject_cross_unauthorized(client):
    res = client.post(f"/submission/{SUB_ID_1}/reject_cross")
    assert res.status_code == 401


def test_reject_cross(client):
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC

    # get submission
    res = client.get(f"/submission/{SUB_ID_1}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    data = res.json()
    assert data["status"] == "submitted"
    assert data["type"] == "cross"
    assert data["categories"]["new_crosses"] == ["hep-ph"]

    # try to reject some other category not associated with cross--should fail
    res = client.post(
        f"/submission/{SUB_ID_1}/reject_cross",
        json={"category": "cs.ML"},
        cookies=cookies,
    )
    assert res.status_code == 409

    # try to reject the only cross category
    res = client.post(
        f"/submission/{SUB_ID_1}/reject_cross",
        json={"category": "hep-ph"},
        cookies=cookies,
    )
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    res = client.get(f"/submission/{SUB_ID_1}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    data = res.json()
    # expect the status to be changed to `removed`
    assert data["status"] == "removed"
    assert data["type"] == "cross"
    # expect the last cross category to remain in arXiv_submission_category
    assert data["categories"]["new_crosses"] == ["hep-ph"]

    # get submission
    res = client.get(f"/submission/{SUB_ID_2}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    data = res.json()
    assert data["status"] == "submitted"
    assert data["type"] == "cross"
    assert data["categories"]["new_crosses"] == ["hep-ph", "cs.AI"]

    # try to reject first of two cross categories
    res = client.post(
        f"/submission/{SUB_ID_2}/reject_cross",
        json={"category": "cs.AI"},
        cookies=cookies,
    )
    res = client.get(f"/submission/{SUB_ID_2}", cookies=cookies)
    data = res.json()
    assert data["status"] == "submitted"
    assert data["type"] == "cross"
    assert data["categories"]["new_crosses"] == ["hep-ph"]

    # try to reject second of two cross categories
    res = client.post(
        f"/submission/{SUB_ID_2}/reject_cross",
        json={"category": "hep-ph"},
        cookies=cookies,
    )
    res = client.get(f"/submission/{SUB_ID_2}", cookies=cookies)
    data = res.json()
    assert data["status"] == "removed"
    assert data["type"] == "cross"
    assert data["categories"]["new_crosses"] == ["hep-ph"]
