from pydantic import BaseModel
from datetime import datetime
from typing import List, Literal, Optional, Union
from enum import Enum

class User(BaseModel):
    is_admin: bool
    is_moderator: bool
    name: str
    username: str
    moderated_categories: List[str]
    moderated_archives: List[str]

    class Config:
        orm_mode = True  #  Reads from non-dict


class PublishTimes(BaseModel):
    submitted: datetime
    next: datetime


class QueueOutline(BaseModel):
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

    
class Submission(BaseModel):
    submission_id: int

    doc_paper_id: Optional[str]

    is_author: Optional[bool]

    submitter_name: Optional[str]
    submitter_email: Optional[str]
    created: Optional[datetime]
    updated: Optional[datetime]
    status: Optional[int]

    submit_time: Optional[datetime]
    release_time: Optional[datetime]

    title: Optional[str]
    authors: Optional[str]
    comments: Optional[str]
    proxy: Optional[str]
    report_num: Optional[str]
    msc_class: Optional[str]
    acm_class: Optional[str]
    journal_ref: Optional[str]
    doi: Optional[str]
    abstract: Optional[str]
    version: Optional[int]
    type: Optional[str]

    is_ok: Optional[bool]
    admin_ok: Optional[bool]

    auto_hold: Optional[bool]
    is_locked: Optional[bool]

    class Config:
        orm_mode = True  #  Reads from non-dict


class SubmissionFull(BaseModel):
    submission_id: int

    doc_paper_id: Optional[str]

    userinfo: Optional[int]
    is_author: Optional[bool]
    agree_policy: Optional[bool]
    viewed: Optional[bool]
    stage: Optional[int]
    submitter_name: Optional[str]
    submitter_email: Optional[str]
    created: Optional[datetime]
    updated: Optional[datetime]
    status: Optional[int]
    sticky_status: Optional[int]
    must_process: Optional[bool]
    submit_time: Optional[datetime]
    release_time: Optional[datetime]
    source_size: Optional[int]
    source_format: Optional[str]
    source_flags: Optional[str]
    has_pilot_data: Optional[bool]
    is_withdrawn: Optional[bool]
    title: Optional[str]
    authors: Optional[str]
    comments: Optional[str]
    proxy: Optional[str]
    report_num: Optional[str]
    msc_class: Optional[str]
    acm_class: Optional[str]
    journal_ref: Optional[str]
    doi: Optional[str]
    abstract: Optional[str]
    version: Optional[int]
    type: Optional[str]
    is_ok: Optional[bool]
    admin_ok: Optional[bool]
    allow_tex_produced: Optional[bool]
    is_oversize: Optional[bool]
    remote_addr: Optional[str]
    remote_host: Optional[str]
    package: Optional[str]
    rt_ticket_id: Optional[int]
    auto_hold: Optional[bool]
    is_locked: Optional[bool]

    class Config:
        orm_mode = True  #  Reads from non-dict


class ModHoldReasons(str, Enum):
    discussion = 'discussion'
    moretime = 'moretime'


class ModHold(BaseModel):
    submission_id: int
    reason: ModHoldReasons

    
