from typing import Optional, Union, List, Literal
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from pydantic import BaseModel

#################### Business objects ####################

class ModHoldReasons(str, Enum):
    """Reasons for mod holds"""
    discussion = "discussion"
    moretime = "moretime"

class HoldType(str, Enum):
    """mod holds can be released by mods,
    admin hold can be released only by admins"""
    admin = "admin"
    mod = "mod"

class SpecificRejectReasons(str, Enum):
    """All the admin reasons except 'other'"""
    scope = "scope"
    softreject = "softreject"
    hardreject = "hardreject"
    nonresearch = "nonresearch"
    salami = "salami"


RejectReasons = Union[SpecificRejectReasons, Literal["reject-other"]]

HoldReasons = Union[RejectReasons, Literal["other"]]

SUBMITTED = 1
"""Submission table status for submitted and not on hold"""

WORKING = 0
"""Submission table status for not yet submitted"""

ON_HOLD = 2
"""Submission table status for on hold"""


@dataclass
class HoldLogicRes():
    visible_comments: List[str] =  field(default_factory=list)
    modapi_comments: List[str] =  field(default_factory=list)
    delete_hold_reason: bool = False
    create_hold_reason: bool = False
    paper_id: str = ''


@dataclass
class HoldReleaseLogicRes():
    release_to_status: str
    visible_comments: List[str] =  field(default_factory=list)
    modapi_comments: List[str] =  field(default_factory=list)
    clear_reason: bool = False
    set_release_time: Optional[datetime] = None
    paper_id: str = ''


################# API objects ##########################
class ModHoldIn(BaseModel):
    """Model for reqeusts for moderator holds."""
    type: Literal["mod"]
    reason: ModHoldReasons

class RejectOther(BaseModel):
    """Model for requests to reject the submission for some other reason with a comment."""
    type: Literal["admin"]
    reason: Literal["reject-other"]
    comment: str

class Reject(BaseModel):
    """Model for requests to reject a submission with a reason from SpecificRejectReasons."""
    type: Literal["admin"]
    reason: SpecificRejectReasons

class SendToAdminOther(BaseModel):
    """"Model for requests to put submission on hold with a comment."""
    type: Literal["admin"]
    reason: Literal["other"]
    comment: str
    sendback: bool

SendToAdminHolds = Union[Reject, RejectOther, SendToAdminOther]
"""Type for all requests that send the submission to the admins."""

HoldTypesIn = Union[ModHoldIn, SendToAdminHolds]
"""Type for all hold reqeusts."""

class HoldOut(BaseModel):
    """Hold Model for responses."""
    type: HoldType
    username: Optional[str]
    reason: Optional[Union[ModHoldReasons, HoldReasons]]

