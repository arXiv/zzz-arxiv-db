from modapi.auth import user_jwt

USER_ID = 246231  # Brandon, mod of q-bio.CB and q-bio.NC

def test_status(client):
    assert client.get('/status').status_code == 200

def test_version(client):
    assert client.get('/version').status_code == 200

def test_email_log(client):
    assert client.get('/email_log').status_code == 401    
    res = client.get("/email_log", cookies={'ARXIVNG_SESSION_ID': user_jwt(USER_ID)})
    res.status_code == 200
