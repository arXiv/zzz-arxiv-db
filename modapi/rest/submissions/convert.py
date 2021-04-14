"""Funcitons to convert from SQLAlchemy ORM to dicts for Pydantic"""

import json
from contextlib import suppress

from sqlalchemy.orm.attributes import instance_dict

from modapi.db import arxiv_models
from modapi.rest import schema

from modapi.userstore import to_name

def to_submission(sub: arxiv_models.Submissions) -> schema.Submission:
    """Convert a submission to an object approprate to use as a response"""
    out = instance_dict(sub)
    # for key in list(out.keys()):
    #     if key.startswith('_'):
    #         del out[key]

    # these have to be done before instance_dict
    # because that somehow messes up SQLALCHEMY ORM
    cats = make_categories(sub)
    name = to_name(sub.submitter.first_name, sub.submitter.last_name)
    suspect = _suspect(sub)

    out["submitter"] = instance_dict(sub.submitter)
    out["submitter"]["is_suspect"] = suspect
    out["submitter"]["name"] = name
    out["submission_category"] = instance_dict(sub.submission_category)
    out["categories"] = cats
    out["status"] = status_by_number[sub.status]
    out["submitter_comments"] = sub.comments
    return out


def _suspect(sub: arxiv_models.Submissions) -> bool:
    rv = False
    with suppress(AttributeError):
        rv = sub.submitter.demographics.flag_suspect
    return rv


def make_categories(sub: arxiv_models.Submissions):
    """Makes a schema.Categories object"""
    # ex {score: 1.2, category: 'q-fin.GN' }
    # acd = [{'score': ]
    return dict(
        classifier_scores=make_classifier(sub),
        new_crosses=[],  # TODO
        proposals=make_proposals(sub),
        submission=dict(
            primary=sub.primary_classification, secondary=sub.secondary_categories
        ),
    )


def make_classifier(sub: arxiv_models.Submissions):
    """Make the classifier data for the submission"""
    try:
        abs_clz = sub.abs_classifier_data
        if not abs_clz or not hasattr(abs_clz, "json"):
            return []
        data = json.loads(abs_clz.json)
        return [
            {"category": row["category"], "score": row["probability"]}
            for row in data["classifier"]
        ]
    except Exception:
        return []


def make_proposals(sub: arxiv_models.Submissions):
    # need to handle type and is_system_proposal
    resolved = [
        convert_prop(prop)
        for prop in sub.proposals
        if prop.response_comment_id and prop.response_comment_id != "null"
    ]
    unresolved = [
        convert_prop(prop)
        for prop in sub.proposals
        if not prop.response_comment_id or prop.response_comment_id == "null"
    ]
    return dict(resolved=resolved, unresolved=unresolved)


def convert_prop(prop: arxiv_models.SubmissionCategoryProposal):
    out = instance_dict(prop)
    out["is_system_proposal"] = False  # TODO
    out["type"] = "primary" if prop.is_primary else "secondary"
    return out


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
