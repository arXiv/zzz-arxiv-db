import pytest
from pytest_mock import mocker

from dataclasses import dataclass

import datetime

from modapi.rest.publish_time import _get_times, Times
from fastapi.testclient import TestClient

from modapi.app import app


@dataclass
class WithJson:
    data: dict

    def json(self):
        return self.data


def test_get_times():
    times = _get_times(WithJson(
        data={
            "arxiv_tz": "EDT",
            "next_freeze": "2021-05-12T18:00:00+00:00",
            "next_mail": "2021-05-13T00:00:00+00:00",
            "subsequent_mail": "2021-05-14T00:00:00+00:00"
        }))
    assert times

    assert isinstance(times, Times)
    
    assert times.next_mail.year == 2021
    assert times.next_mail.month == 5
    assert times.next_mail.day == 13
    assert times.next_mail.hour == 0
    assert times.next_mail.minute == 0
    assert times.next_mail.second == 0
    assert times.next_mail.tzinfo == datetime.timezone.utc


@pytest.fixture
def the_app():
    return TestClient(app)


def test_times_page(mocker, the_app):
    mocked_auth = mocker.patch('modapi.auth.mod_header_user')
    mocked_auth.return_value = {'something': 'mocked'}
    mocked_auth = mocker.patch('modapi.auth.auth_user')
    mocked_auth.return_value = {'something': 'mocked'}
    
    mocked_fn = mocker.patch('modapi.rest.publish_time._get_timepage')
    mocked_fn.return_value = WithJson(
        data={
            "arxiv_tz": "EDT",
            "next_freeze": "2021-05-12T18:00:00+00:00",
            "next_mail": "2021-05-13T00:00:00+00:00",
            "subsequent_mail": "2021-05-14T00:00:00+00:00"
        })

    resp = the_app.get('/times')
    assert resp
    data = resp.json()
    assert data
    assert data['next_mail'] == "2021-05-13T00:00:00+00:00"

