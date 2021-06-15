import pytest
from modapi.db import get_db
from modapi.change_notification.db_changes import  _check_for_changes

@pytest.mark.asyncio
async def test_periodic_check(client):

    latest, changes = await _check_for_changes(get_db, 0)
    assert len(changes) > 0
    assert latest == 16829989
    latest, changes = await _check_for_changes(get_db, latest)
    assert changes == []
    assert latest == 16829989

    
