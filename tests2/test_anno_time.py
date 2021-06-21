import pytest
from argparse import Namespace

from fastapi import HTTPException
from modapi.rest.earliest_announce import earliest_announce
import requests

def test_earliest_anno_down(mocker):
    mocked_get_url = mocker.patch('modapi.rest.earliest_announce._get')
    mocked_get_url.return_value = Namespace(status_code=500)
    with pytest.raises(HTTPException) as ex:
        earliest_announce(1234)
    assert ex.value.status_code == 502

def test_earliest_anno_404(mocker):
    mocked_get_url = mocker.patch('modapi.rest.earliest_announce._get')
    mocked_get_url.return_value = Namespace(status_code=404)
    with pytest.raises(HTTPException) as ex:
        earliest_announce(1234)
    assert ex.value.status_code == 404

def test_earliest_anno_timeout(mocker):
    def rr(x):
        raise requests.Timeout()
    mocked_get_url = mocker.patch('modapi.rest.earliest_announce._get',
                                  side_effect=rr)
    with pytest.raises(HTTPException) as ex:
        earliest_announce(1234)
    assert ex.value.status_code == 504

def test_earliest_anno_connerror(mocker):
    def rr(x):
        raise requests.ConnectionError()
    mocked_get_url = mocker.patch('modapi.rest.earliest_announce._get',
                                  side_effect=rr)
    with pytest.raises(HTTPException) as ex:
        earliest_announce(1234)
    assert ex.value.status_code == 502

