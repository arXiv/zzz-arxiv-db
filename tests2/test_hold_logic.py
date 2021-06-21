from datetime import datetime

from modapi.rest.holds.biz_logic import hold_biz_logic, status_by_number, release_biz_logic
from modapi.rest.holds.domain import ModHoldIn, Reject, HoldReleaseLogicRes, WORKING, ON_HOLD, SUBMITTED

from modapi.auth import User
from fastapi.responses import JSONResponse


mod_user = User(user_id=1111111, name='M The Mod', username='mtm', is_moderator=True,
                is_admin=False, moderated_categories=['cs.LG'])

admin_user = User(user_id=99999, name='A The Admin',
                  username='ata', is_admin=True)

sub_id = 3434343


def test_mod_new_hold():
    exists = dict(status=SUBMITTED, reason=None, hold_user_id=None,
                  hold_type=None, submit_time='bogus-time',
                  sticky_status=False, is_locked=False, paper_id=None)
    result = hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert result
    assert 'Mod Hold' in '|||'.join(result.visible_comments)
    assert 'discussion' in '|||'.join(result.visible_comments)
    assert result.modapi_comments
    assert not result.delete_hold_reason
    assert result.create_hold_reason
    assert result.paper_id == f'submit/{sub_id}'


def test_mod_duplicate_hold():
    exists = dict(status=SUBMITTED, reason="discussion", hold_user_id="2343",
                  hold_type="mod", submit_time='bogus-time',
                  sticky_status=False, is_locked=False, paper_id=None)
    result = hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 409


def test_mod_nosub_hold():
    exists = None
    result = hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404


def test_mod_islocked():
    exists = dict(status=SUBMITTED, reason=None, hold_user_id=None,
                  hold_type=None, submit_time='bogus-time',
                  sticky_status=False, is_locked=True, paper_id=None)
    result = hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403


def test_mod_bad_sub_status():
    for status in status_by_number.keys():
        if status in (1,2,4):
            continue
        
        exists = dict(status=status,
                      reason=None, hold_user_id=None,
                      hold_type=None, submit_time='bogus-time',
                      sticky_status=False, is_locked=False, paper_id=None)
        result = hold_biz_logic(
            ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
        assert result
        assert result.status_code == 409


def test_mod_to_admin_hold():
    exists = dict(status=ON_HOLD, reason="discussion", hold_user_id=1234,
                  hold_type="mod", submit_time='bogus-time',
                  sticky_status=False, is_locked=False, paper_id=None)
    result = hold_biz_logic(
        Reject(type='admin', reason='nonresearch'), exists, sub_id, mod_user)
    assert result
    assert 'Admin Hold' in '|||'.join(result.visible_comments)
    assert 'nonresearch' in '|||'.join(result.visible_comments)
    assert result.modapi_comments
    assert result.delete_hold_reason
    assert result.create_hold_reason



def test_hold_new_admin_hold():
    exists = dict(status=SUBMITTED, reason=None, hold_user_id=1234,
                  type=None, submit_time='bogus-time',
                  sticky_status=False, is_locked=False, paper_id=None)
    hold = Reject(type='admin', reason='nonresearch')
    result = hold_biz_logic(hold, exists, 1234, admin_user)
    assert result
    assert "Admin Hold" in '|||'.join(result.visible_comments)


def test_release_bad_user():    
    bad_user = User(user_id=1111111, name='JustANonModUser', username='mjanmu', is_moderator=False,
                    is_admin=False, moderated_categories=[])
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
    
    
def test_mod_cannot_release_admin_hold():
    exists = dict(status=ON_HOLD, reason=None, hold_user_id=1234,
                  type="admin", submit_time='bogus-time',
                  sticky_status=False, is_locked=False, paper_id=None)
    result = release_biz_logic(exists, 1234, mod_user, None)
    assert result
    assert result.status_code == 403


def test_release_legacy_hold(mocker):
    exists = dict(status=ON_HOLD, reason=None, hold_user_id=1234,
                  type=None, submit_time='bogus-time',
                  sticky_status=False, is_locked=False, paper_id=None)
    result = release_biz_logic(exists, 1234, admin_user, lambda _: datetime.fromisoformat("2010-05-14T00:00:00+00:00"))
    assert result
    assert isinstance(result, HoldReleaseLogicRes)
    assert result.paper_id == 'submit/1234'

def test_hold_existing_admin_hold():
    exists = dict(status=ON_HOLD, reason=None, hold_user_id=1234,
                  type="admin", submit_time='bogus-time',
                  sticky_status=False, is_locked=False, paper_id=None)
    hold = Reject(type='admin', reason='nonresearch')
    result = hold_biz_logic(hold, exists, 1234, admin_user)
    assert result
    assert result.status_code == 409

