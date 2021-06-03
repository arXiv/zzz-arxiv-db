import requests
import os
from modapi.auth import user_jwt

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

def test_hep_subs_via_proposal():
    cookies = {"ARXIVNG_SESSION_ID": user_jwt(246233)} # mod of hep-ph
    res = requests.get(BASE_URL + "/submissions", cookies=cookies)
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None
    subs = res.json()
    assert type(subs) == list
    assert 1137934 in [sub['submission_id'] for sub in subs]
