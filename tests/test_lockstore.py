import pytest

from modapi.collab.lockstore import lock, unlock, unlock_for_sid, current_locks, is_locked

@pytest.mark.asyncio
async def test_lockstore():
    assert not await is_locked(30000)
    assert await lock(30000, 4444, 'bob') is None
    assert await is_locked(30000)
    assert await current_locks()
    assert 30000 in await current_locks()

    assert "not locked" in await unlock(2, 4444, 'bob')
    assert "not locked by" in await unlock(30000, 55, 'sue')
    assert await unlock(30000, 4444, 'bob') is None

    assert await lock(30000, 4444, 'bob') is None
    assert await lock(30001, 4444, 'bob') is None
    assert await lock(30002, 4444, 'bob') is None
    locked = await current_locks()
    assert 30000 in locked
    assert 30001 in locked
    assert 30002 in locked

    assert await unlock_for_sid(4444) != []
    assert await unlock_for_sid(4444) == []
