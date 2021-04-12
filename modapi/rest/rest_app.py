"""arXiv Moderator API"""

import asyncio
import functools

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import modapi.config as config
from modapi.change_notification.db_changes import periodic_check, Changes
from modapi.collab.collab_app import send_changes

from ..db import create_tables, Session

from .flags import router as flags_router
from .holds import router as hold_router
from .status import router as status_router
from .submissions.api import router as subs_router
from .user import router as user_router

import logging

log = logging.getLogger(__name__)

create_tables()

fast_app = FastAPI()

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fast_app.include_router(flags_router, tags=['Flags'])
fast_app.include_router(subs_router, tags=['Submissions'])
fast_app.include_router(status_router, tags=['Service Status'])
fast_app.include_router(hold_router, tags=['Holds'])
fast_app.include_router(user_router, tags=['User'])

db_check_task = None


@fast_app.on_event("startup")
async def on_startup():
    async def broadcast(_, changes: Changes):
        await send_changes(changes)

    ppcf = functools.partial(periodic_check, Session, broadcast)
    global db_check_task
    db_check_task = asyncio.create_task(ppcf())
    

@fast_app.on_event("shutdown")
async def on_shutdown():
    if db_check_task:
        if db_check_task.done() and not db_check_task.cancelled() and db_check_task.exception():
            log.error("Exception in db_check_task")
            log.error(db_check_task.exception())

        if not db_check_task.done():
            db_check_task.cancel()
