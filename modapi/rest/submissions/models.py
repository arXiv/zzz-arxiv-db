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

    # @orm.reconstructor
    # def init_on_load(self):
    #     self.categories = make_categories(self)

    @property
    def categories(self):
        return make_categories(self)

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

    # def _update_submitter(self, submission: domain.Submission) -> None:
    #     """Update submitter information on this row."""
    #     self.submitter_id = submission.creator.native_id
    #     self.submitter_email = submission.creator.email

    # def _update_primary(self, submission: domain.Submission) -> None:
    #     """Update primary classification on this row."""
    #     assert submission.primary_classification is not None
    #     primary_category = submission.primary_classification.category
    #     cur_primary = self.primary_classification

    #     if cur_primary and cur_primary.category != primary_category:
    #         self.categories.remove(cur_primary)
    #         self.categories.append(
    #             SubmissionCategory(submission_id=self.submission_id,
    #                                category=primary_category)
    #         )
    #     elif cur_primary is None and primary_category:
    #         self.categories.append(
    #             SubmissionCategory(
    #                 submission_id=self.submission_id,
    #                 category=primary_category,
    #                 is_primary=1
    #             )
    #         )

    # def _update_secondaries(self, submission: domain.Submission) -> None:
    #     """Update secondary classifications on this row."""
    #     # Remove any categories that have been removed from the Submission.
    #     for db_cat in self.categories:
    #         if db_cat.is_primary == 1:
    #             continue
    #         if db_cat.category not in submission.secondary_categories:
    #             self.categories.remove(db_cat)

    #     # Add any new secondaries
    #     for cat in submission.secondary_classification:
    #         if cat.category not in self.secondary_categories:
    #             self.categories.append(
    #                 SubmissionCategory(
    #                     submission_id=self.submission_id,
    #                     category=cat.category,
    #                     is_primary=0
    #                 )
    #             )



# class User(Base):  # type: ignore
#     """Represents an arXiv user."""

#     __tablename__ = "tapir_users"

#     user_id = Column(Integer, primary_key=True)
#     first_name = Column(String(50), index=True)
#     last_name = Column(String(50), index=True)
#     suffix_name = Column(String(50))
#     share_first_name = Column(Integer, nullable=False, server_default=text("'1'"))
#     share_last_name = Column(Integer, nullable=False, server_default=text("'1'"))
#     email = Column(String(255), nullable=False, unique=True, server_default=text("''"))
#     share_email = Column(Integer, nullable=False, server_default=text("'8'"))
#     email_bouncing = Column(Integer, nullable=False, server_default=text("'0'"))
#     policy_class = Column(
#         ForeignKey("tapir_policy_classes.class_id"),
#         nullable=False,
#         index=True,
#         server_default=text("'0'"),
#     )
#     """
#     +----------+---------------+
#     | class_id | name          |
#     +----------+---------------+
#     |        1 | Administrator |
#     |        2 | Public user   |
#     |        3 | Legacy user   |
#     +----------+---------------+
#     """

#     joined_date = Column(
#         Integer, nullable=False, index=True, server_default=text("'0'")
#     )
#     joined_ip_num = Column(String(16), index=True)
#     joined_remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     flag_internal = Column(
#         Integer, nullable=False, index=True, server_default=text("'0'")
#     )
#     flag_edit_users = Column(
#         Integer, nullable=False, index=True, server_default=text("'0'")
#     )
#     flag_edit_system = Column(Integer, nullable=False, server_default=text("'0'"))
#     flag_email_verified = Column(Integer, nullable=False, server_default=text("'0'"))
#     flag_approved = Column(
#         Integer, nullable=False, index=True, server_default=text("'1'")
#     )
#     flag_deleted = Column(
#         Integer, nullable=False, index=True, server_default=text("'0'")
#     )
#     flag_banned = Column(
#         Integer, nullable=False, index=True, server_default=text("'0'")
#     )
#     flag_wants_email = Column(Integer, nullable=False, server_default=text("'0'"))
#     flag_html_email = Column(Integer, nullable=False, server_default=text("'0'"))
#     tracking_cookie = Column(
#         String(255), nullable=False, index=True, server_default=text("''")
#     )
#     flag_allow_tex_produced = Column(
#         Integer, nullable=False, server_default=text("'0'")
#     )

#     tapir_policy_class = relationship("PolicyClass")
#     username = relationship("Username", uselist=False)

#     @orm.reconstructor
#     def init_on_load(self):
#         # TODO suspect is a regex from the DB!
#         # This is probably taking a long time in legacy
#         self.is_suspect = False
#         self.name = self.username.nickname

#     # def to_user(self) -> domain.agent.User:
#     #     return domain.agent.User(
#     #         self.user_id,
#     #         self.email,
#     #         username=self.username,
#     #         forename=self.first_name,
#     #         surname=self.last_name,
#     #         suffix=self.suffix_name
#     #     )


# class Username(Base):  # type: ignore
#     """
#     Users' usernames (because why not have a separate table).

#     +--------------+------------------+------+-----+---------+----------------+
#     | Field        | Type             | Null | Key | Default | Extra          |
#     +--------------+------------------+------+-----+---------+----------------+
#     | nick_id      | int(10) unsigned | NO   | PRI | NULL    | autoincrement  |
#     | nickname     | varchar(20)      | NO   | UNI |         |                |
#     | user_id      | int(4) unsigned  | NO   | MUL | 0       |                |
#     | user_seq     | int(1) unsigned  | NO   |     | 0       |                |
#     | flag_valid   | int(1) unsigned  | NO   | MUL | 0       |                |
#     | role         | int(10) unsigned | NO   | MUL | 0       |                |
#     | policy       | int(10) unsigned | NO   | MUL | 0       |                |
#     | flag_primary | int(1) unsigned  | NO   |     | 0       |                |
#     +--------------+------------------+------+-----+---------+----------------+
#     """

#     __tablename__ = "tapir_nicknames"

#     nick_id = Column(Integer, primary_key=True)
#     nickname = Column(String(20), nullable=False, unique=True, index=True)
#     user_id = Column(
#         ForeignKey("tapir_users.user_id"), nullable=False, server_default=text("'0'")
#     )
#     user = relationship("User")
#     user_seq = Column(Integer, nullable=False, server_default=text("'0'"))
#     flag_valid = Column(Integer, nullable=False, server_default=text("'0'"))
#     role = Column(Integer, nullable=False, server_default=text("'0'"))
#     policy = Column(Integer, nullable=False, server_default=text("'0'"))
#     flag_primary = Column(Integer, nullable=False, server_default=text("'0'"))

#     user = relationship("User")


# # TODO: what is this?
# class PolicyClass(Base):  # type: ignore
#     """Defines user roles in the system."""

#     __tablename__ = "tapir_policy_classes"

#     class_id = Column(SmallInteger, primary_key=True)
#     name = Column(String(64), nullable=False, server_default=text("''"))
#     description = Column(Text, nullable=False)
#     password_storage = Column(Integer, nullable=False, server_default=text("'0'"))
#     recovery_policy = Column(Integer, nullable=False, server_default=text("'0'"))
#     permanent_login = Column(Integer, nullable=False, server_default=text("'0'"))


# class Tracking(Base):  # type: ignore
#     """Record of SWORD submissions."""

#     __tablename__ = "arXiv_tracking"

#     tracking_id = Column(Integer, primary_key=True)
#     sword_id = Column(
#         Integer, nullable=False, unique=True, server_default=text("'00000000'")
#     )
#     paper_id = Column(String(32), nullable=False)
#     submission_errors = Column(Text)
#     timestamp = Column(
#         DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     )


# class ArchiveCategory(Base):  # type: ignore
#     """Maps categories to the archives in which they reside."""

#     __tablename__ = "arXiv_archive_category"

#     archive_id = Column(
#         String(16), primary_key=True, nullable=False, server_default=text("''")
#     )
#     category_id = Column(String(32), primary_key=True, nullable=False)


# class ArchiveDef(Base):  # type: ignore
#     """Defines the archives in the arXiv classification taxonomy."""

#     __tablename__ = "arXiv_archive_def"

#     archive = Column(String(16), primary_key=True, server_default=text("''"))
#     name = Column(String(255))


# class ArchiveGroup(Base):  # type: ignore
#     """Maps archives to the groups in which they reside."""

#     __tablename__ = "arXiv_archive_group"

#     archive_id = Column(
#         String(16), primary_key=True, nullable=False, server_default=text("''")
#     )
#     group_id = Column(
#         String(16), primary_key=True, nullable=False, server_default=text("''")
#     )


# class Archive(Base):  # type: ignore
#     """Supplemental data about archives in the classification hierarchy."""

#     __tablename__ = "arXiv_archives"

#     archive_id = Column(String(16), primary_key=True, server_default=text("''"))
#     in_group = Column(
#         ForeignKey("arXiv_groups.group_id"),
#         nullable=False,
#         index=True,
#         server_default=text("''"),
#     )
#     archive_name = Column(String(255), nullable=False, server_default=text("''"))
#     start_date = Column(String(4), nullable=False, server_default=text("''"))
#     end_date = Column(String(4), nullable=False, server_default=text("''"))
#     subdivided = Column(Integer, nullable=False, server_default=text("'0'"))

#     arXiv_group = relationship("Group")


# class GroupDef(Base):  # type: ignore
#     """Defines the groups in the arXiv classification taxonomy."""

#     __tablename__ = "arXiv_group_def"

#     archive_group = Column(String(16), primary_key=True, server_default=text("''"))
#     name = Column(String(255))


# class Group(Base):  # type: ignore
#     """Supplemental data about groups in the classification hierarchy."""

#     __tablename__ = "arXiv_groups"

#     group_id = Column(String(16), primary_key=True, server_default=text("''"))
#     group_name = Column(String(255), nullable=False, server_default=text("''"))
#     start_year = Column(String(4), nullable=False, server_default=text("''"))


# class EndorsementDomain(Base):  # type: ignore
#     """Endorsement configurations."""

#     __tablename__ = "arXiv_endorsement_domains"

#     endorsement_domain = Column(String(32), primary_key=True, server_default=text("''"))
#     endorse_all = Column(Enum("y", "n"), nullable=False, server_default=text("'n'"))
#     mods_endorse_all = Column(
#         Enum("y", "n"), nullable=False, server_default=text("'n'")
#     )
#     endorse_email = Column(Enum("y", "n"), nullable=False, server_default=text("'y'"))
#     papers_to_endorse = Column(SmallInteger, nullable=False, server_default=text("'4'"))


# class Category(Base):  # type: ignore
#     """Supplemental data about arXiv categories, including endorsement."""

#     __tablename__ = "arXiv_categories"

#     arXiv_endorsement_domain = relationship("EndorsementDomain")

#     archive = Column(
#         ForeignKey("arXiv_archives.archive_id"),
#         primary_key=True,
#         nullable=False,
#         server_default=text("''"),
#     )
#     """E.g. cond-mat, astro-ph, cs."""
#     arXiv_archive = relationship("Archive")

#     subject_class = Column(
#         String(16), primary_key=True, nullable=False, server_default=text("''")
#     )
#     """E.g. AI, spr-con, str-el, CO, EP."""

#     definitive = Column(Integer, nullable=False, server_default=text("'0'"))
#     active = Column(Integer, nullable=False, server_default=text("'0'"))
#     """Only use rows where active == 1."""

#     category_name = Column(String(255))
#     endorse_all = Column(
#         Enum("y", "n", "d"), nullable=False, server_default=text("'d'")
#     )
#     endorse_email = Column(
#         Enum("y", "n", "d"), nullable=False, server_default=text("'d'")
#     )
#     endorsement_domain = Column(
#         ForeignKey("arXiv_endorsement_domains.endorsement_domain"), index=True
#     )
#     """E.g. astro-ph, acc-phys, chem-ph, cs."""

#     papers_to_endorse = Column(SmallInteger, nullable=False, server_default=text("'0'"))


# class AdminLogEntry(Base):  # type: ignore
#     """

#     +---------------+-----------------------+------+-----+-------------------+
#     | Field         | Type                  | Null | Key | Default           |
#     +---------------+-----------------------+------+-----+-------------------+
#     | id            | int(11)               | NO   | PRI | NULL              |
#     | logtime       | varchar(24)           | YES  |     | NULL              |
#     | created       | timestamp             | NO   |     | CURRENT_TIMESTAMP |
#     | paper_id      | varchar(20)           | YES  | MUL | NULL              |
#     | username      | varchar(20)           | YES  |     | NULL              |
#     | host          | varchar(64)           | YES  |     | NULL              |
#     | program       | varchar(20)           | YES  |     | NULL              |
#     | command       | varchar(20)           | YES  | MUL | NULL              |
#     | logtext       | text                  | YES  |     | NULL              |
#     | document_id   | mediumint(8) unsigned | YES  |     | NULL              |
#     | submission_id | int(11)               | YES  | MUL | NULL              |
#     | notify        | tinyint(1)            | YES  |     | 0                 |
#     +---------------+-----------------------+------+-----+-------------------+
#     """

#     __tablename__ = "arXiv_admin_log"

#     id = Column(Integer, primary_key=True)
#     logtime = Column(String(24), nullable=True)
#     created = Column(DateTime, default=lambda: datetime.now(timezone.utc))
#     paper_id = Column(String(20), nullable=True)
#     username = Column(String(20), nullable=True)
#     host = Column(String(64), nullable=True)
#     program = Column(String(20), nullable=True)
#     command = Column(String(20), nullable=True)
#     logtext = Column(Text, nullable=True)
#     document_id = Column(Integer, nullable=True)
#     submission_id = Column(Integer, nullable=True)
#     notify = Column(Integer, nullable=True, default=0)


# class CategoryProposal(Base):  # type: ignore
#     """
#     Represents a proposal to change the classification of a submission.

#     +---------------------+-----------------+------+-----+---------+
#     | Field               | Type            | Null | Key | Default |
#     +---------------------+-----------------+------+-----+---------+
#     | proposal_id         | int(11)         | NO   | PRI | NULL    |
#     | submission_id       | int(11)         | NO   | PRI | NULL    |
#     | category            | varchar(32)     | NO   | PRI | NULL    |
#     | is_primary          | tinyint(1)      | NO   | PRI | 0       |
#     | proposal_status     | int(11)         | YES  |     | 0       |
#     | user_id             | int(4) unsigned | NO   | MUL | NULL    |
#     | updated             | datetime        | YES  |     | NULL    |
#     | proposal_comment_id | int(11)         | YES  | MUL | NULL    |
#     | response_comment_id | int(11)         | YES  | MUL | NULL    |
#     +---------------------+-----------------+------+-----+---------+
#     """

#     __tablename__ = "arXiv_submission_category_proposal"

#     UNRESOLVED = 0
#     ACCEPTED_AS_PRIMARY = 1
#     ACCEPTED_AS_SECONDARY = 2
#     REJECTED = 3
#     # DOMAIN_STATUS = {
#     #     UNRESOLVED: domain.proposal.Proposal.Status.PENDING,
#     #     ACCEPTED_AS_PRIMARY: domain.proposal.Proposal.Status.ACCEPTED,
#     #     ACCEPTED_AS_SECONDARY: domain.proposal.Proposal.Status.ACCEPTED,
#     #     REJECTED: domain.proposal.Proposal.Status.REJECTED
#     # }

#     proposal_id = Column(Integer, primary_key=True)
#     submission_id = Column(ForeignKey("arXiv_submissions.submission_id"))
#     submission = relationship("Submission")
#     category = Column(String(32))
#     is_primary = Column(Integer, server_default=text("'0'"))
#     proposal_status = Column(Integer, nullable=True, server_default=text("'0'"))
#     user_id = Column(ForeignKey("tapir_users.user_id"))
#     user = relationship("User")
#     updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))
#     proposal_comment_id = Column(ForeignKey("arXiv_admin_log.id"), nullable=True)
#     proposal_comment = relationship("AdminLogEntry", foreign_keys=[proposal_comment_id])
#     response_comment_id = Column(ForeignKey("arXiv_admin_log.id"), nullable=True)
#     response_comment = relationship("AdminLogEntry", foreign_keys=[response_comment_id])

    # def status_from_domain(self, proposal: domain.proposal.Proposal) -> int:
    #     if proposal.status == domain.proposal.Proposal.Status.PENDING: 
    #         return self.UNRESOLVED
    #     elif proposal.status == domain.proposal.Proposal.Status.REJECTED:
    #         return self.REJECTED
    #     elif proposal.status == domain.proposal.Proposal.Status.ACCEPTED:
    #         if proposal.proposed_event_type \
    #                 is domain.event.SetPrimaryClassification:
    #             return self.ACCEPTED_AS_PRIMARY
    #         else:
    #             return self.ACCEPTED_AS_SECONDARY
    #     raise RuntimeError(f'Could not determine status: {proposal.status}')


# def _load_document(paper_id: str) -> Document:
#     with transaction() as session:
#         document: Document = session.query(Document) \
#             .filter(Document.paper_id == paper_id) \
#             .one()
#         if document is None:
#             raise RuntimeError('No such document')
#         return document


# def _get_user_by_username(username: str) -> User:
#     with transaction() as session:
#         u: User = session.query(Username) \
#             .filter(Username.nickname == username) \
#             .first() \
#             .user
#         return u


def make_categories(sub: SubmissionsOut):
    """Makes a schema.Categories object"""
    return dict(
        classifier_scores=[],  # TODO
        new_crosses=[],  # TODO
        proposals=dict(resolved=[], unresolved=[],),
        submission=dict(primary=sub.primary_classification,
                        secondary=sub.secondary_categories),
        )
