from sqlalchemy import Integer
from sqlalchemy.types import TypeDecorator
from datetime import datetime

from arxiv_db import arxiv_business_tz


class EpochIntArxivTz(TypeDecorator):
    """Epoch in arXiv offices TZ represted as an Integer in the db."""
    impl = Integer

    def __init__(self):
        TypeDecorator.__init__(self)

    def process_bind_param(self, dt:datetime, dialect):
        return int(dt.astimezone(arxiv_business_tz).timestamp())

    def process_result_value(self, value:int, dialect):
        return datetime.fromtimestamp(value, tz=arxiv_business_tz)
