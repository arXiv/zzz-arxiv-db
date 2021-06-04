from modapi.rest.holds import _hold_biz_logic, ModHoldIn, status_by_number, Reject

from modapi.auth import User
from fastapi.responses import JSONResponse


mod_user = User(user_id=1111111, name='M The Mod', username='mtm', is_moderator=True,
                is_admin=False, moderated_categories=['cs.LG'])

admin_user = User(user_id=99999, name='A The Admin',
                  username='ata', is_admin=True)

sub_id = 3434343


def test_mod_new_hold():
    exists = dict(status=1, reason=None, hold_user_id=None,
                  hold_type=None, submit_time='bogus-time',
                  sticky_status=False, is_locked=False)
    result = _hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert result
    assert 'Mod Hold' in '|||'.join(result.visible_comments)
    assert 'discussion' in '|||'.join(result.visible_comments)
    assert result.modapi_comments
    assert not result.delete_hold_reason
    assert result.create_hold_reason


def test_mod_duplicate_hold():
    exists = dict(status=1, reason="discussion", hold_user_id="2343",
                  hold_type="mod", submit_time='bogus-time',
                  sticky_status=False, is_locked=False)
    result = _hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 409


def test_mod_nosub_hold():
    exists = None
    result = _hold_biz_logic(
        ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
    assert isinstance(result, JSONResponse)
    assert result.status_code == 404


def test_mod_islocked():
    exists = dict(status=1, reason=None, hold_user_id=None,
                  hold_type=None, submit_time='bogus-time',
                  sticky_status=False, is_locked=True)
    result = _hold_biz_logic(
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
                      sticky_status=False, is_locked=False)
        result = _hold_biz_logic(
            ModHoldIn(type='mod', reason='discussion'), exists, sub_id, mod_user)
        assert result
        assert result.status_code == 409


def test_mod_to_admin_hold():
    exists = dict(status=2, reason="discussion", hold_user_id=1234,
                  hold_type="mod", submit_time='bogus-time',
                  sticky_status=False, is_locked=False)
    result = _hold_biz_logic(
        Reject(type='admin', reason='nonresearch'), exists, sub_id, mod_user)
    assert result
    assert 'Admin Hold' in '|||'.join(result.visible_comments)
    assert 'nonresearch' in '|||'.join(result.visible_comments)
    assert result.modapi_comments
    assert result.delete_hold_reason
    assert result.create_hold_reason

