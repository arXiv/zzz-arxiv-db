import requests
import os
from modapi.auth import user_jwt

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

SUB_ID_1 = 1137914


def test_docs():
    response = requests.get(BASE_URL + "/docs")
    assert response.status_code == 200


def test_flags():
    # get initial state: empty flag list
    res = requests.get(BASE_URL + "/flags")
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data == []

    #put a flag
    res = requests.put(
        BASE_URL + f"/submission/{SUB_ID_1}/flag",
        json={"username": "bob", "flag": "checkmark"},
    )
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    # get that flag
    res = requests.get(BASE_URL + "/flags")
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data
    flag = data[0]

    assert flag["username"] == "bob"
    assert flag["submission_id"] == SUB_ID_1
    #TODO ADD FLAG
    #assert flag["flag"] == "checkmark"

    res = requests.put(  # try to put a duplicate flag, should fail 
        BASE_URL + f"/submission/{SUB_ID_1}/flag",
        json={"username": "bob", "flag": "checkmark"},
    )     
    assert res.status_code != 200  # should not be able to do duplicate flag
    assert res.status_code != 201  # should not be able to do duplicate flag

    res = requests.post(
        BASE_URL + f"/submission/{SUB_ID_1}/flag/delete", json={"username": "bob"}
    )
    assert res.status_code == 200     # delete the flag

    res = requests.get(BASE_URL + "/flags")
    assert res.status_code == 200
    assert res.json() == []     # flag should be gone


def test_flags_from_multiple_mods():
    #put a flag from modA
    res = requests.put(
        BASE_URL + f"/submission/{SUB_ID_1}/flag",
        json={"username": "modA", "flag": "checkmark"},
    )
    assert res.status_code == 200

    # put a flag from modB
    res = requests.put(
        BASE_URL + f"/submission/{SUB_ID_1}/flag",
        json={"username": "modB", "flag": "checkmark"},
    )
    assert res.status_code == 200
    
    res = requests.get(BASE_URL + "/flags")
    assert res.status_code == 200
    assert set([fg['username'] for fg in res.json()]) == set(['modA', 'modB'])  # Should have flags from both mods 
    
    res = requests.post(
        BASE_URL + f"/submission/{SUB_ID_1}/flag/delete", json={"username": "modA"}
    )
    assert res.status_code == 200     # delete the flag

    res = requests.post(
        BASE_URL + f"/submission/{SUB_ID_1}/flag/delete", json={"username": "modB"}
    )
    assert res.status_code == 200     # delete the flag

