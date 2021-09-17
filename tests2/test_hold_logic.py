from datetime import datetime

from modapi.rest.holds.biz_logic import hold_biz_logic, status_by_number, release_biz_logic
from modapi.rest.holds.domain import ModHoldIn, Reject, HoldReleaseLogicRes, ON_HOLD, SUBMITTED

from modapi.auth import User
from fastapi.responses import JSONResponse


mod_user = User(user_id=1111111, name='M The Mod', username='mtm', is_moderator=True,
                is_admin=False, moderated_categories=['cs.LG'])

admin_user = User(user_id=99999, name='A The Admin',
                  username='ata', is_admin=True)

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
    exists.status=SUBMITTED
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


def test_release_mod_hold(mocker):
    hr = mocker.patch('modapi.tables.arxiv_models.SubmissionHoldReason')
    hr.reason="discussion"
    hr.user_id=1234
    hr.type="mod"

    exists = mocker.patch('modapi.tables.arxiv_models.Submissions')
    exists.status=ON_HOLD
    exists.hold_reasons=[hr]
    exists.hold_reason=hr
    exists.submit_time=datetime.fromisoformat("2010-05-13T00:00:00+00:00")
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    result = release_biz_logic(exists, 1234, mod_user, lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result
    print(result)
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
    exists.submit_time='bogus-time'
    exists.sticky_status=False
    exists.is_locked=False
    exists.doc_paper_id=None
    exists.primary_classification = 'cs.OH'

    result = release_biz_logic(exists, 1234, admin_user, lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result
    assert isinstance(result, HoldReleaseLogicRes)
    assert result.paper_id == 'submit/1234'


def test_admin_cannot_hold_release_no_primary(mocker):
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


def test_mod_cannot_hold_release_no_primary(mocker):
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
