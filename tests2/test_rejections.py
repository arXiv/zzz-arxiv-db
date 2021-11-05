from unittest import mock
from modapi.auth import user_jwt
from modapi.email import build_reject_cross_email

SUB_ID_1 = 4401
SUB_ID_2 = 4402
SUB_ID_3 = 1137932
SUB_ID_4 = 4403


def test_category_rejection_unauthorized(client):
    res = client.post(f"/submission/{SUB_ID_1}/category_rejection")
    assert res.status_code == 401

def test_reject_category_singleton(client):
    """Test rejection for a submission that only has a single category."""
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC

    # get submission
    res = client.get(f"/submission/{SUB_ID_3}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    data = res.json()
    assert data["status"] == "submitted"
    assert data["type"] == "new"
    assert data["categories"]["submission"]["primary"] == "q-bio.GN"
    assert data["categories"]["submission"]["secondary"] == []

    # accept_secondary action
    res = client.post(
        f"/submission/{SUB_ID_3}/category_rejection",
        json={"category": "q-bio.GN", "action": "accept_secondary"},
        cookies=cookies
    )
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data == "success"

    res = client.get(f"/submission/{SUB_ID_3}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    # expect the status to be changed to `on_hold`
    data = res.json()
    assert data["status"] == "on hold"
    assert data["type"] == "new"
    assert data["categories"]["submission"]["primary"] == None
    assert data["categories"]["submission"]["secondary"] == ["q-bio.GN"]

    # reject action
    res = client.post(
        f"/submission/{SUB_ID_3}/category_rejection",
        json={"category": "q-bio.GN", "action": "reject"},
        cookies=cookies
    )
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data == "success"

    res = client.get(f"/submission/{SUB_ID_3}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data["status"] == "on hold"
    assert data["categories"]["submission"]["primary"] == None
    assert data["categories"]["submission"]["secondary"] == []

def test_reject_category_multiple(client):
    """Test rejection for a submission that has multiple categories."""
    cookies = {
        "ARXIVNG_SESSION_ID": user_jwt(246231)
    }  # Brandon, mod of q-bio.CB and q-bio.NC

    # get submission
    res = client.get(f"/submission/{SUB_ID_4}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    data = res.json()
    assert data["status"] == "submitted"
    assert data["type"] == "new"
    assert data["categories"]["submission"]["primary"] == "cs.LG"
    assert set(data["categories"]["submission"]["secondary"]) == set(["cs.AI", "cs.DD", "hep-ph"])

    # accept_secondary action
    res = client.post(
        f"/submission/{SUB_ID_4}/category_rejection",
        json={"category": "cs.LG", "action": "accept_secondary"},
        cookies=cookies
    )
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data == "success"

    res = client.get(f"/submission/{SUB_ID_4}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    # expect the status to be changed to `on_hold`
    data = res.json()
    assert data["status"] == "on hold"
    assert data["type"] == "new"
    assert data["categories"]["submission"]["primary"] == None
    assert set(data["categories"]["submission"]["secondary"]) == set(["cs.AI", "cs.DD", "cs.LG", "hep-ph"])

    # reject action
    res = client.post(
        f"/submission/{SUB_ID_4}/category_rejection",
        json={"category": "hep-ph", "action": "reject"},
        cookies=cookies
    )
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data == "success"

    res = client.get(f"/submission/{SUB_ID_4}", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data["status"] == "on hold"
    assert data["categories"]["submission"]["primary"] == None
    assert set(data["categories"]["submission"]["secondary"]) == set(["cs.AI", "cs.DD", "cs.LG"])

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
        f"/submission/{SUB_ID_1}/category_rejection",
        json={"category": "cs.ML", "action": "reject"},
        cookies=cookies,
    )
    assert res.status_code == 409

    # try accept_secondary action for cross--should fail
    res = client.post(
        f"/submission/{SUB_ID_1}/category_rejection",
        json={"category": "cs.ML", "action": "accept_secondary"},
        cookies=cookies,
    )
    assert res.status_code == 403

    # try to reject the only cross category
    res = client.post(
        f"/submission/{SUB_ID_1}/category_rejection",
        json={"category": "hep-ph", "action": "reject"},
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
    assert data["categories"]["new_crosses"] == []

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
        f"/submission/{SUB_ID_2}/category_rejection",
        json={"category": "cs.AI", "action": "reject"},
        cookies=cookies,
    )
    res = client.get(f"/submission/{SUB_ID_2}", cookies=cookies)
    data = res.json()
    assert data["status"] == "submitted"
    assert data["type"] == "cross"
    assert data["categories"]["new_crosses"] == ["hep-ph"]

    # try to reject second of two cross categories
    res = client.post(
        f"/submission/{SUB_ID_2}/category_rejection",
        json={"category": "hep-ph", "action": "reject"},
        cookies=cookies,
    )
    res = client.get(f"/submission/{SUB_ID_2}", cookies=cookies)
    data = res.json()
    assert data["status"] == "removed"
    assert data["type"] == "cross"
    assert data["categories"]["new_crosses"] == []
