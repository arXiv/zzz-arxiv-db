import pytest

from datetime import datetime

from pydantic.error_wrappers import ValidationError

from modapi.rest.holds.biz_logic import hold_biz_logic, status_by_number, release_biz_logic, _release_status_from_submit_time
from modapi.rest.holds.domain import WORKING, ModHoldIn, Reject, HoldReleaseLogicRes, ON_HOLD, SUBMITTED

from modapi.auth import User
from fastapi.responses import JSONResponse


mod_user = User(user_id=1111111, name='M The Mod', username='mtm', is_moderator=True,
                is_admin=False, moderated_categories=['cs.LG'], email='a@example.com')

admin_user = User(user_id=99999, name='A The Admin',
                  username='ata', is_admin=True, email='ab@example.com')

sub_id = 3434343

    
def test_release_status_from_submit_time():
    assert WORKING == _release_status_from_submit_time(None)
    
    # submit on Monday, release time on Monday
    status = _release_status_from_submit_time(datetime(2021,9,13,13,59,59), datetime(2021,9,13,19,0,0))
    assert status == 1
    status = _release_status_from_submit_time(datetime(2021,9,13,14,0,0), datetime(2021,9,13,19,0,0))
    assert status == 4
    status = _release_status_from_submit_time(datetime(2021,9,13,14,0,1), datetime(2021,9,13,19,0,0))
    assert status == 4
    status = _release_status_from_submit_time(datetime(2021,9,13,14,0,1), datetime(2021,9,13,20,0,0))
    assert status == 4
    status = _release_status_from_submit_time(datetime(2021,9,13,14,0,1), datetime(2021,9,13,20,0,1))
    assert status == 1

    # submit on Wednesday, release time on Thursday
    status = _release_status_from_submit_time(datetime(2021,9,15,13,59,59), datetime(2021,9,16,19,0,0))
    assert status == 1
    status = _release_status_from_submit_time(datetime(2021,9,15,14,0,0), datetime(2021,9,16,20,0,0))
    assert status == 1

    # submit and release time on Friday
    status = _release_status_from_submit_time(datetime(2021,9,17,13,59,59), datetime(2021,9,17,20,0,0))
    assert status == 1
    status = _release_status_from_submit_time(datetime(2021,9,17,14,0,0), datetime(2021,9,17,20,0,0))
    assert status == 4
    status = _release_status_from_submit_time(datetime(2021,9,17,14,0,0), datetime(2021,9,17,20,0,1))
    assert status == 4

    # Sunday / Sunday
    status = _release_status_from_submit_time(datetime(2021,9,19,13,59,59), datetime(2021,9,19,19,0,0))
    assert status == 4
    status = _release_status_from_submit_time(datetime(2021,9,19,13,59,59), datetime(2021,9,19,20,0,1))
    assert status == 1

    # Monday
    status = _release_status_from_submit_time(datetime(2021,9,20,9,0,0), datetime(2021,9,20,9,0,5))
    assert status == 1
    status = _release_status_from_submit_time(datetime(2021,9,20,9,0,0), datetime(2021,9,20,14,0,5))
    assert status == 1
    status = _release_status_from_submit_time(datetime(2021,9,20,9,0,0), datetime(2021,9,20,20,0,5))
    assert status == 1
    status = _release_status_from_submit_time(datetime(2021,9,20,14,1,0), datetime(2021,9,20,14,0,5))
    assert status == 4
    status = _release_status_from_submit_time(datetime(2021,9,20,14,1,0), datetime(2021,9,20,20,0,5))
    assert status == 1

    # submit time later than release time (artificial; should never happen)
    status = _release_status_from_submit_time(datetime(2021,9,21,9,0,0), datetime(2021,9,20,9,0,5))
    assert status == 4


def test_cannot_release_no_sub():
    result = release_biz_logic(None, 1234, mod_user, lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result.status_code == 404

def test_cannot_release_locked(mocker):
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id=1234
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons=[hr]
    exists.hold_reason=hr
    exists.submit_time=datetime(2010, 5, 13, 0, 0, 0)
    exists.sticky_status=False
    exists.is_locked=True
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    result = release_biz_logic(exists, 1234, mod_user, None)
    assert result.status_code == 403

    result = release_biz_logic(exists, 1234, admin_user, None)
    assert result.status_code == 403
    
    
def test_release_mod_hold(mocker):
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id=1234
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons=[hr]
    exists.hold_reason=hr
    exists.submit_time=datetime(2010, 5, 13, 0, 0, 0)
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    result = release_biz_logic(exists, 1234, mod_user, lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result
    assert isinstance(result, HoldReleaseLogicRes)
    assert result.release_to_status == 1


def test_release_bad_user(mocker):
    bad_user = mocker.patch('modapi.tables.arxiv_models.TapirUsers')
    bad_user.user_id=1111111
    bad_user.name='JustANonModUser'
    bad_user.username='mjanmu'
    bad_user.is_moderator=False
    bad_user.is_admin=False
    bad_user.moderated_categories=[]

    res = release_biz_logic(None, 1234, bad_user, None)
    assert res
    assert res.status_code == 403

    res = release_biz_logic(None, 1234, None, None)
    assert res
    assert res.status_code == 403

    res = hold_biz_logic(None, None, 1234, bad_user)
    assert res
    assert res.status_code == 403

    res = hold_biz_logic(None, None, 1234, None)
    assert res
    assert res.status_code == 403


def test_mod_cannot_release_admin_hold(mocker):
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason=None
    hr.user_id=1234
    hr.type="admin"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons=[hr]
    exists.hold_reason =hr
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    result = release_biz_logic(exists, 1234, mod_user, None)
    assert result
    assert result.status_code == 403


def test_release_legacy_hold(mocker):
    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons=[]
    exists.hold_reason=[]
    exists.submit_time=datetime.now()
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    result = release_biz_logic(exists, 1234, admin_user, lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result
    assert isinstance(result, HoldReleaseLogicRes)
    assert result.paper_id == 'submit/1234'
    assert "Release: legacy hold" in result.visible_comments

def test_admin_cannot_release_no_primary(mocker):
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id=1234
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons=[hr]
    exists.hold_reason =hr
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification=None

    result = release_biz_logic(exists, 1234, admin_user,
                               lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result
    assert result.status_code > 400

    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="nonresearch"
    hr.user_id=1234
    hr.type="admin"

    exists.hold_reasons=[hr]
    exists.hold_reason =hr

    result = release_biz_logic(exists, 1234, admin_user,
                               lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result
    assert result.status_code > 400


def test_mod_cannot_release_no_primary(mocker):
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id=1234
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons=[hr]
    exists.hold_reason =hr
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification=None

    result = release_biz_logic(exists, 1234, mod_user,
                               lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result
    assert result.status_code > 400


def test_cannot_release_not_held(mocker):
    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=WORKING
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification=None
    result = release_biz_logic(exists, 1234, admin_user,
                               lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result.status_code > 400

    
