import requests
import os
from modapi.auth import user_jwt

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

SUB_ID_1 = 1137914
   
def test_auth():
    res = requests.get(BASE_URL + "/holds")
    assert res.status_code == 401  # Should be auth protected
    
def test_holds():
    cookies = {'ARXIVNG_SESSION_ID': user_jwt(246231)} # Brandon, mod of q-bio.CB and q-bio.NC
    res = requests.get(
        BASE_URL + "/holds",
        cookies = cookies
        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None    
    pre_add_count = len(res.json())

    # add hold
    res = requests.post( BASE_URL + f"/submission/{SUB_ID_1}/hold",
                         json={'type': 'mod', 'reason':'discussion'},
                        cookies = cookies
                        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200


    res = requests.get(
        BASE_URL + "/holds",
        cookies = cookies
        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count +1

    
    # try to add duplicate hold
    res = requests.post( BASE_URL + f"/submission/{SUB_ID_1}/hold",
                         json={'type': 'mod', 'reason':'discussion'},
                        cookies = cookies
                        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code >= 300 or res.status_code < 200 # should not be success, it's a duplicate
    
    res = requests.get(
        BASE_URL + "/holds",
        cookies = cookies
        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count + 1


    # release hold
    res = requests.post( BASE_URL + f"/submission/{SUB_ID_1}/hold/release" ,
                         cookies = cookies )
    body = res.content
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code >= 200 and res.status_code < 300

    res = requests.get(
        BASE_URL + "/holds",
        cookies = cookies
        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count




def test_multi_mod(): 
    cookies_mod_a = {'ARXIVNG_SESSION_ID': user_jwt(246231)} # Brandon, mod of q-bio.CB and q-bio.NC
    res = requests.get(
        BASE_URL + "/holds",
        cookies = cookies_mod_a
        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert res.json() is not None    
    pre_add_count = len(res.json())

    # add hold
    res = requests.post( BASE_URL + f"/submission/{SUB_ID_1}/hold",
                         json={'type': 'mod', 'reason':'discussion'},
                        cookies = cookies_mod_a
                        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200


    res = requests.get(
        BASE_URL + "/holds",
        cookies = cookies_mod_a
        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count +1  # Hold should have been added

    # Other moderator releases hold
    cookies_mod_b = {'ARXIVNG_SESSION_ID': user_jwt(246232)} 
    res = requests.post( BASE_URL + f"/submission/{SUB_ID_1}/hold/release" ,
                         cookies = cookies_mod_b )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code >= 200 and res.status_code < 300

    res = requests.get(
        BASE_URL + "/holds",
        cookies = cookies_mod_a
        )
    assert res.status_code != 401  # Tests must run with env var JWT_SECRET same as server
    assert res.status_code == 200
    assert len(res.json()) == pre_add_count
