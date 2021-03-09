"""arXiv Moderator API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import modapi.config as config

from modapi.db import database, engine, metadata

from .mod_routes import router as mod_router
from .flags import router as flags_router
from .submissions import router as subs_router
from .status import router as status_router

metadata.create_all(engine)

fast_app = FastAPI()

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fast_app.include_router(mod_router, tags=['Holds'])
fast_app.include_router(flags_router, tags=['Flags'])
fast_app.include_router(subs_router, tags=['Submissions'])
fast_app.include_router(status_router, tags=['Service Status'])


@fast_app.on_event("startup")
async def startup():
    await database.connect()


@fast_app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
