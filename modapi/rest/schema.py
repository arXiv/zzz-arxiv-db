from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel


class OrmBaseModel(BaseModel):

    class Config:
        orm_mode = True  #  Reads from non-dict

        
class User(OrmBaseModel):
    is_admin: bool
    is_moderator: bool
    name: str
    username: str
    moderated_categories: List[str]
    moderated_archives: List[str]

    class Config:
        orm_mode = True  #  Reads from non-dict


class PublishTimes(OrmBaseModel):
    submitted: datetime
    next: datetime


class QueueOutline(OrmBaseModel):
    user: User
    current_time: datetime
    publish_times: PublishTimes
    last_queue_view: datetime
    num_submissions_with_actionable_proposals: int
    queue: List[str]

    class Config:
        orm_mode = True  #  Reads from non-dict


SubTypeLiterals = Literal["new", "rep", "jref", "cross", "wdr"]

StatusLiteral = Literal[1, 2, 4]

PropTypeLiterals = Literal["primary", "secondary"]

class ClassifierScore(OrmBaseModel):
    score: float
    category: str


class SubmissionClassification(OrmBaseModel):
    secondary: List[str]
    primary: Optional[str]


class Proposal(OrmBaseModel):
    response_comment_id: Optional[int]
    is_system_proposal: bool
    proposal_comment_id: int
    proposal_id: int
    category: str
    type: PropTypeLiterals
    updated: datetime


class Proposals(OrmBaseModel):
    resolved: List[Proposal]
    unresolved: List[Proposal]
    

class Categories(OrmBaseModel):
    classifier_scores: List[ClassifierScore]
    submission: SubmissionClassification
    new_crosses: List[str]
    proposals: Proposals

    
class Submitter(OrmBaseModel):
    email: str
    name: str
    is_suspect: bool
    
    class Config:
        orm_mode = True  #  Reads from non-dict

    
#TODO align Optional with database table definition 
class Submission(OrmBaseModel):
    """Submission model to transmit to client"""
    submission_id: int
    doc_paper_id: Optional[str]

    created: Optional[datetime]
    updated: Optional[datetime]
    submit_time: Optional[datetime]
    release_time: Optional[datetime]

    status: str
    version: Optional[int]
    type: Optional[str]
    
    title: Optional[str]
    authors: Optional[str]
    comments: Optional[str]
    abstract: Optional[str]

    proxy: Optional[str]
    report_num: Optional[str]
    msc_class: Optional[str]
    acm_class: Optional[str]
    journal_ref: Optional[str]
    doi: Optional[str]

    is_ok: Optional[bool]
    admin_ok: Optional[bool]

    auto_hold: Optional[bool]
    is_locked: Optional[bool]

    categories: Categories
    submitter: Submitter

    comment_count: Optional[int]
    
    class Config:
        orm_mode = True  # Reads from non-dict like SQLAlchemy returns


class ModHoldReasons(str, Enum):
    discussion = "discussion"
    moretime = "moretime"


class ModHold(OrmBaseModel):
    submission_id: int
    reason: ModHoldReasons


ModFlagLiterals = Literal["checkmark"]

modflag_to_int = {"checkmark": 1}


class Flag(OrmBaseModel):
    flag: ModFlagLiterals


class FlagOut(OrmBaseModel):
    username: str
    updated: datetime
    submission_id: int
