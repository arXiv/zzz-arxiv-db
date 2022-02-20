from modapi.auth import user_jwt

SUB_ID_1 = 1137914


def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_flags_unauthorized(client):
    res = client.get("/flags")
    assert res.status_code == 401


def test_flags(client):
    # get initial state: empty flag list
    cookies = {'ARXIVNG_SESSION_ID': user_jwt(246231)} # Brandon, mod of q-bio.CB and q-bio.NC
    res = client.get("/flags", cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"
    data = res.json()
    assert data == [] # Expecting an empty test DB

    
    #put a flag
    res = client.put(f"/submission/{SUB_ID_1}/flag",
                     json={"flag": "checkmark"},
                     cookies=cookies)
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/json"

    # get that flag
    res = client.get("/flags",
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

    res = client.put(  # try to put a duplicate flag, should fail
        f"/submission/{SUB_ID_1}/flag",
        json={"username": "bbarker", "flag": "checkmark"},
        cookies=cookies
    )     
    assert res.status_code != 200  # should not be able to do duplicate flag
    assert res.status_code != 201  # should not be able to do duplicate flag

    res = client.post(
        f"/submission/{SUB_ID_1}/flag/delete",
        cookies=cookies
    )
    assert res.status_code == 200     # delete the flag

    res = client.get("/flags",
                     cookies=cookies)
    assert res.status_code == 200
    assert res.json() == []     # flag should be gone
