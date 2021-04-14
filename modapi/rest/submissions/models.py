"""SQLAlchemy ORM classes for the classic database."""

# 2021-04-02 BDC This was copied from
# submission-core/core/arxiv/services/classic/models.py commit 6077ce4
# Ideally this file would not be copied. arXiv could have a python
# package that is a domain agnostic SQLAlchemy model of the classic
# database that could be resued in a baggage free way in many
# services.

from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    text,
    Integer,
    SmallInteger,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from modapi.db import arxiv_models

import logging

logger = logging.getLogger(__name__)


class Submitter(arxiv_models.TapirUsers):
    username = relationship("TapirNicknames", uselist=False)
    @orm.reconstructor
    def init_on_load(self):
        # TODO suspect is a regex from the DB!
        # This is probably taking a long time in legacy
        self.is_suspect = False
        self.name = self.username.nickname


class SubmissionsOut(arxiv_models.Submissions):  # type: ignore
    # Pre-moderation stages; these are tied to the classic submission UI.
    NEW = 0
    STARTED = 1
    FILES_ADDED = 2
    PROCESSED = 3
    METADATA_ADDED = 4
    SUBMITTED = 5
    STAGES = [NEW, STARTED, FILES_ADDED, PROCESSED, METADATA_ADDED, SUBMITTED]

    # Submission status; this describes where the submission is in the
    # publication workflow.
    NOT_SUBMITTED = 0  # Working.
    SUBMITTED = 1  # Enqueued for moderation, to be scheduled.
    ON_HOLD = 2
    UNUSED = 3
    NEXT_PUBLISH_DAY = 4
    """Scheduled for the next publication cycle."""
    PROCESSING = 5
    """Scheduled for today."""
    NEEDS_EMAIL = 6
    """Announced, not yet announced."""

    ANNOUNCED = 7
    DELETED_ANNOUNCED = 27
    """Announced and files expired."""

    PROCESSING_SUBMISSION = 8
    REMOVED = 9  # This is "rejected".

    USER_DELETED = 10
    ERROR_STATE = 19
    """There was a problem validating the submission during publication."""

    DELETED_EXPIRED = 20
    """Was working but expired."""
    DELETED_ON_HOLD = 22
    DELETED_PROCESSING = 25

    DELETED_REMOVED = 29
    DELETED_USER_EXPIRED = 30
    """User deleted and files expired."""

    DELETED = (
        USER_DELETED,
        DELETED_ON_HOLD,
        DELETED_PROCESSING,
        DELETED_REMOVED,
        DELETED_USER_EXPIRED,
        DELETED_EXPIRED,
    )

    NEW_SUBMISSION = "new"
    REPLACEMENT = "rep"
    JOURNAL_REFERENCE = "jref"
    WITHDRAWAL = "wdr"
    CROSS_LIST = "cross"
    WITHDRAWN_FORMAT = "withdrawn"

    submitter = relationship("Submitter")
    submission_category = relationship(
        "SubmissionCategory",
        back_populates="submission",
    )


    @property
    def primary_classification(self) -> Optional["Category"]:
        """Get the primary classification for this submission."""
        categories = [
            db_cat for db_cat in self.submission_category if db_cat.is_primary == 1
        ]
        try:
            cat: Category = categories[0].category
        except Exception:
            return None
        return cat

    def get_arxiv_id(self) -> Optional[str]:
        """Get the arXiv identifier for this submission."""
        if not self.document:
            return None
        paper_id: Optional[str] = self.document.paper_id
        return paper_id

    def get_created(self) -> datetime:
        """Get the UTC-localized creation datetime."""
        dt: datetime = self.created.replace(tzinfo=timezone.utc)
        return dt

    def get_updated(self) -> datetime:
        """Get the UTC-localized updated datetime."""
        dt: datetime = self.updated.replace(tzinfo=timezone.utc)
        return dt

    def is_working(self) -> bool:
        return bool(self.status == self.NOT_SUBMITTED)

    def is_announced(self) -> bool:
        return bool(self.status in [self.ANNOUNCED, self.DELETED_ANNOUNCED])

    def is_active(self) -> bool:
        return bool(not self.is_announced() and not self.is_deleted())

    def is_rejected(self) -> bool:
        return bool(self.status == self.REMOVED)

    def is_finalized(self) -> bool:
        return bool(self.status > self.WORKING and not self.is_deleted())

    def is_deleted(self) -> bool:
        return bool(self.status in self.DELETED)

    def is_on_hold(self) -> bool:
        return bool(self.status == self.ON_HOLD)

    def is_new_version(self) -> bool:
        """Indicate whether this row represents a new version."""
        return bool(self.type in [self.NEW_SUBMISSION, self.REPLACEMENT])

    def is_withdrawal(self) -> bool:
        return bool(self.type == self.WITHDRAWAL)

    def is_crosslist(self) -> bool:
        return bool(self.type == self.CROSS_LIST)

    def is_jref(self) -> bool:
        return bool(self.type == self.JOURNAL_REFERENCE)

    @property
    def secondary_categories(self) -> List[str]:
        """Category names from this submission's secondary classifications."""
        return [c.category for c in self.submission_category if c.is_primary == 0]

