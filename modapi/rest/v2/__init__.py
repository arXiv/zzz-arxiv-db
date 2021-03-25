"""V2 of the NG mod API. 

We are using the v2 prefix to isolate the code from the API 
that is deployed for the closed beta round 1 (Mid March 2021).

With the v2 we can deploy breaking changes to the API and the 
arxiv-check can be updated to handle these.

Some expected changes:
- Auth on all calls
- different hold API

"""

from fastapi import APIRouter, Depends

from ..flags import router as flags_router
from .holds import router as holds_router
from ..submissions import router as subs_router

from modapi.auth import auth_user

router = APIRouter(prefix="/v2",
                   tags=["APIv2"])

router.include_router(holds_router,
                      dependencies=[Depends(auth_user)])

# Right now flags_router is shared with v1 and v2
# if changes are made to flags_router, preserve the existing
# code for v1.
router.include_router(flags_router,
                      dependencies=[Depends(auth_user)])

# Right now subs_router is shared with v1 and v2
# if changes are made to subs_router, preserve the existing
# code for v1.
router.include_router(subs_router,
                      dependencies=[Depends(auth_user)])

