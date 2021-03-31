import requests
import os
from modapi.auth import user_jwt

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

SUB_ID_1 = 1137914


def test_docs():
    response = requests.get(BASE_URL + "/docs")
    assert response.status_code == 200


def test_flags_unauthorized():
    res = requests.get(BASE_URL + "/flags")
    assert res.status_code == 401


def test_flags():
    # get initial state: empty flag list
    cookies = {'ARXIVNG_SESSION_ID': user_jwt(246231)} # Brandon, mod of q-bio.CB and q-bio.NC
    res = requests.get(BASE_URL + "/flags",
                           cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data == [] # Expecting an empty test DB

    
    #put a flag
    res = requests.put(
        BASE_URL + f"/submission/{SUB_ID_1}/flag",
        json={"flag": "checkmark"},
        cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    # get that flag
    res = requests.get(BASE_URL + "/flags",
                       cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data
    flag = data[0]

    assert flag["username"] == "bbarker"
    assert flag["submission_id"] == SUB_ID_1
    #TODO ADD FLAG
    #assert flag["flag"] == "checkmark"

    res = requests.put(  # try to put a duplicate flag, should fail 
        BASE_URL + f"/submission/{SUB_ID_1}/flag",
        json={"username": "bbarker", "flag": "checkmark"},
        cookies=cookies
    )     
    assert res.status_code != 200  # should not be able to do duplicate flag
    assert res.status_code != 201  # should not be able to do duplicate flag

    res = requests.post(
        BASE_URL + f"/submission/{SUB_ID_1}/flag/delete",
        cookies=cookies
    )
    assert res.status_code == 200     # delete the flag

    res = requests.get(BASE_URL + "/flags",
                       cookies=cookies)
    assert res.status_code == 200
    assert res.json() == []     # flag should be gone
