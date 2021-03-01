import sqlalchemy
from sqlalchemy.sql import select
from modapi.arxiv_schema import (
    ArXivDocuments,
    ArXivSubmissions,
    ArXivSubmissionAbsClassifierData,
    ArXivSubmissionCategory,
    ArXivSubmissionCategoryProposal,
    ArXivSubmissionViewFlag,
    TapirNicknames,
    TapirUsers,
)

import modapi.rest.model as model


def get_submission(database, sub_id: int) -> model.Submission:
    """Gets a submission from the DB by submission ID"""
    stmt = ArXivSubmissions.select( [ArXivSubmissions.submission_id,
                   ArXivSubmissions.auto_hold,
                   ArXivSubmissions.is_oversize,
                   ArXivSubmissions.comments, ArXivSubmissions.proxy ,
                   ArXivSubmissions.report_num,
                   ArXivSubmissions.msc_class,
                   ArXivSubmissions.acm_class,
                   ArXivSubmissions.journal_ref, ArXivSubmissions.doi ,
                   ArXivSubmissions.source_size,
                   ArXivSubmissions.submitter_email,
                   ArXivSubmissions.abstract, ArXivSubmissions.authors,
                   ArXivSubmissions.type , ArXivSubmissions.status,
                   ArXivSubmissions.doc_paper_id,
                   ArXivSubmissions.document_id,
                   ArXivSubmissions.submitter_name ,
                   ArXivSubmissions.submitter_id,
                   ArXivSubmissions.title, ArXivSubmissions.is_ok,
                   ArXivSubmissions.submit_time,] )\
                   .where(ArXivSubmissions.submission_id == sub_id)
    return database.execute(stmt)


#    query = schema.ArxivSubmissions.
