"""Funcitons to convert from SQLAlchemy ORM to dicts for Pydantic"""

import json
from contextlib import suppress

from sqlalchemy.orm.attributes import instance_dict

from modapi.auth import User
from modapi.tables import arxiv_models
from modapi.rest import schema

import logging

log = logging.getLogger(__name__)

SYSTEM_USER_ID = 41106
"""ID of the system user"""

resolutions = ["unresolved", "accepted as primary", "accepted as secondary", "rejected"]


def to_submission(sub: arxiv_models.Submissions, user: User) -> schema.Submission:
    """Convert a submission to an object approprate to use as a response"""
    out = instance_dict(sub)
    cats = make_categories(sub)
    suspect = _suspect(sub)
    out["submitter"] = instance_dict(sub.submitter)
    out["submitter"]["is_suspect"] = suspect
    out["submitter"]["name"] = sub.submitter_name
    out["submission_category"] = instance_dict(sub.submission_category)
    out["categories"] = cats
    out["status"] = status_by_number[sub.status]
    out["submitter_comments"] = sub.comments
    out["comment_count"] = len(
        [lg for lg in sub.admin_log if lg.command == "admin comment"]
    )
    out["matched"] = make_match(cats, user)
    return out


def make_match(cats: dict, user: User):
    "Determine how a submission matched to appear on moderator's list."
    mods_categories = user.moderated_categories
    mods_archives = user.moderated_archives

    for cat in mods_categories:
        if (
            (cats["submission"]["primary"] and cat == cats["submission"]["primary"])
            or cat in cats["submission"]["secondary"]
            or cat in cats["new_crosses"]
            or (
                cats["proposals"]["unresolved"]
                and cat
                in list(ucat["category"] for ucat in cats["proposals"]["unresolved"])
            )
        ):
            return "moderated_category"

    for archive in mods_archives:
        if (
            (
                cats["submission"]["primary"]
                and cats["submission"]["primary"].startswith(archive)
            )
            or any(c.startswith(archive) for c in cats["submission"]["secondary"])
            or any(c.startswith(archive) for c in cats["new_crosses"])
            or (
                cats["proposals"]["unresolved"]
                and any(
                    c.startswith(archive)
                    for c in list(
                        ucat["category"] for ucat in cats["proposals"]["unresolved"]
                    )
                )
            )
        ):
            return "moderated_archive"

    return "unknown"


def _suspect(sub: arxiv_models.Submissions) -> bool:
    rv = False
    with suppress(AttributeError):
        rv = sub.submitter.demographics.flag_suspect
    return rv


def make_categories(sub: arxiv_models.Submissions):
    """Makes a schema.Categories object"""
    return dict(
        classifier_scores=make_classifier(sub),
        new_crosses=sub.new_crosses,
        proposals=make_proposals(sub),
        submission=dict(
            primary=sub.primary_classification, secondary=sub.secondary_categories
        ),
    )


def make_classifier(sub: arxiv_models.Submissions):
    """Make the classifier data for the submission"""
    abs_clz = sub.abs_classifier_data
    if not abs_clz:
        return []

    abs_clz = abs_clz[0]
    if not abs_clz or not hasattr(abs_clz, "json") or not abs_clz.json:
        return []

    try:
        data = json.loads(abs_clz.json)
        return [
            {"category": row["category"], "score": row["probability"]}
            for row in data["classifier"]
        ]
    except Exception as err:
        log.error(
            "could not decode classifier json for submission %s: %s",
            sub.submission_id,
            err,
        )
        return [{"error": "could not parse classifier json"}]


def make_proposals(sub: arxiv_models.Submissions):
    resolved = [
        convert_prop(prop) for prop in sub.proposals if prop.proposal_status != 0
    ]
    unresolved = [
        convert_prop(prop) for prop in sub.proposals if prop.proposal_status == 0
    ]
    return dict(resolved=resolved, unresolved=unresolved)


def convert_prop(prop: arxiv_models.SubmissionCategoryProposal):
    out = instance_dict(prop)
    out["is_system_proposal"] = prop.user_id == SYSTEM_USER_ID
    out["type"] = "primary" if prop.is_primary else "secondary"
    out["status"] = prop_status(prop)
    return out


def prop_status(prop: arxiv_models.SubmissionCategoryProposal):
    if prop and prop.proposal_status < len(resolutions):
        return resolutions[prop.proposal_status]
    else:
        return f"unknown status: {prop.prop_status}"


status_by_number = {
    # --- 'is_current' method statuses ( 0 - 4 )
    0: "working",  # incomplete; not submitted
    1: "submitted",
    2: "on hold",
    3: "unused",
    4: "next",  # for tomorrow
    # --- 'is_processing' method statuses (5 - 8)
    5: "processing",
    6: "needs_email",
    7: "published",
    8: "processing(submitting)",  # text extraction , etc
    # --- removed or error
    9: "removed",
    10: "user deleted",
    19: "error state",
    # --- expired (files removed) status are the above +20, usual ones are:
    20: "deleted(working)",  # was working but expired
    22: "deleted(on hold)",
    25: "deleted(processing)",
    27: "deleted(published)",  # published and files expired
    29: "deleted(removed)",
    30: "deleted(user deleted)",  # user deleted and files expired
}
