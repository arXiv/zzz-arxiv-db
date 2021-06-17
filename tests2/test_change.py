import pytest
from modapi.change_notification.db_changes import  _check_for_changes

MAX_ADMIN_LOG_ID_IN_TEST_DB=1

@pytest.mark.asyncio
async def test_periodic_check(get_test_db):
    latest, changes = await _check_for_changes(get_test_db, 0)
    assert len(changes) > 0
    assert latest == MAX_ADMIN_LOG_ID_IN_TEST_DB

    latest, changes = await _check_for_changes(get_test_db, latest)
    assert changes == []
    assert latest == 1
    
