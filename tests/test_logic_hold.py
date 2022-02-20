import pytest

from datetime import datetime

from pydantic.error_wrappers import ValidationError

from modapi.rest.holds.biz_logic import hold_biz_logic, status_by_number, release_by_mod_biz_logic, _release_status_from_submit_time
from modapi.rest.holds.domain import WORKING, HoldLogicRes, ModHoldIn, Reject, HoldReleaseLogicRes, ON_HOLD, SUBMITTED

from modapi.auth import User
from fastapi.responses import JSONResponse


mod_user = User(user_id=1111111, name='M The Mod', username='mtm', is_moderator=True,
                is_admin=False, moderated_categories=['cs.LG'], email='a@example.com')

admin_user = User(user_id=99999, name='A The Admin',
                  username='ata', is_admin=True, email='b@example.com')

sub_id = 3434343


def test_mod_new_hold(mocker):
    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=SUBMITTED
    exists.hold_reasons = []
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.hold_reason =None
    exists.primary_classification = 'cs.OH'

    result = hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert result
    assert 'Mod Hold' in '|||'.join(result.visible_comments)
    assert 'discussion' in '|||'.join(result.visible_comments)
    assert result.modapi_comments
    assert not result.delete_hold_reason
    assert result.create_hold_reason
    assert result.paper_id == f'submit/{sub_id}'


def test_mod_duplicate_hold(mocker):
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id="2343"
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons = [hr]
    exists.hold_reason =hr
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'


    result = hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 409


def test_mod_nosub_hold(mocker):
    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists = None
    result = hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404


def test_mod_islocked(mocker):
    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=SUBMITTED
    exists.hold_reasons = []
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=True
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    result = hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403


def test_mod_bad_sub_status(mocker):    
    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    for status in status_by_number.keys():
        if status in (1,2,4):
            continue

        exists.status=status
        exists.hold_reasons = []
        exists.submit_time='bogus-time'
        exists.sticky_status=False
        exists.is_locked=False
        exists.doc_paper_id=None
        exists.primary_classification = 'cs.OH'

        result = hold_biz_logic(
            ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
        assert result
        assert result.status_code == 409


def test_mod_to_admin_hold(mocker):
    """Mod can turn an mod hold to an admin hold"""
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id=1234
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons = [hr]
    exists.hold_reason =hr
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    result = hold_biz_logic(
        Reject(type='admin', reason='nonresearch'), exists, sub_id, mod_user)
    assert result
    assert 'Admin Hold' in '|||'.join(result.visible_comments)
    assert 'nonresearch' in '|||'.join(result.visible_comments)
    assert result.modapi_comments
    assert result.delete_hold_reason
    assert result.create_hold_reason


def test_hold_new_admin_hold(mocker):
    """Mod can put a hold on a unheld sub"""
    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=SUBMITTED
    exists.hold_reasons=[]
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.hold_reason =None
    exists.primary_classification = 'cs.OH'

    hold = Reject(type='admin', reason='nonresearch')
    result = hold_biz_logic(hold, exists, 1234, admin_user)
    assert result
    assert "Admin Hold" in '|||'.join(result.visible_comments)


def test_hold_existing_admin_hold(mocker):
    """Mod cannot put another hold on sub that is already admin held"""
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="nonresearch"
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

    hold = Reject(type='admin', reason='nonresearch')
    result = hold_biz_logic(hold, exists, 1234, admin_user)
    assert result
    assert result.status_code == 409


def test_hold_existing_legacy_hold(mocker):
    """Mod can put a legacy held submission on Admin hold"""
    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons=[]
    exists.hold_reason =None
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    hold = Reject(type='admin', reason='nonresearch')
    result = hold_biz_logic(hold, exists, 1234, admin_user)
    assert result.create_hold_reason
    assert "Admin Hold" in '\n'.join(result.visible_comments)


def test_invalid_hold_type(mocker):
    with pytest.raises(ValidationError):
        Reject(type='Imabadholdtype', reason='nonresearch')

def test_mod_hold_lingering_reason(mocker):
    """mod can put a sub on mod hold when there is a hold reason but the
    submission is not on hold. The hold reason is "lingering"
    """
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id=1234
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=SUBMITTED
    exists.hold_reasons=[hr]
    exists.hold_reason =hr
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    hold = ModHoldIn(type='mod', reason='discussion')
    result = hold_biz_logic(hold, exists, 1234, mod_user)
    assert isinstance(result, HoldLogicRes)
    assert result.create_hold_reason
    assert result.delete_hold_reason
    assert result.visible_comments
    assert result.modapi_comments
    
    
def test_admin_hold_lingering_reason(mocker):
    """mod can put a sub on mod hold when there is a hold reason but the
    submission is not on hold. The hold reason is "lingering"
    """
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id=1234
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=SUBMITTED
    exists.hold_reasons=[hr]
    exists.hold_reason =hr
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    hold = Reject(type='admin', reason='softreject')
    result = hold_biz_logic(hold, exists, 1234, admin_user)
    assert isinstance(result, HoldLogicRes)
    assert result.create_hold_reason
    assert result.delete_hold_reason
    assert result.visible_comments
    assert result.modapi_comments
    
