from fastapi import FastAPI
from .collab_app import sio
from .config import allow_origins

from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

fast_app = FastAPI()

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@fast_app.get("/")
async def root():
    return {"status": "ready"}

@fast_app.get("/testRestToSocket")
async def rtos():
    await sio.emit("in_edit", {"id": "submission1234", "editor": "bob", "scope": "mod"})
    return {"did it": True}


#################### fast_api ####################


@fast_app.get("/status")
async def status():
    """Get the status of the ModAPI service."""
    return {"status": "ready"}


@fast_app.get("/queue_alt/{submission_id}")
async def queue_alt(submission_id: Optional[int] = None):
    return {"error": "not implemented"}


@fast_app.get("/submission/{submission_id}")
async def submission(submission_id: int):
    return {"error": "not implemented"}


@fast_app.get("/category_taxonomy")
async def category_taxonomy():
    return {"error": "not implemented"}


@fast_app.get("/comments/{submission_id}")
async def comments(submission_id: Optional[int] = None):
    return {"error": "not implemented"}


@fast_app.put("/comment/{submission_id}")
async def comment(submission_id: int):
    return {"error": "not implemented"}


@fast_app.get("/proposals/{submission_id}")
async def proposals(submission_id: int):
    return {"error": "not implemented"}


@fast_app.put("/proposals/{submission_id}")
async def proposals(submission_id: int):
    return {"error": "not implemented"}


@fast_app.put("/proposal_response/{submission_id}")
async def proposal_response(submission_id: int):
    return {"error": "not implemented"}


@fast_app.put("/category_rejection/{submission_id}")
async def category_rejection(submission_id: int):
    return {"error": "not implemented"}


@fast_app.put("/category_promotion/{submission_id}")
async def category_promotion(submission_id: int):
    return {"error": "not implemented"}


@fast_app.get("/moderators/{submission_id}")
async def moderators(submission_id: int):
    return {"error": "not implemented"}


@fast_app.get("/classifier_scores/{submission_id}")
async def classifier_scores(submission_id: int):
    return {"error": "not implemented"}


@fast_app.get("/categories/{submission_id}")
async def categories(submission_id: int):
    return {"error": "not implemented"}


@fast_app.get("/view_flag/{submission_id}")
async def view_flag(submission_id: int):
    return {"error": "not implemented"}


@fast_app.put("/view_flag/{submission_id}")
async def view_flag_put(submission_id: int):
    return {"error": "not implemented"}
