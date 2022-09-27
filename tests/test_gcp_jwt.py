import pytest

import logging
import os

import google.oauth2.id_token
from google.auth.transport import requests

from modapi import auth
from modapi.config import config
from modapi.tables.arxiv_tables import tapir_users, tapir_nicknames

auth.log.setLevel(logging.DEBUG)

USER_ID = 246231  # Brandon, mod of q-bio.CB and q-bio.NC
EMAIL_NO_PRIV = 'no-mail-randomreader@example.com' # Random Reader. Not mod, not admin

EMAIL_SA = 'qa-tools-sa@arxiv-proj.iam.gserviceaccount.com' # admin service account email

def test_unknown_user(mocker, client):
    mock_gcp = mocker.patch('modapi.gcp_token_check.verify_token')
    mock_gcp.return_value = {'whence':'from-gcp-but-really-mocked-in' + __file__,
                             'azp': 'some-email-not-in-arxiv-users@gmail.com'}    
    res = client.get("/me", headers={'Authorization': 'Bearer AnythingSinceMocked'})
    assert res.status_code == 401


def test_unprivileged_user(mocker, client):
    mock_gcp = mocker.patch('modapi.gcp_token_check.verify_token')
    mock_gcp.return_value = {'whence':'from-gcp-but-really-mocked-in' + __file__,
                             'azp': EMAIL_NO_PRIV}
    res = client.get("/me", headers={'Authorization': 'Bearer AnythingSinceMocked'})
    assert res.status_code == 401


def test_admin_user(mocker, client):
    mocker.patch('modapi.auth.verify_token',
                 return_value = {'whence':'from-gcp-but-really-mocked-in' + __file__,
                                 'azp': EMAIL_SA})    
    res = client.get("/me", headers={'Authorization': 'Bearer AnythingSinceMocked'})
    assert res.status_code == 200


def test_noemail(mocker, client):
    mocker.patch('modapi.auth.verify_token',
                 return_value = {'whence':'from-gcp-but-really-mocked-in' + __file__,
                                 'azp': 'totalyfakeemail@example.com'})    
    res = client.get("/me", headers={'Authorization': 'Bearer AnythingSinceMocked'})
    assert res.status_code == 401


def test_on_gcp(get_test_db, client):
    """Integration test with GCP that makes a user with an eamil of a service account.

    To run this do:

       GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/arxiv-test-xyz.json pytest tests2/test_gcp_jwt.py
    """
    id = None
    jwt = None

    db = next(get_test_db())
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        auth_req = google.auth.transport.requests.Request()
        jwt = google.oauth2.id_token.fetch_id_token(auth_req, config.audience)
        assert jwt
        id = google.oauth2.id_token.verify_oauth2_token(jwt, requests.Request(), config.audience)
        assert id
        email = id['azp']
        assert email
        db.execute(tapir_users.insert().values(
            user_id=999999,
            email=email,
            first_name='test',
            last_name='account',
            joined_ip_num='1234',
            flag_edit_users=1,
            flag_email_verified=1,
        ))
        db.execute(tapir_nicknames.insert().values(
            nick_id=2122399,
            nickname='test_sa_account',
            user_id=999999,
        ))
        db.commit()

    if not id or not jwt:
        pytest.skip("Not testing GCP since GOOGLE_APPLICATION_CREDENTIALS is not set")

    res = client.get("/me", headers={"Authorization": f"Bearer {jwt}"})
    assert res.status_code == 200
