
from fastapi import APIRouter, Depends, status as httpstatus
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from sqlalchemy.orm import Session

from arxiv import taxonomy

from modapi.db import get_db
from modapi.tables.arxiv_models import Submissions, AdminLog

from modapi.auth import User, auth_user


router = APIRouter()

class RejectIn(BaseModel):
    category: str
    action: str
    
@router.post("/submission/{submission_id}/category_rejection")
async def post_rejection(submission_id: int,
                         reject_data: RejectIn,
                         user: User = Depends(auth_user),
                         db: Session = Depends(get_db)):
    """Rejects a subject category on a submission.

    accept_secondary means to remove the category as primary of the
    submission and set it as a secondary category of the submission.

    Rejecting the primary of a submission will put it on hold due to
    the lack of primary.
    """

    if reject_data.category not in taxonomy.CATEGORIES:
        return JSONResponse(status_code=httpstatus.HTTP_400_BAD_REQUEST,
                            content={"msg": 'Invalid category'})
        
    if not user.is_admin and not user.can_moderate(reject_data.category):
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN,
                            content={"msg": 'insufficient privileges to take action on category'})

    sub:Submissions = db.query(Submissions).filter(Submissions.submission_id == submission_id).first()
    if not sub:
        return JSONResponse(status_code=httpstatus.HTTP_404_NOT_FOUND,
                            content={"msg":"Submission not found"})

    if sub.is_locked:
            return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN,
                            content={"msg": "Submission is locked"})

    if sub.type != 'new':
        return JSONResponse(status_code=httpstatus.HTTP_409_CONFLICT,
                            content={"msg": "Rejection only supported on type new"})

    if sub.status not in [1,2,4]:
        return JSONResponse(status_code=httpstatus.HTTP_409_CONFLICT,
                            content={"msg": "Rejection only supported on status 1,2 or 4"})

    if sub.primary_category != reject_data.category \
       and reject_data.category not in sub.secondary_categories:
        return JSONResponse(status_code=httpstatus.HTTP_409_CONFLICT,
                            content={"msg": "Submission does not have rejection category"})
        
    put_on_hold = sub.status != 2 and sub.primary_classification == reject_data.category

    if reject_data.action == 'accept_secondary':
        # if the user is a mod do proposals to record it in the proposal system.
        # TODO Make and reject a primary proposal to the reject category
        # TODO Make and accept a secondary proposal to the reject category
        # TODO Log it to accept proposal?
        # else admin
        # TODO Do the change and log it
        pass
    elif reject_data.action == 'reject':
        # TODO Make and reject a primary proposal to the reject category
        # Log it and add log msg id to proposal
        # else amdin
        # TODO Do the cahnge and log it
        pass

