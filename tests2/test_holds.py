from modapi.auth import user_jwt

SUB_ID_1 = 1137914


def test_auth(client):
    res = client.get("/holds")
    assert res.status_code == 401  # Should be auth protected


def test_make(client):
    # Brandon, mod of q-bio.CB and q-bio.NC
    cookies = {"ARXIVNG_SESSION_ID": user_jwt(246231)}
    res = client.get("/holds", cookies=cookies)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert res.json() is not None
    pre_add_count = len(res.json())

    # add hold
    res = client.post(
        f"/submission/{SUB_ID_1}/hold",
        json={"type": "mod", "reason": "discussion"},
        cookies=cookies,
    )
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200

    res = client.get("/holds", cookies=cookies)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count + 1
    holds = res.json()
    assert [str(SUB_ID_1), "246231", "mod", "discussion"] in holds

    # try to add duplicate hold
    res = client.post(f"/submission/{SUB_ID_1}/hold",
                      json={"type": "mod", "reason": "discussion"},
                      cookies=cookies)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    # should not be success, it's a duplicate
    assert res.status_code >= 300 or res.status_code < 200

    res = client.get("/holds", cookies=cookies)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count + 1

    # release hold
    res = client.post(f"/submission/{SUB_ID_1}/hold/release", cookies=cookies)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code >= 200 and res.status_code < 300

    res = client.get("/holds", cookies=cookies)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count


def test_multi_mod(client):
    # Brandon, mod of q-bio.CB and q-bio.NC
    cookies_mod_a = {"ARXIVNG_SESSION_ID": user_jwt(246231)}
    res = client.get("/holds", cookies=cookies_mod_a)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert res.json() is not None
    pre_add_count = len(res.json())

    # add hold
    res = client.post(
        f"/submission/{SUB_ID_1}/hold",
        json={"type": "mod", "reason": "discussion"},
        cookies=cookies_mod_a,
    )
    print(res.json())
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200

    res = client.get("/holds", cookies=cookies_mod_a)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count + 1  # Hold should have been added

    # Other moderator releases hold
    cookies_mod_b = {"ARXIVNG_SESSION_ID": user_jwt(246232)}
    res = client.post(f"/submission/{SUB_ID_1}/hold/release", cookies=cookies_mod_b)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code >= 200 and res.status_code < 300

    res = client.get("/holds", cookies=cookies_mod_a)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count


def test_locked(client):
    cookies_mod_a = {"ARXIVNG_SESSION_ID": user_jwt(246231)}  # Brandon

    # add hold
    sub_locked = 100430
    res = client.post(
        f"/submission/{sub_locked}/hold",
        json={"type": "mod", "reason": "discussion"},
        cookies=cookies_mod_a,
    )
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 403  # locked is forbidden

    res = client.post(f"/submission/{sub_locked}/hold/release", cookies=cookies_mod_a)
    print(res.json())
    # Tests must run with env var JWT_SECRET same as server
    assert res.status_code != 401
    assert res.status_code == 403  # locked is forbidden
