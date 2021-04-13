"""arXiv Moderator API"""
import modapi.config as config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..db import create_tables

from .flags import router as flags_router
from .holds import router as hold_router
from .status import router as status_router
from .submissions.api import router as subs_router
from .user import router as user_router

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

# @fast_app.on_event("startup")
# async def startup():
#     await database.connect()


# @fast_app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
