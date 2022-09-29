"""arXiv database SQLAlchemy models.

This was generated with sqlacodegen on 2022-09-29 with the declarative
generator against a copy of the production database.

Some of the tables are represented with sqlalchemy tables since the
lack primary keys.

The class names were changed to remove the 'ArXiv' prefix.

"""

from sqlalchemy import BINARY, BigInteger, CHAR, Column, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, JSON, SmallInteger, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


class SubscriptionUniversalInstitution(Base):
    __tablename__ = 'Subscription_UniversalInstitution'
    __table_args__ = (
        Index('name', 'name'),
    )

    name = Column(String(255), nullable=False)
    id = Column(Integer, primary_key=True)
    resolver_URL = Column(String(255))
    label = Column(String(255))
    alt_text = Column(String(255))
    link_icon = Column(String(255))
    note = Column(String(255))

    Subscription_UniversalInstitutionContact = relationship('SubscriptionUniversalInstitutionContact', back_populates='Subscription_UniversalInstitution')
    Subscription_UniversalInstitutionIP = relationship('SubscriptionUniversalInstitutionIP', back_populates='Subscription_UniversalInstitution')


class AdminLog(Base):
    __tablename__ = 'arXiv_admin_log'
    __table_args__ = (
        Index('arXiv_admin_log_idx_command', 'command'),
        Index('arXiv_admin_log_idx_paper_id', 'paper_id'),
        Index('arXiv_admin_log_idx_submission_id', 'submission_id'),
        Index('arXiv_admin_log_idx_username', 'username')
    )

    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    logtime = Column(String(24))
    paper_id = Column(String(20))
    username = Column(String(20))
    host = Column(String(64))
    program = Column(String(20))
    command = Column(String(20))
    logtext = Column(Text)
    document_id = Column(MEDIUMINT)
    submission_id = Column(Integer)
    notify = Column(TINYINT(1), server_default=text("'0'"))

    arXiv_submission_category_proposal = relationship('SubmissionCategoryProposal', foreign_keys='[SubmissionCategoryProposal.proposal_comment_id]', back_populates='proposal_comment')
    arXiv_submission_category_proposal_ = relationship('SubmissionCategoryProposal', foreign_keys='[SubmissionCategoryProposal.response_comment_id]', back_populates='response_comment')
    arXiv_submission_hold_reason = relationship('SubmissionHoldReason', back_populates='comment')


t_arXiv_admin_state = Table(
    'arXiv_admin_state', metadata,
    Column('document_id', Integer),
    Column('timestamp', TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    Column('abs_timestamp', Integer),
    Column('src_timestamp', Integer),
    Column('state', Enum('pending', 'ok', 'bad'), nullable=False, server_default=text("'pending'")),
    Column('admin', String(32)),
    Column('comment', String(255)),
    Index('document_id', 'document_id', unique=True)
)


class ArchiveCategory(Base):
    __tablename__ = 'arXiv_archive_category'

    archive_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    category_id = Column(String(32), primary_key=True, nullable=False)


class ArchiveDef(Base):
    __tablename__ = 'arXiv_archive_def'

    archive = Column(String(16), primary_key=True, server_default=text("''"))
    name = Column(String(255))


class ArchiveGroup(Base):
    __tablename__ = 'arXiv_archive_group'

    archive_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    group_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))


class AwsConfig(Base):
    __tablename__ = 'arXiv_aws_config'

    domain = Column(String(75), primary_key=True, nullable=False)
    keyname = Column(String(60), primary_key=True, nullable=False)
    value = Column(String(150))


class AwsFiles(Base):
    __tablename__ = 'arXiv_aws_files'
    __table_args__ = (
        Index('type', 'type'),
    )

    type = Column(String(10), nullable=False, server_default=text("''"))
    filename = Column(String(100), primary_key=True, server_default=text("''"))
    md5sum = Column(String(50))
    content_md5sum = Column(String(50))
    size = Column(Integer)
    timestamp = Column(DateTime)
    yymm = Column(String(4))
    seq_num = Column(Integer)
    first_item = Column(String(20))
    last_item = Column(String(20))
    num_items = Column(Integer)


class BibFeeds(Base):
    __tablename__ = 'arXiv_bib_feeds'

    bib_id = Column(MEDIUMINT, primary_key=True)
    name = Column(String(64), nullable=False, server_default=text("''"))
    priority = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    strip_journal_ref = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    uri = Column(String(255))
    identifier = Column(String(255))
    version = Column(String(255))
    concatenate_dupes = Column(Integer)
    max_updates = Column(Integer)
    email_errors = Column(String(255))
    prune_ids = Column(Text)
    prune_regex = Column(Text)
    enabled = Column(TINYINT(1), server_default=text("'0'"))


class BibUpdates(Base):
    __tablename__ = 'arXiv_bib_updates'

    update_id = Column(MEDIUMINT, primary_key=True)
    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    bib_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    journal_ref = Column(Text)
    doi = Column(Text)


t_arXiv_black_email = Table(
    'arXiv_black_email', metadata,
    Column('pattern', String(64))
)


t_arXiv_block_email = Table(
    'arXiv_block_email', metadata,
    Column('pattern', String(64))
)


class BogusCountries(Base):
    __tablename__ = 'arXiv_bogus_countries'

    user_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    country_name = Column(String(255), nullable=False, server_default=text("''"))


class CategoryDef(Base):
    __tablename__ = 'arXiv_category_def'

    category = Column(String(32), primary_key=True)
    name = Column(String(255))
    active = Column(TINYINT(1), server_default=text("'1'"))

    arXiv_document_category = relationship('DocumentCategory', back_populates='arXiv_category_def')
    arXiv_submission_category = relationship('SubmissionCategory', back_populates='arXiv_category_def')
    arXiv_submission_category_proposal = relationship('SubmissionCategoryProposal', back_populates='arXiv_category_def')


class DblpAuthors(Base):
    __tablename__ = 'arXiv_dblp_authors'
    __table_args__ = (
        Index('author_id', 'author_id', unique=True),
        Index('name', 'name', unique=True)
    )

    author_id = Column(MEDIUMINT, primary_key=True)
    name = Column(String(40))

    arXiv_dblp_document_authors = relationship('DblpDocumentAuthors', back_populates='author')


class EndorsementDomains(Base):
    __tablename__ = 'arXiv_endorsement_domains'

    endorsement_domain = Column(String(32), primary_key=True, server_default=text("''"))
    endorse_all = Column(Enum('y', 'n'), nullable=False, server_default=text("'n'"))
    mods_endorse_all = Column(Enum('y', 'n'), nullable=False, server_default=text("'n'"))
    endorse_email = Column(Enum('y', 'n'), nullable=False, server_default=text("'y'"))
    papers_to_endorse = Column(SMALLINT, nullable=False, server_default=text("'4'"))

    arXiv_categories = relationship('Categories', back_populates='arXiv_endorsement_domains')


class FreezeLog(Base):
    __tablename__ = 'arXiv_freeze_log'

    date = Column(INTEGER, primary_key=True, server_default=text("'0'"))


class GroupDef(Base):
    __tablename__ = 'arXiv_group_def'

    archive_group = Column(String(16), primary_key=True, server_default=text("''"))
    name = Column(String(255))


class Groups(Base):
    __tablename__ = 'arXiv_groups'

    group_id = Column(String(16), primary_key=True, server_default=text("''"))
    group_name = Column(String(255), nullable=False, server_default=text("''"))
    start_year = Column(String(4), nullable=False, server_default=text("''"))

    arXiv_archives = relationship('Archives', back_populates='arXiv_groups')


class Licenses(Base):
    __tablename__ = 'arXiv_licenses'

    name = Column(String(255), primary_key=True)
    label = Column(String(255))
    active = Column(TINYINT(1), server_default=text("'1'"))
    note = Column(String(400))
    sequence = Column(TINYINT)

    arXiv_metadata = relationship('Metadata', back_populates='arXiv_licenses')
    arXiv_submissions = relationship('Submissions', back_populates='arXiv_licenses')


class LogPositions(Base):
    __tablename__ = 'arXiv_log_positions'

    id = Column(String(255), primary_key=True, server_default=text("''"))
    position = Column(INTEGER)
    date = Column(INTEGER)


class MonitorKlog(Base):
    __tablename__ = 'arXiv_monitor_klog'

    t = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    sent = Column(INTEGER)


class MonitorMailq(Base):
    __tablename__ = 'arXiv_monitor_mailq'

    t = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    main_q = Column(INTEGER, nullable=False, server_default=text("'0'"))
    local_q = Column(INTEGER, nullable=False, server_default=text("'0'"))
    local_host_map = Column(INTEGER, nullable=False, server_default=text("'0'"))
    local_timeout = Column(INTEGER, nullable=False, server_default=text("'0'"))
    local_refused = Column(INTEGER, nullable=False, server_default=text("'0'"))
    local_in_flight = Column(INTEGER, nullable=False, server_default=text("'0'"))


class MonitorMailsent(Base):
    __tablename__ = 'arXiv_monitor_mailsent'

    t = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    sent = Column(INTEGER)


class NextMail(Base):
    __tablename__ = 'arXiv_next_mail'
    __table_args__ = (
        Index('arXiv_next_mail_idx_document_id', 'document_id'),
        Index('arXiv_next_mail_idx_document_id_version', 'document_id', 'version')
    )

    next_mail_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, nullable=False)
    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    version = Column(Integer, nullable=False, server_default=text("'1'"))
    type = Column(String(255), nullable=False, server_default=text("'new'"))
    is_written = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    paper_id = Column(String(20))
    extra = Column(String(255))
    mail_id = Column(CHAR(6))


class OrcidConfig(Base):
    __tablename__ = 'arXiv_orcid_config'

    domain = Column(String(75), primary_key=True, nullable=False)
    keyname = Column(String(60), primary_key=True, nullable=False)
    value = Column(String(150))


t_arXiv_ownership_requests_papers = Table(
    'arXiv_ownership_requests_papers', metadata,
    Column('request_id', INTEGER, nullable=False, server_default=text("'0'")),
    Column('document_id', INTEGER, nullable=False, server_default=text("'0'")),
    Index('document_id', 'document_id'),
    Index('request_id', 'request_id', 'document_id', unique=True)
)


class PaperSessions(Base):
    __tablename__ = 'arXiv_paper_sessions'

    paper_session_id = Column(INTEGER, primary_key=True)
    paper_id = Column(String(16), nullable=False, server_default=text("''"))
    start_time = Column(INTEGER, nullable=False, server_default=text("'0'"))
    end_time = Column(INTEGER, nullable=False, server_default=text("'0'"))
    ip_name = Column(String(16), nullable=False, server_default=text("''"))


class PublishLog(Base):
    __tablename__ = 'arXiv_publish_log'

    date = Column(INTEGER, primary_key=True, server_default=text("'0'"))


t_arXiv_refresh_list = Table(
    'arXiv_refresh_list', metadata,
    Column('filename', String(255)),
    Column('mtime', INTEGER),
    Index('arXiv_refresh_list_mtime', 'mtime')
)


class RejectSessionUsernames(Base):
    __tablename__ = 'arXiv_reject_session_usernames'

    username = Column(String(64), primary_key=True, server_default=text("''"))


class SciencewisePings(Base):
    __tablename__ = 'arXiv_sciencewise_pings'

    paper_id_v = Column(String(32), primary_key=True)
    updated = Column(DateTime)


class State(Base):
    __tablename__ = 'arXiv_state'

    id = Column(Integer, primary_key=True)
    name = Column(String(24))
    value = Column(String(24))


t_arXiv_stats_hourly = Table(
    'arXiv_stats_hourly', metadata,
    Column('ymd', Date, nullable=False),
    Column('hour', TINYINT, nullable=False),
    Column('node_num', TINYINT, nullable=False),
    Column('access_type', CHAR(1), nullable=False),
    Column('connections', INTEGER, nullable=False),
    Index('arXiv_stats_hourly_idx_access_type', 'access_type'),
    Index('arXiv_stats_hourly_idx_hour', 'hour'),
    Index('arXiv_stats_hourly_idx_node_num', 'node_num'),
    Index('arXiv_stats_hourly_idx_ymd', 'ymd')
)


class StatsMonthlyDownloads(Base):
    __tablename__ = 'arXiv_stats_monthly_downloads'

    ym = Column(Date, primary_key=True)
    downloads = Column(INTEGER, nullable=False)


class StatsMonthlySubmissions(Base):
    __tablename__ = 'arXiv_stats_monthly_submissions'

    ym = Column(Date, primary_key=True, server_default=text("'0000-00-00'"))
    num_submissions = Column(SMALLINT, nullable=False)
    historical_delta = Column(TINYINT, nullable=False, server_default=text("'0'"))


class SubmissionAgreements(Base):
    __tablename__ = 'arXiv_submission_agreements'

    agreement_id = Column(SMALLINT, primary_key=True)
    commit_ref = Column(String(255), nullable=False)
    effective_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    content = Column(Text)

    arXiv_submissions = relationship('Submissions', back_populates='agreement')


class SubmitterFlags(Base):
    __tablename__ = 'arXiv_submitter_flags'

    flag_id = Column(Integer, primary_key=True)
    comment = Column(String(255))
    pattern = Column(String(255))


class SuspectEmails(Base):
    __tablename__ = 'arXiv_suspect_emails'

    id = Column(Integer, primary_key=True)
    type = Column(String(10), nullable=False)
    pattern = Column(Text, nullable=False)
    comment = Column(Text, nullable=False)
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class Titles(Base):
    __tablename__ = 'arXiv_titles'
    __table_args__ = (
        Index('arXiv_repno_idx', 'report_num'),
        Index('arXiv_titles_idx', 'title')
    )

    paper_id = Column(String(64), primary_key=True)
    title = Column(String(255))
    report_num = Column(String(255))
    date = Column(Date)


class TrackbackPings(Base):
    __tablename__ = 'arXiv_trackback_pings'
    __table_args__ = (
        Index('arXiv_trackback_pings__document_id', 'document_id'),
        Index('arXiv_trackback_pings__posted_date', 'posted_date'),
        Index('arXiv_trackback_pings__status', 'status'),
        Index('arXiv_trackback_pings__url', 'url')
    )

    trackback_id = Column(MEDIUMINT, primary_key=True)
    title = Column(String(255), nullable=False, server_default=text("''"))
    excerpt = Column(String(255), nullable=False, server_default=text("''"))
    url = Column(String(255), nullable=False, server_default=text("''"))
    blog_name = Column(String(255), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    remote_addr = Column(String(16), nullable=False, server_default=text("''"))
    posted_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    is_stale = Column(TINYINT, nullable=False, server_default=text("'0'"))
    approved_by_user = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    approved_time = Column(Integer, nullable=False, server_default=text("'0'"))
    status = Column(Enum('pending', 'pending2', 'accepted', 'rejected', 'spam'), nullable=False, server_default=text("'pending'"))
    document_id = Column(MEDIUMINT)
    site_id = Column(INTEGER)


class TrackbackSites(Base):
    __tablename__ = 'arXiv_trackback_sites'
    __table_args__ = (
        Index('arXiv_trackback_sites__pattern', 'pattern'),
    )

    pattern = Column(String(255), nullable=False, server_default=text("''"))
    site_id = Column(INTEGER, primary_key=True)
    action = Column(Enum('neutral', 'accept', 'reject', 'spam'), nullable=False, server_default=text("'neutral'"))


class Tracking(Base):
    __tablename__ = 'arXiv_tracking'
    __table_args__ = (
        Index('sword_id', 'sword_id', unique=True),
    )

    tracking_id = Column(Integer, primary_key=True)
    sword_id = Column(INTEGER(8), nullable=False, server_default=text("'00000000'"))
    paper_id = Column(String(32), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    submission_errors = Column(Text)

    arXiv_submissions = relationship('Submissions', back_populates='sword')


t_arXiv_updates = Table(
    'arXiv_updates', metadata,
    Column('document_id', Integer),
    Column('version', Integer, nullable=False, server_default=text("'1'")),
    Column('date', Date),
    Column('action', Enum('new', 'replace', 'absonly', 'cross', 'repcro')),
    Column('archive', String(20)),
    Column('category', String(20)),
    Index('archive_index', 'archive'),
    Index('category_index', 'category'),
    Index('date_index', 'date'),
    Index('document_id', 'document_id', 'date', 'action', 'category', unique=True),
    Index('document_id_index', 'document_id')
)


t_arXiv_updates_tmp = Table(
    'arXiv_updates_tmp', metadata,
    Column('document_id', Integer),
    Column('date', Date),
    Column('action', Enum('new', 'replace', 'absonly', 'cross', 'repcro')),
    Column('category', String(20)),
    Index('document_id', 'document_id', 'date', 'action', 'category', unique=True)
)


t_arXiv_white_email = Table(
    'arXiv_white_email', metadata,
    Column('pattern', String(64)),
    Index('uc_pattern', 'pattern', unique=True)
)


t_arXiv_xml_notifications = Table(
    'arXiv_xml_notifications', metadata,
    Column('control_id', INTEGER),
    Column('type', Enum('submission', 'cross', 'jref')),
    Column('queued_date', INTEGER, nullable=False, server_default=text("'0'")),
    Column('sent_date', INTEGER, nullable=False, server_default=text("'0'")),
    Column('status', Enum('unsent', 'sent', 'failed')),
    Index('control_id', 'control_id'),
    Index('status', 'status')
)


class DbixClassSchemaVersions(Base):
    __tablename__ = 'dbix_class_schema_versions'

    version = Column(String(10), primary_key=True)
    installed = Column(String(20), nullable=False)


t_demographics_backup = Table(
    'demographics_backup', metadata,
    Column('user_id', INTEGER, nullable=False, server_default=text("'0'")),
    Column('country', CHAR(2), nullable=False, server_default=text("''")),
    Column('affiliation', String(255), nullable=False, server_default=text("''")),
    Column('url', String(255), nullable=False, server_default=text("''")),
    Column('type', SMALLINT),
    Column('os', SMALLINT),
    Column('archive', String(16)),
    Column('subject_class', String(16)),
    Column('original_subject_classes', String(255), nullable=False, server_default=text("''")),
    Column('flag_group_physics', INTEGER),
    Column('flag_group_math', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_group_cs', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_group_nlin', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_proxy', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_journal', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_xml', INTEGER, nullable=False, server_default=text("'0'")),
    Column('dirty', INTEGER, nullable=False, server_default=text("'2'")),
    Column('flag_group_test', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_suspect', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_group_q_bio', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_no_upload', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_no_endorse', INTEGER, nullable=False, server_default=text("'0'")),
    Column('veto_status', Enum('ok', 'no-endorse', 'no-upload'), server_default=text("'ok'"))
)


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(CHAR(72), primary_key=True)
    session_data = Column(Text)
    expires = Column(Integer)


class TapirCountries(Base):
    __tablename__ = 'tapir_countries'

    digraph = Column(CHAR(2), primary_key=True, server_default=text("''"))
    country_name = Column(String(255), nullable=False, server_default=text("''"))
    rank = Column(INTEGER, nullable=False, server_default=text("'255'"))

    tapir_address = relationship('TapirAddress', back_populates='tapir_countries')
    tapir_demographics = relationship('TapirDemographics', back_populates='tapir_countries')


class TapirEmailLog(Base):
    __tablename__ = 'tapir_email_log'
    __table_args__ = (
        Index('mailing_id', 'mailing_id'),
    )

    mail_id = Column(INTEGER, primary_key=True)
    sent_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    template_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    reference_type = Column(CHAR(1))
    reference_id = Column(INTEGER)
    email = Column(String(255))
    flag_bounced = Column(INTEGER)
    mailing_id = Column(INTEGER)


t_tapir_error_log = Table(
    'tapir_error_log', metadata,
    Column('error_date', INTEGER, nullable=False, server_default=text("'0'")),
    Column('user_id', INTEGER),
    Column('session_id', INTEGER),
    Column('ip_addr', String(16), nullable=False, server_default=text("''")),
    Column('remote_host', String(255), nullable=False, server_default=text("''")),
    Column('tracking_cookie', String(32), nullable=False, server_default=text("''")),
    Column('message', String(32), nullable=False, server_default=text("''")),
    Column('url', String(255), nullable=False, server_default=text("''")),
    Column('error_url', String(255), nullable=False, server_default=text("''")),
    Index('error_date', 'error_date'),
    Index('ip_addr', 'ip_addr'),
    Index('message', 'message'),
    Index('session_id', 'session_id'),
    Index('tracking_cookie', 'tracking_cookie'),
    Index('user_id', 'user_id')
)


class TapirIntegerVariables(Base):
    __tablename__ = 'tapir_integer_variables'

    variable_id = Column(String(32), primary_key=True, server_default=text("''"))
    value = Column(INTEGER, nullable=False, server_default=text("'0'"))


class TapirNicknamesAudit(Base):
    __tablename__ = 'tapir_nicknames_audit'
    __table_args__ = (
        Index('creation_date', 'creation_date'),
        Index('creation_ip_num', 'creation_ip_num'),
        Index('tracking_cookie', 'tracking_cookie')
    )

    nick_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    creation_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    creation_ip_num = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))


t_tapir_no_cookies = Table(
    'tapir_no_cookies', metadata,
    Column('log_date', INTEGER, nullable=False, server_default=text("'0'")),
    Column('ip_addr', String(16), nullable=False, server_default=text("''")),
    Column('remote_host', String(255), nullable=False, server_default=text("''")),
    Column('tracking_cookie', String(255), nullable=False, server_default=text("''")),
    Column('session_data', String(255), nullable=False, server_default=text("''")),
    Column('user_agent', String(255), nullable=False, server_default=text("''"))
)


t_tapir_periodic_tasks_log = Table(
    'tapir_periodic_tasks_log', metadata,
    Column('t', INTEGER, nullable=False, server_default=text("'0'")),
    Column('entry', Text),
    Index('tapir_periodic_tasks_log_1', 't')
)


class TapirPolicyClasses(Base):
    __tablename__ = 'tapir_policy_classes'

    class_id = Column(SMALLINT, primary_key=True)
    name = Column(String(64), nullable=False, server_default=text("''"))
    description = Column(Text, nullable=False)
    password_storage = Column(INTEGER, nullable=False, server_default=text("'0'"))
    recovery_policy = Column(INTEGER, nullable=False, server_default=text("'0'"))
    permanent_login = Column(Integer, nullable=False, server_default=text("'0'"))

    tapir_users = relationship('TapirUsers', back_populates='tapir_policy_classes')


class TapirPresessions(Base):
    __tablename__ = 'tapir_presessions'

    presession_id = Column(INTEGER, primary_key=True)
    ip_num = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    created_at = Column(INTEGER, nullable=False, server_default=text("'0'"))


class TapirStringVariables(Base):
    __tablename__ = 'tapir_string_variables'

    variable_id = Column(String(32), primary_key=True, server_default=text("''"))
    value = Column(Text, nullable=False)


class TapirStrings(Base):
    __tablename__ = 'tapir_strings'

    name = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    module = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    language = Column(String(32), primary_key=True, nullable=False, server_default=text("'en'"))
    string = Column(Text, nullable=False)


class SubscriptionUniversalInstitutionContact(Base):
    __tablename__ = 'Subscription_UniversalInstitutionContact'
    __table_args__ = (
        ForeignKeyConstraint(['sid'], ['Subscription_UniversalInstitution.id'], ondelete='CASCADE', name='Subscription_Institution_Contact_Universal'),
        Index('sid', 'sid')
    )

    sid = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    active = Column(TINYINT, server_default=text("'0'"))
    contact_name = Column(String(255))
    phone = Column(String(255))
    note = Column(String(2048))

    Subscription_UniversalInstitution = relationship('SubscriptionUniversalInstitution', back_populates='Subscription_UniversalInstitutionContact')


class SubscriptionUniversalInstitutionIP(Base):
    __tablename__ = 'Subscription_UniversalInstitutionIP'
    __table_args__ = (
        ForeignKeyConstraint(['sid'], ['Subscription_UniversalInstitution.id'], ondelete='CASCADE', name='Subscription_Institution_IP_Universal'),
        Index('end', 'end'),
        Index('ip', 'start', 'end'),
        Index('sid', 'sid'),
        Index('start', 'start')
    )

    sid = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    end = Column(BigInteger, nullable=False)
    start = Column(BigInteger, nullable=False)
    exclude = Column(TINYINT, server_default=text("'0'"))

    Subscription_UniversalInstitution = relationship('SubscriptionUniversalInstitution', back_populates='Subscription_UniversalInstitutionIP')


class Archives(Base):
    __tablename__ = 'arXiv_archives'
    __table_args__ = (
        ForeignKeyConstraint(['in_group'], ['arXiv_groups.group_id'], name='0_576'),
        Index('in_group', 'in_group')
    )

    archive_id = Column(String(16), primary_key=True, server_default=text("''"))
    in_group = Column(String(16), nullable=False, server_default=text("''"))
    archive_name = Column(String(255), nullable=False, server_default=text("''"))
    start_date = Column(String(4), nullable=False, server_default=text("''"))
    end_date = Column(String(4), nullable=False, server_default=text("''"))
    subdivided = Column(INTEGER, nullable=False, server_default=text("'0'"))

    arXiv_groups = relationship('Groups', back_populates='arXiv_archives')
    arXiv_categories = relationship('Categories', back_populates='arXiv_archives')


t_tapir_save_post_variables = Table(
    'tapir_save_post_variables', metadata,
    Column('presession_id', INTEGER, nullable=False, server_default=text("'0'")),
    Column('name', String(255)),
    Column('value', MEDIUMTEXT, nullable=False),
    Column('seq', INTEGER, nullable=False, server_default=text("'0'")),
    ForeignKeyConstraint(['presession_id'], ['tapir_presessions.presession_id'], name='0_558'),
    Index('presession_id', 'presession_id')
)


class TapirUsers(Base):
    __tablename__ = 'tapir_users'
    __table_args__ = (
        ForeignKeyConstraint(['policy_class'], ['tapir_policy_classes.class_id'], name='0_510'),
        Index('email', 'email', unique=True),
        Index('first_name', 'first_name'),
        Index('flag_approved', 'flag_approved'),
        Index('flag_banned', 'flag_banned'),
        Index('flag_can_lock', 'flag_can_lock'),
        Index('flag_deleted', 'flag_deleted'),
        Index('flag_edit_users', 'flag_edit_users'),
        Index('flag_internal', 'flag_internal'),
        Index('joined_date', 'joined_date'),
        Index('joined_ip_num', 'joined_ip_num'),
        Index('last_name', 'last_name'),
        Index('policy_class', 'policy_class'),
        Index('tracking_cookie', 'tracking_cookie')
    )

    user_id = Column(INTEGER, primary_key=True)
    share_first_name = Column(INTEGER, nullable=False, server_default=text("'1'"))
    share_last_name = Column(INTEGER, nullable=False, server_default=text("'1'"))
    email = Column(String(255), nullable=False, server_default=text("''"))
    share_email = Column(INTEGER, nullable=False, server_default=text("'8'"))
    email_bouncing = Column(INTEGER, nullable=False, server_default=text("'0'"))
    policy_class = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    joined_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    joined_remote_host = Column(String(255), nullable=False, server_default=text("''"))
    flag_internal = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_edit_users = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_edit_system = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_email_verified = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_approved = Column(INTEGER, nullable=False, server_default=text("'1'"))
    flag_deleted = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_banned = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_wants_email = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_html_email = Column(INTEGER, nullable=False, server_default=text("'0'"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    flag_allow_tex_produced = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_can_lock = Column(INTEGER, nullable=False, server_default=text("'0'"))
    first_name = Column(String(50))
    last_name = Column(String(50))
    suffix_name = Column(String(50))
    joined_ip_num = Column(String(16))

    tapir_policy_classes = relationship('TapirPolicyClasses', back_populates='tapir_users')
    arXiv_control_holds = relationship('ControlHolds', foreign_keys='[ControlHolds.last_changed_by]', back_populates='tapir_users')
    arXiv_control_holds_ = relationship('ControlHolds', foreign_keys='[ControlHolds.placed_by]', back_populates='tapir_users_')
    arXiv_documents = relationship('Documents', back_populates='submitter')
    arXiv_moderator_api_key = relationship('ModeratorApiKey', back_populates='user')
    tapir_address = relationship('TapirAddress', back_populates='user')
    tapir_email_change_tokens = relationship('TapirEmailChangeTokens', back_populates='user')
    tapir_email_templates = relationship('TapirEmailTemplates', foreign_keys='[TapirEmailTemplates.created_by]', back_populates='tapir_users')
    tapir_email_templates_ = relationship('TapirEmailTemplates', foreign_keys='[TapirEmailTemplates.updated_by]', back_populates='tapir_users_')
    tapir_email_tokens = relationship('TapirEmailTokens', back_populates='user')
    tapir_nicknames = relationship('TapirNicknames', back_populates='user')
    tapir_phone = relationship('TapirPhone', back_populates='user')
    tapir_recovery_tokens = relationship('TapirRecoveryTokens', back_populates='user')
    tapir_sessions = relationship('TapirSessions', back_populates='user')
    arXiv_cross_control = relationship('CrossControl', back_populates='user')
    arXiv_endorsement_requests = relationship('EndorsementRequests', back_populates='endorsee')
    arXiv_jref_control = relationship('JrefControl', back_populates='user')
    arXiv_metadata = relationship('Metadata', back_populates='submitter')
    arXiv_show_email_requests = relationship('ShowEmailRequests', back_populates='user')
    arXiv_submission_control = relationship('SubmissionControl', back_populates='user')
    arXiv_submissions = relationship('Submissions', back_populates='submitter')
    tapir_admin_audit = relationship('TapirAdminAudit', foreign_keys='[TapirAdminAudit.admin_user]', back_populates='tapir_users')
    tapir_admin_audit_ = relationship('TapirAdminAudit', foreign_keys='[TapirAdminAudit.affected_user]', back_populates='tapir_users_')
    tapir_email_mailings = relationship('TapirEmailMailings', foreign_keys='[TapirEmailMailings.created_by]', back_populates='tapir_users')
    tapir_email_mailings_ = relationship('TapirEmailMailings', foreign_keys='[TapirEmailMailings.sent_by]', back_populates='tapir_users_')
    tapir_permanent_tokens = relationship('TapirPermanentTokens', back_populates='user')
    tapir_recovery_tokens_used = relationship('TapirRecoveryTokensUsed', back_populates='user')
    arXiv_endorsements = relationship('Endorsements', foreign_keys='[Endorsements.endorsee_id]', back_populates='endorsee')
    arXiv_endorsements_ = relationship('Endorsements', foreign_keys='[Endorsements.endorser_id]', back_populates='endorser')
    arXiv_ownership_requests = relationship('OwnershipRequests', back_populates='user')
    arXiv_submission_category_proposal = relationship('SubmissionCategoryProposal', back_populates='user')
    arXiv_submission_flag = relationship('SubmissionFlag', back_populates='user')
    arXiv_submission_hold_reason = relationship('SubmissionHoldReason', back_populates='user')
    arXiv_submission_view_flag = relationship('SubmissionViewFlag', back_populates='user')


class AuthorIds(TapirUsers):
    __tablename__ = 'arXiv_author_ids'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='arXiv_author_ids_ibfk_1'),
        Index('author_id', 'author_id')
    )

    user_id = Column(INTEGER, primary_key=True)
    author_id = Column(String(50), nullable=False)
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))


t_arXiv_bad_pw = Table(
    'arXiv_bad_pw', metadata,
    Column('user_id', INTEGER, nullable=False, server_default=text("'0'")),
    ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_601'),
    Index('user_id', 'user_id')
)


class Categories(Base):
    __tablename__ = 'arXiv_categories'
    __table_args__ = (
        ForeignKeyConstraint(['archive'], ['arXiv_archives.archive_id'], name='0_578'),
        ForeignKeyConstraint(['endorsement_domain'], ['arXiv_endorsement_domains.endorsement_domain'], name='0_753'),
        Index('endorsement_domain', 'endorsement_domain')
    )

    archive = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    subject_class = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    definitive = Column(Integer, nullable=False, server_default=text("'0'"))
    active = Column(Integer, nullable=False, server_default=text("'0'"))
    endorse_all = Column(Enum('y', 'n', 'd'), nullable=False, server_default=text("'d'"))
    endorse_email = Column(Enum('y', 'n', 'd'), nullable=False, server_default=text("'d'"))
    papers_to_endorse = Column(SMALLINT, nullable=False, server_default=text("'0'"))
    category_name = Column(String(255))
    endorsement_domain = Column(String(32))

    arXiv_archives = relationship('Archives', back_populates='arXiv_categories')
    arXiv_endorsement_domains = relationship('EndorsementDomains', back_populates='arXiv_categories')
    arXiv_cross_control = relationship('CrossControl', back_populates='arXiv_categories')
    arXiv_demographics = relationship('Demographics', back_populates='arXiv_categories')
    arXiv_endorsement_requests = relationship('EndorsementRequests', back_populates='arXiv_categories')
    arXiv_endorsements = relationship('Endorsements', back_populates='arXiv_categories')


class ControlHolds(Base):
    __tablename__ = 'arXiv_control_holds'
    __table_args__ = (
        ForeignKeyConstraint(['last_changed_by'], ['tapir_users.user_id'], name='arXiv_control_holds_ibfk_2'),
        ForeignKeyConstraint(['placed_by'], ['tapir_users.user_id'], name='arXiv_control_holds_ibfk_1'),
        Index('control_id', 'control_id', 'hold_type', unique=True),
        Index('hold_reason', 'hold_reason'),
        Index('hold_status', 'hold_status'),
        Index('hold_type', 'hold_type'),
        Index('last_changed_by', 'last_changed_by'),
        Index('origin', 'origin'),
        Index('placed_by', 'placed_by')
    )

    hold_id = Column(INTEGER, primary_key=True)
    control_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    hold_type = Column(Enum('submission', 'cross', 'jref'), nullable=False, server_default=text("'submission'"))
    hold_status = Column(Enum('held', 'extended', 'accepted', 'rejected'), nullable=False, server_default=text("'held'"))
    hold_reason = Column(String(255), nullable=False, server_default=text("''"))
    hold_data = Column(String(255), nullable=False, server_default=text("''"))
    origin = Column(Enum('auto', 'user', 'admin', 'moderator'), nullable=False, server_default=text("'auto'"))
    placed_by = Column(INTEGER)
    last_changed_by = Column(INTEGER)

    tapir_users = relationship('TapirUsers', foreign_keys=[last_changed_by], back_populates='arXiv_control_holds')
    tapir_users_ = relationship('TapirUsers', foreign_keys=[placed_by], back_populates='arXiv_control_holds_')


class Documents(Base):
    __tablename__ = 'arXiv_documents'
    __table_args__ = (
        ForeignKeyConstraint(['submitter_id'], ['tapir_users.user_id'], name='0_580'),
        Index('dated', 'dated'),
        Index('paper_id', 'paper_id', unique=True),
        Index('submitter_email', 'submitter_email'),
        Index('submitter_id', 'submitter_id'),
        Index('title', 'title')
    )

    document_id = Column(MEDIUMINT, primary_key=True)
    paper_id = Column(String(20), nullable=False, server_default=text("''"))
    title = Column(String(255), nullable=False, server_default=text("''"))
    submitter_email = Column(String(64), nullable=False, server_default=text("''"))
    dated = Column(INTEGER, nullable=False, server_default=text("'0'"))
    authors = Column(Text)
    submitter_id = Column(INTEGER)
    primary_subject_class = Column(String(16))
    created = Column(DateTime)

    submitter = relationship('TapirUsers', back_populates='arXiv_documents')
    arXiv_admin_metadata = relationship('AdminMetadata', back_populates='document')
    arXiv_cross_control = relationship('CrossControl', back_populates='document')
    arXiv_dblp_document_authors = relationship('DblpDocumentAuthors', back_populates='document')
    arXiv_document_category = relationship('DocumentCategory', back_populates='document')
    arXiv_jref_control = relationship('JrefControl', back_populates='document')
    arXiv_metadata = relationship('Metadata', back_populates='document')
    arXiv_mirror_list = relationship('MirrorList', back_populates='document')
    arXiv_show_email_requests = relationship('ShowEmailRequests', back_populates='document')
    arXiv_submission_control = relationship('SubmissionControl', back_populates='document')
    arXiv_submissions = relationship('Submissions', back_populates='document')
    arXiv_top_papers = relationship('TopPapers', back_populates='document')
    arXiv_versions = relationship('Versions', back_populates='document')


t_arXiv_duplicates = Table(
    'arXiv_duplicates', metadata,
    Column('user_id', INTEGER, nullable=False, server_default=text("'0'")),
    Column('email', String(255)),
    Column('username', String(255)),
    ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_599'),
    Index('user_id', 'user_id')
)


class ModeratorApiKey(Base):
    __tablename__ = 'arXiv_moderator_api_key'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='arXiv_moderator_api_key_ibfk_1'),
    )

    user_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    valid = Column(Integer, nullable=False, server_default=text("'1'"))
    issued_when = Column(INTEGER, nullable=False, server_default=text("'0'"))
    issued_to = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))

    user = relationship('TapirUsers', back_populates='arXiv_moderator_api_key')


class OrcidIds(TapirUsers):
    __tablename__ = 'arXiv_orcid_ids'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='arXiv_orcid_ids_ibfk_1'),
        Index('orcid', 'orcid')
    )

    user_id = Column(INTEGER, primary_key=True)
    orcid = Column(String(19), nullable=False)
    authenticated = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))


class QueueView(TapirUsers):
    __tablename__ = 'arXiv_queue_view'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], ondelete='CASCADE', name='arXiv_queue_view_ibfk_1'),
    )

    user_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    total_views = Column(INTEGER, nullable=False, server_default=text("'0'"))
    last_view = Column(DateTime)
    second_last_view = Column(DateTime)


class SuspiciousNames(TapirUsers):
    __tablename__ = 'arXiv_suspicious_names'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_606'),
    )

    user_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    full_name = Column(String(255), nullable=False, server_default=text("''"))


class SwordLicenses(TapirUsers):
    __tablename__ = 'arXiv_sword_licenses'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='user_id_fk'),
    )

    user_id = Column(INTEGER, primary_key=True)
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    license = Column(String(127))


class TapirAddress(Base):
    __tablename__ = 'tapir_address'
    __table_args__ = (
        ForeignKeyConstraint(['country'], ['tapir_countries.digraph'], name='0_523'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_522'),
        Index('address_type', 'address_type'),
        Index('city', 'city'),
        Index('country', 'country'),
        Index('postal_code', 'postal_code')
    )

    user_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    address_type = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    company = Column(String(80), nullable=False, server_default=text("''"))
    line1 = Column(String(80), nullable=False, server_default=text("''"))
    line2 = Column(String(80), nullable=False, server_default=text("''"))
    city = Column(String(50), nullable=False, server_default=text("''"))
    state = Column(String(50), nullable=False, server_default=text("''"))
    postal_code = Column(String(16), nullable=False, server_default=text("''"))
    country = Column(CHAR(2), nullable=False, server_default=text("''"))
    share_addr = Column(INTEGER, nullable=False, server_default=text("'0'"))

    tapir_countries = relationship('TapirCountries', back_populates='tapir_address')
    user = relationship('TapirUsers', back_populates='tapir_address')


class TapirDemographics(TapirUsers):
    __tablename__ = 'tapir_demographics'
    __table_args__ = (
        ForeignKeyConstraint(['country'], ['tapir_countries.digraph'], name='0_518'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_517'),
        Index('birthday', 'birthday'),
        Index('country', 'country'),
        Index('postal_code', 'postal_code')
    )

    user_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    gender = Column(Integer, nullable=False, server_default=text("'0'"))
    share_gender = Column(INTEGER, nullable=False, server_default=text("'16'"))
    share_birthday = Column(INTEGER, nullable=False, server_default=text("'16'"))
    country = Column(CHAR(2), nullable=False, server_default=text("''"))
    share_country = Column(INTEGER, nullable=False, server_default=text("'16'"))
    postal_code = Column(String(16), nullable=False, server_default=text("''"))
    birthday = Column(Date)

    tapir_countries = relationship('TapirCountries', back_populates='tapir_demographics')


class TapirEmailChangeTokens(Base):
    __tablename__ = 'tapir_email_change_tokens'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_535'),
        Index('secret', 'secret')
    )

    user_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    tapir_dest = Column(String(255), nullable=False, server_default=text("''"))
    issued_when = Column(INTEGER, nullable=False, server_default=text("'0'"))
    issued_to = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(16), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    used = Column(INTEGER, nullable=False, server_default=text("'0'"))
    session_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    old_email = Column(String(255))
    new_email = Column(String(255))
    consumed_when = Column(INTEGER)
    consumed_from = Column(String(16))

    user = relationship('TapirUsers', back_populates='tapir_email_change_tokens')


class TapirEmailTemplates(Base):
    __tablename__ = 'tapir_email_templates'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['tapir_users.user_id'], name='0_560'),
        ForeignKeyConstraint(['updated_by'], ['tapir_users.user_id'], name='0_561'),
        Index('created_by', 'created_by'),
        Index('short_name', 'short_name', 'lang', unique=True),
        Index('update_date', 'update_date'),
        Index('updated_by', 'updated_by')
    )

    template_id = Column(INTEGER, primary_key=True)
    short_name = Column(String(32), nullable=False, server_default=text("''"))
    lang = Column(CHAR(2), nullable=False, server_default=text("'en'"))
    long_name = Column(String(255), nullable=False, server_default=text("''"))
    data = Column(Text, nullable=False)
    sql_statement = Column(Text, nullable=False)
    update_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    created_by = Column(INTEGER, nullable=False, server_default=text("'0'"))
    updated_by = Column(INTEGER, nullable=False, server_default=text("'0'"))
    workflow_status = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_system = Column(INTEGER, nullable=False, server_default=text("'0'"))

    tapir_users = relationship('TapirUsers', foreign_keys=[created_by], back_populates='tapir_email_templates')
    tapir_users_ = relationship('TapirUsers', foreign_keys=[updated_by], back_populates='tapir_email_templates_')
    tapir_email_headers = relationship('TapirEmailHeaders', back_populates='template')
    tapir_email_mailings = relationship('TapirEmailMailings', back_populates='template')


class TapirEmailTokens(Base):
    __tablename__ = 'tapir_email_tokens'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_530'),
        Index('secret', 'secret')
    )

    user_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    tapir_dest = Column(String(255), nullable=False, server_default=text("''"))
    issued_when = Column(INTEGER, nullable=False, server_default=text("'0'"))
    issued_to = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    wants_perm_token = Column(Integer, nullable=False, server_default=text("'0'"))

    user = relationship('TapirUsers', back_populates='tapir_email_tokens')


class TapirNicknames(Base):
    __tablename__ = 'tapir_nicknames'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_570'),
        Index('flag_valid', 'flag_valid'),
        Index('nickname', 'nickname', unique=True),
        Index('policy', 'policy'),
        Index('role', 'role'),
        Index('user_id', 'user_id', 'user_seq', unique=True)
    )

    nick_id = Column(INTEGER, primary_key=True)
    nickname = Column(String(20), nullable=False, server_default=text("''"))
    user_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    user_seq = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_valid = Column(INTEGER, nullable=False, server_default=text("'0'"))
    role = Column(INTEGER, nullable=False, server_default=text("'0'"))
    policy = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_primary = Column(INTEGER, nullable=False, server_default=text("'0'"))

    user = relationship('TapirUsers', back_populates='tapir_nicknames')


class TapirPhone(Base):
    __tablename__ = 'tapir_phone'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_520'),
        Index('phone_number', 'phone_number'),
        Index('phone_type', 'phone_type')
    )

    user_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    phone_type = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    share_phone = Column(INTEGER, nullable=False, server_default=text("'16'"))
    phone_number = Column(String(32))

    user = relationship('TapirUsers', back_populates='tapir_phone')


class TapirRecoveryTokens(Base):
    __tablename__ = 'tapir_recovery_tokens'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_546'),
        Index('secret', 'secret')
    )

    user_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    valid = Column(Integer, nullable=False, server_default=text("'1'"))
    tapir_dest = Column(String(255), nullable=False, server_default=text("''"))
    issued_when = Column(INTEGER, nullable=False, server_default=text("'0'"))
    issued_to = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))

    user = relationship('TapirUsers', back_populates='tapir_recovery_tokens')


class TapirSessions(Base):
    __tablename__ = 'tapir_sessions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_525'),
        Index('end_time', 'end_time'),
        Index('start_time', 'start_time'),
        Index('user_id', 'user_id')
    )

    session_id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    last_reissue = Column(Integer, nullable=False, server_default=text("'0'"))
    start_time = Column(Integer, nullable=False, server_default=text("'0'"))
    end_time = Column(Integer, nullable=False, server_default=text("'0'"))

    user = relationship('TapirUsers', back_populates='tapir_sessions')
    tapir_admin_audit = relationship('TapirAdminAudit', back_populates='session')
    tapir_permanent_tokens = relationship('TapirPermanentTokens', back_populates='session')
    tapir_recovery_tokens_used = relationship('TapirRecoveryTokensUsed', back_populates='session')


class TapirUsersHot(TapirUsers):
    __tablename__ = 'tapir_users_hot'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_514'),
        Index('last_login', 'last_login'),
        Index('number_sessions', 'number_sessions'),
        Index('second_last_login', 'second_last_login')
    )

    user_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    last_login = Column(INTEGER, nullable=False, server_default=text("'0'"))
    second_last_login = Column(INTEGER, nullable=False, server_default=text("'0'"))
    number_sessions = Column(Integer, nullable=False, server_default=text("'0'"))


class TapirUsersPassword(TapirUsers):
    __tablename__ = 'tapir_users_password'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_512'),
    )

    user_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    password_storage = Column(INTEGER, nullable=False, server_default=text("'0'"))
    password_enc = Column(String(50), nullable=False, server_default=text("''"))


class AdminMetadata(Base):
    __tablename__ = 'arXiv_admin_metadata'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], ondelete='CASCADE', name='meta_doc_fk'),
        Index('document_id', 'document_id'),
        Index('id', 'metadata_id'),
        Index('pidv', 'paper_id', 'version', unique=True)
    )

    metadata_id = Column(Integer, primary_key=True)
    version = Column(Integer, nullable=False, server_default=text("'1'"))
    document_id = Column(MEDIUMINT)
    paper_id = Column(String(64))
    created = Column(DateTime)
    updated = Column(DateTime)
    submitter_name = Column(String(64))
    submitter_email = Column(String(64))
    history = Column(Text)
    source_size = Column(Integer)
    source_type = Column(String(12))
    title = Column(Text)
    authors = Column(Text)
    category_string = Column(String(255))
    comments = Column(Text)
    proxy = Column(String(255))
    report_num = Column(Text)
    msc_class = Column(String(255))
    acm_class = Column(String(255))
    journal_ref = Column(Text)
    doi = Column(String(255))
    abstract = Column(Text)
    license = Column(String(255))
    modtime = Column(Integer)
    is_current = Column(TINYINT(1), server_default=text("'0'"))

    document = relationship('Documents', back_populates='arXiv_admin_metadata')


t_arXiv_bogus_subject_class = Table(
    'arXiv_bogus_subject_class', metadata,
    Column('document_id', MEDIUMINT, nullable=False, server_default=text("'0'")),
    Column('category_name', String(255), nullable=False, server_default=text("''")),
    ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='0_604'),
    Index('document_id', 'document_id')
)


class CrossControl(Base):
    __tablename__ = 'arXiv_cross_control'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class'], name='arXiv_cross_control_ibfk_2'),
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_cross_control_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='arXiv_cross_control_ibfk_3'),
        Index('archive', 'archive', 'subject_class'),
        Index('document_id', 'document_id', 'version'),
        Index('freeze_date', 'freeze_date'),
        Index('status', 'status'),
        Index('user_id', 'user_id')
    )

    control_id = Column(INTEGER, primary_key=True)
    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    version = Column(TINYINT, nullable=False, server_default=text("'0'"))
    desired_order = Column(TINYINT, nullable=False, server_default=text("'0'"))
    user_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    status = Column(Enum('new', 'frozen', 'published', 'rejected'), nullable=False, server_default=text("'new'"))
    archive = Column(String(16), nullable=False, server_default=text("''"))
    subject_class = Column(String(16), nullable=False, server_default=text("''"))
    request_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    freeze_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    publish_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_must_notify = Column(Enum('0', '1'), server_default=text("'1'"))

    arXiv_categories = relationship('Categories', back_populates='arXiv_cross_control')
    document = relationship('Documents', back_populates='arXiv_cross_control')
    user = relationship('TapirUsers', back_populates='arXiv_cross_control')


class Dblp(Documents):
    __tablename__ = 'arXiv_dblp'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_DBLP_cdfk1'),
    )

    document_id = Column(MEDIUMINT, primary_key=True, server_default=text("'0'"))
    url = Column(String(80))


class DblpDocumentAuthors(Base):
    __tablename__ = 'arXiv_dblp_document_authors'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['arXiv_dblp_authors.author_id'], name='arXiv_DBLP_ibfk2'),
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_DBLP_abfk1'),
        Index('author_id', 'author_id'),
        Index('document_id', 'document_id')
    )

    document_id = Column(MEDIUMINT, primary_key=True, nullable=False)
    author_id = Column(MEDIUMINT, primary_key=True, nullable=False, server_default=text("'0'"))
    position = Column(TINYINT, nullable=False, server_default=text("'0'"))

    author = relationship('DblpAuthors', back_populates='arXiv_dblp_document_authors')
    document = relationship('Documents', back_populates='arXiv_dblp_document_authors')


class Demographics(TapirUsers):
    __tablename__ = 'arXiv_demographics'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class'], name='0_588'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_587'),
        Index('archive', 'archive', 'subject_class'),
        Index('country', 'country'),
        Index('flag_group_cs', 'flag_group_cs'),
        Index('flag_group_econ', 'flag_group_econ'),
        Index('flag_group_eess', 'flag_group_eess'),
        Index('flag_group_math', 'flag_group_math'),
        Index('flag_group_nlin', 'flag_group_nlin'),
        Index('flag_group_physics', 'flag_group_physics'),
        Index('flag_group_q_bio', 'flag_group_q_bio'),
        Index('flag_group_q_fin', 'flag_group_q_fin'),
        Index('flag_group_stat', 'flag_group_stat'),
        Index('flag_journal', 'flag_journal'),
        Index('flag_proxy', 'flag_proxy'),
        Index('flag_suspect', 'flag_suspect'),
        Index('flag_xml', 'flag_xml'),
        Index('type', 'type')
    )

    user_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    country = Column(CHAR(2), nullable=False, server_default=text("''"))
    affiliation = Column(String(255), nullable=False, server_default=text("''"))
    url = Column(String(255), nullable=False, server_default=text("''"))
    original_subject_classes = Column(String(255), nullable=False, server_default=text("''"))
    flag_group_math = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_group_cs = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_group_nlin = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_proxy = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_journal = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_xml = Column(INTEGER, nullable=False, server_default=text("'0'"))
    dirty = Column(INTEGER, nullable=False, server_default=text("'2'"))
    flag_group_test = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_suspect = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_group_q_bio = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_group_q_fin = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_group_stat = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_group_eess = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_group_econ = Column(INTEGER, nullable=False, server_default=text("'0'"))
    veto_status = Column(Enum('ok', 'no-endorse', 'no-upload', 'no-replace'), nullable=False, server_default=text("'ok'"))
    type = Column(SMALLINT)
    archive = Column(String(16))
    subject_class = Column(String(16))
    flag_group_physics = Column(INTEGER)

    arXiv_categories = relationship('Categories', back_populates='arXiv_demographics')


class DocumentCategory(Base):
    __tablename__ = 'arXiv_document_category'
    __table_args__ = (
        ForeignKeyConstraint(['category'], ['arXiv_category_def.category'], name='doc_cat_cat'),
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], ondelete='CASCADE', name='doc_cat_doc'),
        Index('category', 'category'),
        Index('document_id', 'document_id')
    )

    document_id = Column(MEDIUMINT, primary_key=True, nullable=False, server_default=text("'0'"))
    category = Column(String(32), primary_key=True, nullable=False)
    is_primary = Column(TINYINT(1), nullable=False, server_default=text("'0'"))

    arXiv_category_def = relationship('CategoryDef', back_populates='arXiv_document_category')
    document = relationship('Documents', back_populates='arXiv_document_category')


class EndorsementRequests(Base):
    __tablename__ = 'arXiv_endorsement_requests'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class'], name='0_723'),
        ForeignKeyConstraint(['endorsee_id'], ['tapir_users.user_id'], name='0_722'),
        Index('archive', 'archive', 'subject_class'),
        Index('endorsee_id', 'endorsee_id'),
        Index('endorsee_id_2', 'endorsee_id', 'archive', 'subject_class', unique=True),
        Index('secret', 'secret', unique=True)
    )

    request_id = Column(INTEGER, primary_key=True)
    endorsee_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    archive = Column(String(16), nullable=False, server_default=text("''"))
    subject_class = Column(String(16), nullable=False, server_default=text("''"))
    secret = Column(String(16), nullable=False, server_default=text("''"))
    flag_valid = Column(INTEGER, nullable=False, server_default=text("'0'"))
    issued_when = Column(INTEGER, nullable=False, server_default=text("'0'"))
    point_value = Column(INTEGER, nullable=False, server_default=text("'0'"))

    arXiv_categories = relationship('Categories', back_populates='arXiv_endorsement_requests')
    endorsee = relationship('TapirUsers', back_populates='arXiv_endorsement_requests')
    arXiv_endorsements = relationship('Endorsements', back_populates='request')
    arXiv_ownership_requests = relationship('OwnershipRequests', back_populates='endorsement_request')


t_arXiv_in_category = Table(
    'arXiv_in_category', metadata,
    Column('document_id', MEDIUMINT, nullable=False, server_default=text("'0'")),
    Column('archive', String(16), nullable=False, server_default=text("''")),
    Column('subject_class', String(16), nullable=False, server_default=text("''")),
    Column('is_primary', TINYINT(1), nullable=False, server_default=text("'0'")),
    ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class'], name='0_583'),
    ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='0_582'),
    Index('arXiv_in_category_mp', 'archive', 'subject_class'),
    Index('archive', 'archive', 'subject_class', 'document_id', unique=True),
    Index('document_id', 'document_id')
)


class JrefControl(Base):
    __tablename__ = 'arXiv_jref_control'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_jref_control_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='arXiv_jref_control_ibfk_2'),
        Index('document_id', 'document_id', 'version', unique=True),
        Index('freeze_date', 'freeze_date'),
        Index('status', 'status'),
        Index('user_id', 'user_id')
    )

    control_id = Column(INTEGER, primary_key=True)
    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    version = Column(TINYINT, nullable=False, server_default=text("'0'"))
    user_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    status = Column(Enum('new', 'frozen', 'published', 'rejected'), nullable=False, server_default=text("'new'"))
    jref = Column(String(255), nullable=False, server_default=text("''"))
    request_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    freeze_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    publish_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_must_notify = Column(Enum('0', '1'), server_default=text("'1'"))

    document = relationship('Documents', back_populates='arXiv_jref_control')
    user = relationship('TapirUsers', back_populates='arXiv_jref_control')


class Metadata(Base):
    __tablename__ = 'arXiv_metadata'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], ondelete='CASCADE', onupdate='CASCADE', name='arXiv_metadata_fk_document_id'),
        ForeignKeyConstraint(['license'], ['arXiv_licenses.name'], name='arXiv_metadata_fk_license'),
        ForeignKeyConstraint(['submitter_id'], ['tapir_users.user_id'], name='arXiv_metadata_fk_submitter_id'),
        Index('arXiv_metadata_idx_document_id', 'document_id'),
        Index('arXiv_metadata_idx_license', 'license'),
        Index('arXiv_metadata_idx_submitter_id', 'submitter_id'),
        Index('pidv', 'paper_id', 'version', unique=True)
    )

    metadata_id = Column(Integer, primary_key=True)
    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    paper_id = Column(String(64), nullable=False)
    submitter_name = Column(String(64), nullable=False)
    submitter_email = Column(String(64), nullable=False)
    version = Column(Integer, nullable=False, server_default=text("'1'"))
    is_withdrawn = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created = Column(DateTime)
    updated = Column(DateTime)
    submitter_id = Column(INTEGER)
    source_size = Column(Integer)
    source_format = Column(String(12))
    source_flags = Column(String(12))
    title = Column(Text)
    authors = Column(Text)
    abs_categories = Column(String(255))
    comments = Column(Text)
    proxy = Column(String(255))
    report_num = Column(Text)
    msc_class = Column(String(255))
    acm_class = Column(String(255))
    journal_ref = Column(Text)
    doi = Column(String(255))
    abstract = Column(Text)
    license = Column(String(255))
    modtime = Column(Integer)
    is_current = Column(TINYINT(1), server_default=text("'1'"))

    document = relationship('Documents', back_populates='arXiv_metadata')
    arXiv_licenses = relationship('Licenses', back_populates='arXiv_metadata')
    submitter = relationship('TapirUsers', back_populates='arXiv_metadata')
    arXiv_datacite_dois = relationship('DataciteDois', back_populates='metadata_')


class MirrorList(Base):
    __tablename__ = 'arXiv_mirror_list'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_mirror_list_fk_document_id'),
        Index('arXiv_mirror_list_idx_document_id', 'document_id')
    )

    mirror_list_id = Column(Integer, primary_key=True)
    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    version = Column(Integer, nullable=False, server_default=text("'1'"))
    write_source = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    write_abs = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    is_written = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created = Column(DateTime)
    updated = Column(DateTime)

    document = relationship('Documents', back_populates='arXiv_mirror_list')


t_arXiv_moderators = Table(
    'arXiv_moderators', metadata,
    Column('user_id', INTEGER, nullable=False, server_default=text("'0'")),
    Column('archive', String(16), nullable=False, server_default=text("''")),
    Column('subject_class', String(16), nullable=False, server_default=text("''")),
    Column('is_public', TINYINT, nullable=False, server_default=text("'0'")),
    Column('no_email', TINYINT(1), server_default=text("'0'")),
    Column('no_web_email', TINYINT(1), server_default=text("'0'")),
    Column('no_reply_to', TINYINT(1), server_default=text("'0'")),
    Column('daily_update', TINYINT(1), server_default=text("'0'")),
    ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class'], name='0_591'),
    ForeignKeyConstraint(['archive'], ['arXiv_archive_group.archive_id'], name='fk_archive_id'),
    ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_590'),
    Index('arXiv_moderators_idx_no_email', 'no_email'),
    Index('arXiv_moderators_idx_no_reply_to', 'no_reply_to'),
    Index('arXiv_moderators_idx_no_web_email', 'no_web_email'),
    Index('user_id', 'archive', 'subject_class', 'user_id', unique=True),
    Index('user_id_2', 'user_id')
)


t_arXiv_paper_owners = Table(
    'arXiv_paper_owners', metadata,
    Column('document_id', MEDIUMINT, nullable=False, server_default=text("'0'")),
    Column('user_id', INTEGER, nullable=False, server_default=text("'0'")),
    Column('date', INTEGER, nullable=False, server_default=text("'0'")),
    Column('added_by', INTEGER, nullable=False, server_default=text("'0'")),
    Column('remote_addr', String(16), nullable=False, server_default=text("''")),
    Column('remote_host', String(255), nullable=False, server_default=text("''")),
    Column('tracking_cookie', String(32), nullable=False, server_default=text("''")),
    Column('valid', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_author', INTEGER, nullable=False, server_default=text("'0'")),
    Column('flag_auto', INTEGER, nullable=False, server_default=text("'1'")),
    ForeignKeyConstraint(['added_by'], ['tapir_users.user_id'], name='0_595'),
    ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='0_593'),
    ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_594'),
    Index('added_by', 'added_by'),
    Index('document_id', 'document_id', 'user_id', unique=True),
    Index('user_id', 'user_id')
)


class PaperPw(Documents):
    __tablename__ = 'arXiv_paper_pw'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='0_585'),
    )

    document_id = Column(MEDIUMINT, primary_key=True, server_default=text("'0'"))
    password_storage = Column(INTEGER)
    password_enc = Column(String(50))


class QuestionableCategories(Categories):
    __tablename__ = 'arXiv_questionable_categories'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class'], name='0_756'),
    )

    archive = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    subject_class = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))


class ShowEmailRequests(Base):
    __tablename__ = 'arXiv_show_email_requests'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_show_email_requests_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='arXiv_show_email_requests_ibfk_2'),
        Index('dated', 'dated'),
        Index('document_id', 'document_id'),
        Index('remote_addr', 'remote_addr'),
        Index('user_id', 'user_id', 'dated')
    )

    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    user_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    session_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    dated = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_allowed = Column(TINYINT, nullable=False, server_default=text("'0'"))
    remote_addr = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    request_id = Column(INTEGER, primary_key=True)

    document = relationship('Documents', back_populates='arXiv_show_email_requests')
    user = relationship('TapirUsers', back_populates='arXiv_show_email_requests')


class SubmissionControl(Base):
    __tablename__ = 'arXiv_submission_control'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_submission_control_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='arXiv_submission_control_ibfk_2'),
        Index('document_id', 'document_id', 'version', unique=True),
        Index('freeze_date', 'freeze_date'),
        Index('pending_paper_id', 'pending_paper_id'),
        Index('request_date', 'request_date'),
        Index('status', 'status'),
        Index('user_id', 'user_id')
    )

    control_id = Column(INTEGER, primary_key=True)
    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    version = Column(TINYINT, nullable=False, server_default=text("'0'"))
    pending_paper_id = Column(String(20), nullable=False, server_default=text("''"))
    user_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    status = Column(Enum('new', 'frozen', 'published', 'rejected'), nullable=False, server_default=text("'new'"))
    request_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    freeze_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    publish_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_must_notify = Column(Enum('0', '1'), server_default=text("'1'"))

    document = relationship('Documents', back_populates='arXiv_submission_control')
    user = relationship('TapirUsers', back_populates='arXiv_submission_control')


class Submissions(Base):
    __tablename__ = 'arXiv_submissions'
    __table_args__ = (
        ForeignKeyConstraint(['agreement_id'], ['arXiv_submission_agreements.agreement_id'], name='agreement_fk'),
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], ondelete='CASCADE', onupdate='CASCADE', name='arXiv_submissions_fk_document_id'),
        ForeignKeyConstraint(['license'], ['arXiv_licenses.name'], onupdate='CASCADE', name='arXiv_submissions_fk_license'),
        ForeignKeyConstraint(['submitter_id'], ['tapir_users.user_id'], ondelete='CASCADE', onupdate='CASCADE', name='arXiv_submissions_fk_submitter_id'),
        ForeignKeyConstraint(['sword_id'], ['arXiv_tracking.sword_id'], name='arXiv_submissions_fk_sword_id'),
        Index('agreement_fk', 'agreement_id'),
        Index('arXiv_submissions_idx_doc_paper_id', 'doc_paper_id'),
        Index('arXiv_submissions_idx_document_id', 'document_id'),
        Index('arXiv_submissions_idx_is_locked', 'is_locked'),
        Index('arXiv_submissions_idx_is_ok', 'is_ok'),
        Index('arXiv_submissions_idx_license', 'license'),
        Index('arXiv_submissions_idx_rt_ticket_id', 'rt_ticket_id'),
        Index('arXiv_submissions_idx_status', 'status'),
        Index('arXiv_submissions_idx_submitter_id', 'submitter_id'),
        Index('arXiv_submissions_idx_sword_id', 'sword_id'),
        Index('arXiv_submissions_idx_type', 'type')
    )

    submission_id = Column(Integer, primary_key=True)
    is_author = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    status = Column(Integer, nullable=False, server_default=text("'0'"))
    is_withdrawn = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    version = Column(Integer, nullable=False, server_default=text("'1'"))
    remote_addr = Column(VARCHAR(16), nullable=False, server_default=text("''"))
    remote_host = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    package = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    is_locked = Column(INTEGER, nullable=False, server_default=text("'0'"))
    document_id = Column(MEDIUMINT)
    doc_paper_id = Column(VARCHAR(20))
    sword_id = Column(INTEGER)
    userinfo = Column(TINYINT, server_default=text("'0'"))
    agree_policy = Column(TINYINT(1), server_default=text("'0'"))
    viewed = Column(TINYINT(1), server_default=text("'0'"))
    stage = Column(Integer, server_default=text("'0'"))
    submitter_id = Column(INTEGER)
    submitter_name = Column(String(64))
    submitter_email = Column(String(64))
    created = Column(DateTime)
    updated = Column(DateTime)
    sticky_status = Column(Integer)
    must_process = Column(TINYINT(1), server_default=text("'1'"))
    submit_time = Column(DateTime)
    release_time = Column(DateTime)
    source_size = Column(Integer, server_default=text("'0'"))
    source_format = Column(VARCHAR(12))
    source_flags = Column(VARCHAR(12))
    has_pilot_data = Column(TINYINT(1))
    title = Column(Text)
    authors = Column(Text)
    comments = Column(Text)
    proxy = Column(VARCHAR(255))
    report_num = Column(Text)
    msc_class = Column(String(255))
    acm_class = Column(String(255))
    journal_ref = Column(Text)
    doi = Column(String(255))
    abstract = Column(Text)
    license = Column(VARCHAR(255))
    type = Column(CHAR(8))
    is_ok = Column(TINYINT(1))
    admin_ok = Column(TINYINT(1))
    allow_tex_produced = Column(TINYINT(1), server_default=text("'0'"))
    is_oversize = Column(TINYINT(1), server_default=text("'0'"))
    rt_ticket_id = Column(INTEGER)
    auto_hold = Column(TINYINT(1), server_default=text("'0'"))
    agreement_id = Column(SMALLINT)

    agreement = relationship('SubmissionAgreements', back_populates='arXiv_submissions')
    document = relationship('Documents', back_populates='arXiv_submissions')
    arXiv_licenses = relationship('Licenses', back_populates='arXiv_submissions')
    submitter = relationship('TapirUsers', back_populates='arXiv_submissions')
    sword = relationship('Tracking', back_populates='arXiv_submissions')
    arXiv_pilot_files = relationship('PilotFiles', back_populates='submission')
    arXiv_submission_category = relationship('SubmissionCategory', back_populates='submission')
    arXiv_submission_category_proposal = relationship('SubmissionCategoryProposal', back_populates='submission')
    arXiv_submission_flag = relationship('SubmissionFlag', back_populates='submission')
    arXiv_submission_hold_reason = relationship('SubmissionHoldReason', back_populates='submission')
    arXiv_submission_near_duplicates = relationship('SubmissionNearDuplicates', back_populates='submission')
    arXiv_submission_qa_reports = relationship('SubmissionQaReports', back_populates='submission')
    arXiv_submission_view_flag = relationship('SubmissionViewFlag', back_populates='submission')


class TopPapers(Base):
    __tablename__ = 'arXiv_top_papers'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_top_papers_ibfk_1'),
        Index('document_id', 'document_id')
    )

    from_week = Column(Date, primary_key=True, nullable=False, server_default=text("'0000-00-00'"))
    class_ = Column('class', CHAR(1), primary_key=True, nullable=False, server_default=text("''"))
    rank = Column(SMALLINT, primary_key=True, nullable=False, server_default=text("'0'"))
    document_id = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))
    viewers = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))

    document = relationship('Documents', back_populates='arXiv_top_papers')


class Versions(Base):
    __tablename__ = 'arXiv_versions'
    __table_args__ = (
        ForeignKeyConstraint(['document_id'], ['arXiv_documents.document_id'], name='arXiv_versions_ibfk_1'),
        Index('freeze_date', 'freeze_date'),
        Index('publish_date', 'publish_date'),
        Index('request_date', 'request_date')
    )

    document_id = Column(MEDIUMINT, primary_key=True, nullable=False, server_default=text("'0'"))
    version = Column(TINYINT, primary_key=True, nullable=False, server_default=text("'0'"))
    request_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    freeze_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    publish_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_current = Column(MEDIUMINT, nullable=False, server_default=text("'0'"))

    document = relationship('Documents', back_populates='arXiv_versions')


class TapirAdminAudit(Base):
    __tablename__ = 'tapir_admin_audit'
    __table_args__ = (
        ForeignKeyConstraint(['admin_user'], ['tapir_users.user_id'], name='0_554'),
        ForeignKeyConstraint(['affected_user'], ['tapir_users.user_id'], name='0_555'),
        ForeignKeyConstraint(['session_id'], ['tapir_sessions.session_id'], name='0_553'),
        Index('admin_user', 'admin_user'),
        Index('affected_user', 'affected_user'),
        Index('data', 'data'),
        Index('data_2', 'data'),
        Index('data_3', 'data'),
        Index('ip_addr', 'ip_addr'),
        Index('log_date', 'log_date'),
        Index('session_id', 'session_id')
    )

    log_date = Column(INTEGER, nullable=False, server_default=text("'0'"))
    ip_addr = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    affected_user = Column(INTEGER, nullable=False, server_default=text("'0'"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    action = Column(String(32), nullable=False, server_default=text("''"))
    data = Column(Text, nullable=False)
    comment = Column(Text, nullable=False)
    entry_id = Column(INTEGER, primary_key=True)
    session_id = Column(INTEGER)
    admin_user = Column(INTEGER)

    tapir_users = relationship('TapirUsers', foreign_keys=[admin_user], back_populates='tapir_admin_audit')
    tapir_users_ = relationship('TapirUsers', foreign_keys=[affected_user], back_populates='tapir_admin_audit_')
    session = relationship('TapirSessions', back_populates='tapir_admin_audit')


t_tapir_email_change_tokens_used = Table(
    'tapir_email_change_tokens_used', metadata,
    Column('user_id', INTEGER, nullable=False, server_default=text("'0'")),
    Column('secret', String(32), nullable=False, server_default=text("''")),
    Column('used_when', INTEGER, nullable=False, server_default=text("'0'")),
    Column('used_from', String(16), nullable=False, server_default=text("''")),
    Column('remote_host', String(255), nullable=False, server_default=text("''")),
    Column('session_id', INTEGER, nullable=False, server_default=text("'0'")),
    ForeignKeyConstraint(['session_id'], ['tapir_sessions.session_id'], name='0_538'),
    ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_537'),
    Index('session_id', 'session_id'),
    Index('user_id', 'user_id')
)


class TapirEmailHeaders(Base):
    __tablename__ = 'tapir_email_headers'
    __table_args__ = (
        ForeignKeyConstraint(['template_id'], ['tapir_email_templates.template_id'], name='0_563'),
    )

    template_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    header_name = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    header_content = Column(String(255), nullable=False, server_default=text("''"))

    template = relationship('TapirEmailTemplates', back_populates='tapir_email_headers')


class TapirEmailMailings(Base):
    __tablename__ = 'tapir_email_mailings'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['tapir_users.user_id'], name='0_565'),
        ForeignKeyConstraint(['sent_by'], ['tapir_users.user_id'], name='0_566'),
        ForeignKeyConstraint(['template_id'], ['tapir_email_templates.template_id'], name='0_567'),
        Index('created_by', 'created_by'),
        Index('sent_by', 'sent_by'),
        Index('template_id', 'template_id')
    )

    mailing_id = Column(INTEGER, primary_key=True)
    template_id = Column(INTEGER)
    created_by = Column(INTEGER)
    sent_by = Column(INTEGER)
    created_date = Column(INTEGER)
    sent_date = Column(INTEGER)
    complete_date = Column(INTEGER)
    mailing_name = Column(String(255))
    comment = Column(Text)

    tapir_users = relationship('TapirUsers', foreign_keys=[created_by], back_populates='tapir_email_mailings')
    tapir_users_ = relationship('TapirUsers', foreign_keys=[sent_by], back_populates='tapir_email_mailings_')
    template = relationship('TapirEmailTemplates', back_populates='tapir_email_mailings')


t_tapir_email_tokens_used = Table(
    'tapir_email_tokens_used', metadata,
    Column('user_id', INTEGER, nullable=False, server_default=text("'0'")),
    Column('secret', String(32), nullable=False, server_default=text("''")),
    Column('used_when', INTEGER, nullable=False, server_default=text("'0'")),
    Column('used_from', String(16), nullable=False, server_default=text("''")),
    Column('remote_host', String(255), nullable=False, server_default=text("''")),
    Column('session_id', INTEGER, nullable=False, server_default=text("'0'")),
    ForeignKeyConstraint(['session_id'], ['tapir_sessions.session_id'], name='0_533'),
    ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_532'),
    Index('session_id', 'session_id'),
    Index('user_id', 'user_id')
)


class TapirPermanentTokens(Base):
    __tablename__ = 'tapir_permanent_tokens'
    __table_args__ = (
        ForeignKeyConstraint(['session_id'], ['tapir_sessions.session_id'], name='0_541'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_540'),
        Index('session_id', 'session_id')
    )

    user_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    valid = Column(Integer, nullable=False, server_default=text("'1'"))
    issued_when = Column(INTEGER, nullable=False, server_default=text("'0'"))
    issued_to = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    session_id = Column(INTEGER, nullable=False, server_default=text("'0'"))

    session = relationship('TapirSessions', back_populates='tapir_permanent_tokens')
    user = relationship('TapirUsers', back_populates='tapir_permanent_tokens')


t_tapir_permanent_tokens_used = Table(
    'tapir_permanent_tokens_used', metadata,
    Column('user_id', INTEGER),
    Column('secret', String(32), nullable=False, server_default=text("''")),
    Column('used_when', INTEGER),
    Column('used_from', String(16)),
    Column('remote_host', String(255), nullable=False, server_default=text("''")),
    Column('session_id', INTEGER, nullable=False, server_default=text("'0'")),
    ForeignKeyConstraint(['session_id'], ['tapir_sessions.session_id'], name='0_544'),
    ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_543'),
    Index('session_id', 'session_id'),
    Index('user_id', 'user_id')
)


class TapirRecoveryTokensUsed(Base):
    __tablename__ = 'tapir_recovery_tokens_used'
    __table_args__ = (
        ForeignKeyConstraint(['session_id'], ['tapir_sessions.session_id'], name='0_549'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_548'),
        Index('session_id', 'session_id')
    )

    user_id = Column(INTEGER, primary_key=True, nullable=False, server_default=text("'0'"))
    secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    used_when = Column(INTEGER)
    used_from = Column(String(16))
    session_id = Column(INTEGER)

    session = relationship('TapirSessions', back_populates='tapir_recovery_tokens_used')
    user = relationship('TapirUsers', back_populates='tapir_recovery_tokens_used')


class TapirSessionsAudit(TapirSessions):
    __tablename__ = 'tapir_sessions_audit'
    __table_args__ = (
        ForeignKeyConstraint(['session_id'], ['tapir_sessions.session_id'], name='0_527'),
        Index('ip_addr', 'ip_addr'),
        Index('tracking_cookie', 'tracking_cookie')
    )

    session_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    ip_addr = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))


class DataciteDois(Base):
    __tablename__ = 'arXiv_datacite_dois'
    __table_args__ = (
        ForeignKeyConstraint(['metadata_id'], ['arXiv_metadata.metadata_id'], name='arXiv_datacite_dois_ibfk_1'),
        Index('account_paper_id', 'account', 'paper_id', unique=True),
        Index('metadata_id', 'metadata_id')
    )

    doi = Column(String(255), primary_key=True)
    metadata_id = Column(Integer, nullable=False)
    paper_id = Column(String(64), nullable=False)
    account = Column(Enum('test', 'prod'))
    created = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    metadata_ = relationship('Metadata', back_populates='arXiv_datacite_dois')


class EndorsementRequestsAudit(EndorsementRequests):
    __tablename__ = 'arXiv_endorsement_requests_audit'
    __table_args__ = (
        ForeignKeyConstraint(['request_id'], ['arXiv_endorsement_requests.request_id'], name='0_725'),
    )

    request_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    session_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    remote_addr = Column(String(16))
    remote_host = Column(String(255))
    tracking_cookie = Column(String(255))


class Endorsements(Base):
    __tablename__ = 'arXiv_endorsements'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class'], name='0_729'),
        ForeignKeyConstraint(['endorsee_id'], ['tapir_users.user_id'], name='0_728'),
        ForeignKeyConstraint(['endorser_id'], ['tapir_users.user_id'], name='0_727'),
        ForeignKeyConstraint(['request_id'], ['arXiv_endorsement_requests.request_id'], name='0_730'),
        Index('archive', 'archive', 'subject_class'),
        Index('endorsee_id', 'endorsee_id'),
        Index('endorser_id', 'endorser_id'),
        Index('endorser_id_2', 'endorser_id', 'endorsee_id', 'archive', 'subject_class', unique=True),
        Index('request_id', 'request_id')
    )

    endorsement_id = Column(INTEGER, primary_key=True)
    endorsee_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    archive = Column(String(16), nullable=False, server_default=text("''"))
    subject_class = Column(String(16), nullable=False, server_default=text("''"))
    flag_valid = Column(INTEGER, nullable=False, server_default=text("'0'"))
    point_value = Column(INTEGER, nullable=False, server_default=text("'0'"))
    issued_when = Column(INTEGER, nullable=False, server_default=text("'0'"))
    endorser_id = Column(INTEGER)
    type = Column(Enum('user', 'admin', 'auto'))
    request_id = Column(INTEGER)

    arXiv_categories = relationship('Categories', back_populates='arXiv_endorsements')
    endorsee = relationship('TapirUsers', foreign_keys=[endorsee_id], back_populates='arXiv_endorsements')
    endorser = relationship('TapirUsers', foreign_keys=[endorser_id], back_populates='arXiv_endorsements_')
    request = relationship('EndorsementRequests', back_populates='arXiv_endorsements')


class OwnershipRequests(Base):
    __tablename__ = 'arXiv_ownership_requests'
    __table_args__ = (
        ForeignKeyConstraint(['endorsement_request_id'], ['arXiv_endorsement_requests.request_id'], name='0_735'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_734'),
        Index('endorsement_request_id', 'endorsement_request_id'),
        Index('user_id', 'user_id')
    )

    request_id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    workflow_status = Column(Enum('pending', 'accepted', 'rejected'), nullable=False, server_default=text("'pending'"))
    endorsement_request_id = Column(INTEGER)

    endorsement_request = relationship('EndorsementRequests', back_populates='arXiv_ownership_requests')
    user = relationship('TapirUsers', back_populates='arXiv_ownership_requests')


class PilotDatasets(Submissions):
    __tablename__ = 'arXiv_pilot_datasets'
    __table_args__ = (
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], name='arXiv_pilot_datasets_cdfk3'),
    )

    submission_id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    last_checked = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    numfiles = Column(SMALLINT, server_default=text("'0'"))
    feed_url = Column(String(256))
    manifestation = Column(String(256))
    published = Column(TINYINT(1), server_default=text("'0'"))


class PilotFiles(Base):
    __tablename__ = 'arXiv_pilot_files'
    __table_args__ = (
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], name='arXiv_pilot_files_cdfk3'),
        Index('arXiv_pilot_files_cdfk3', 'submission_id')
    )

    file_id = Column(INTEGER, primary_key=True)
    submission_id = Column(Integer, nullable=False)
    filename = Column(String(256), server_default=text("''"))
    entity_url = Column(String(256))
    description = Column(String(80))
    byRef = Column(TINYINT(1), server_default=text("'1'"))

    submission = relationship('Submissions', back_populates='arXiv_pilot_files')


class SubmissionAbsClassifierData(Submissions):
    __tablename__ = 'arXiv_submission_abs_classifier_data'
    __table_args__ = (
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], ondelete='CASCADE', name='arXiv_submission_abs_classifier_data_ibfk_1'),
    )

    submission_id = Column(Integer, primary_key=True, server_default=text("'0'"))
    last_update = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    json = Column(Text)
    status = Column(Enum('processing', 'success', 'failed', 'no connection'))
    message = Column(Text)
    is_oversize = Column(TINYINT(1), server_default=text("'0'"))
    suggested_primary = Column(Text)
    suggested_reason = Column(Text)
    autoproposal_primary = Column(Text)
    autoproposal_reason = Column(Text)
    classifier_service_version = Column(Text)
    classifier_model_version = Column(Text)


class SubmissionCategory(Base):
    __tablename__ = 'arXiv_submission_category'
    __table_args__ = (
        ForeignKeyConstraint(['category'], ['arXiv_category_def.category'], name='arXiv_submission_category_fk_category'),
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], ondelete='CASCADE', onupdate='CASCADE', name='arXiv_submission_category_fk_submission_id'),
        Index('arXiv_submission_category_idx_category', 'category'),
        Index('arXiv_submission_category_idx_is_primary', 'is_primary'),
        Index('arXiv_submission_category_idx_is_published', 'is_published'),
        Index('arXiv_submission_category_idx_submission_id', 'submission_id')
    )

    submission_id = Column(Integer, primary_key=True, nullable=False)
    category = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    is_primary = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    is_published = Column(TINYINT(1), server_default=text("'0'"))

    arXiv_category_def = relationship('CategoryDef', back_populates='arXiv_submission_category')
    submission = relationship('Submissions', back_populates='arXiv_submission_category')


class SubmissionCategoryProposal(Base):
    __tablename__ = 'arXiv_submission_category_proposal'
    __table_args__ = (
        ForeignKeyConstraint(['category'], ['arXiv_category_def.category'], name='arXiv_submission_category_proposal_fk_category'),
        ForeignKeyConstraint(['proposal_comment_id'], ['arXiv_admin_log.id'], name='arXiv_submission_category_proposal_fk_prop_comment_id'),
        ForeignKeyConstraint(['response_comment_id'], ['arXiv_admin_log.id'], name='arXiv_submission_category_proposal_fk_resp_comment_id'),
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], ondelete='CASCADE', onupdate='CASCADE', name='arXiv_submission_category_proposal_fk_submission_id'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='arXiv_submission_category_proposal_fk_user_id'),
        Index('arXiv_submission_category_proposal_fk_prop_comment_id', 'proposal_comment_id'),
        Index('arXiv_submission_category_proposal_fk_resp_comment_id', 'response_comment_id'),
        Index('arXiv_submission_category_proposal_fk_user_id', 'user_id'),
        Index('arXiv_submission_category_proposal_idx_category', 'category'),
        Index('arXiv_submission_category_proposal_idx_is_primary', 'is_primary'),
        Index('arXiv_submission_category_proposal_idx_key', 'proposal_id'),
        Index('arXiv_submission_category_proposal_idx_submission_id', 'submission_id')
    )

    proposal_id = Column(Integer, primary_key=True, nullable=False)
    submission_id = Column(Integer, primary_key=True, nullable=False)
    category = Column(VARCHAR(32), primary_key=True, nullable=False)
    is_primary = Column(TINYINT(1), primary_key=True, nullable=False, server_default=text("'0'"))
    user_id = Column(INTEGER, nullable=False)
    proposal_status = Column(Integer, server_default=text("'0'"))
    updated = Column(DateTime)
    proposal_comment_id = Column(Integer)
    response_comment_id = Column(Integer)

    arXiv_category_def = relationship('CategoryDef', back_populates='arXiv_submission_category_proposal')
    proposal_comment = relationship('AdminLog', foreign_keys=[proposal_comment_id], back_populates='arXiv_submission_category_proposal')
    response_comment = relationship('AdminLog', foreign_keys=[response_comment_id], back_populates='arXiv_submission_category_proposal_')
    submission = relationship('Submissions', back_populates='arXiv_submission_category_proposal')
    user = relationship('TapirUsers', back_populates='arXiv_submission_category_proposal')


class SubmissionClassifierData(Submissions):
    __tablename__ = 'arXiv_submission_classifier_data'
    __table_args__ = (
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], ondelete='CASCADE', name='arXiv_submission_classifier_data_ibfk_1'),
    )

    submission_id = Column(Integer, primary_key=True, server_default=text("'0'"))
    last_update = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    json = Column(Text)
    status = Column(Enum('processing', 'success', 'failed', 'no connection'))
    message = Column(Text)
    is_oversize = Column(TINYINT(1), server_default=text("'0'"))


class SubmissionFlag(Base):
    __tablename__ = 'arXiv_submission_flag'
    __table_args__ = (
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], ondelete='CASCADE', name='arXiv_submission_flag_ibfk_2'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], ondelete='CASCADE', name='arXiv_submission_flag_ibfk_1'),
        Index('uniq_one_flag_per_mod', 'submission_id', 'user_id', unique=True),
        Index('user_id', 'user_id')
    )

    flag_id = Column(Integer, primary_key=True)
    user_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    submission_id = Column(Integer, nullable=False)
    flag = Column(TINYINT, nullable=False, server_default=text("'0'"))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    submission = relationship('Submissions', back_populates='arXiv_submission_flag')
    user = relationship('TapirUsers', back_populates='arXiv_submission_flag')


class SubmissionHoldReason(Base):
    __tablename__ = 'arXiv_submission_hold_reason'
    __table_args__ = (
        ForeignKeyConstraint(['comment_id'], ['arXiv_admin_log.id'], name='arXiv_submission_hold_reason_ibfk_3'),
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], ondelete='CASCADE', name='arXiv_submission_hold_reason_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], ondelete='CASCADE', name='arXiv_submission_hold_reason_ibfk_2'),
        Index('comment_id', 'comment_id'),
        Index('submission_id', 'submission_id'),
        Index('user_id', 'user_id')
    )

    reason_id = Column(Integer, primary_key=True, nullable=False)
    submission_id = Column(Integer, nullable=False)
    user_id = Column(INTEGER, primary_key=True, nullable=False)
    reason = Column(String(30))
    type = Column(String(30))
    comment_id = Column(Integer)

    comment = relationship('AdminLog', back_populates='arXiv_submission_hold_reason')
    submission = relationship('Submissions', back_populates='arXiv_submission_hold_reason')
    user = relationship('TapirUsers', back_populates='arXiv_submission_hold_reason')


class SubmissionNearDuplicates(Base):
    __tablename__ = 'arXiv_submission_near_duplicates'
    __table_args__ = (
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], ondelete='CASCADE', name='arXiv_submission_near_duplicates_ibfk_1'),
        Index('match', 'submission_id', 'matching_id', unique=True)
    )

    submission_id = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    matching_id = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    similarity = Column(DECIMAL(2, 1), nullable=False)
    last_update = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    submission = relationship('Submissions', back_populates='arXiv_submission_near_duplicates')


class SubmissionQaReports(Base):
    __tablename__ = 'arXiv_submission_qa_reports'
    __table_args__ = (
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], name='arXiv_submission_qa_reports_ibfk_1'),
        Index('report_key_name', 'report_key_name'),
        Index('submission_id', 'submission_id')
    )

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, nullable=False)
    report_key_name = Column(String(64), nullable=False)
    num_flags = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    report = Column(JSON, nullable=False)
    created = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    report_uri = Column(String(256))

    submission = relationship('Submissions', back_populates='arXiv_submission_qa_reports')


class SubmissionViewFlag(Base):
    __tablename__ = 'arXiv_submission_view_flag'
    __table_args__ = (
        ForeignKeyConstraint(['submission_id'], ['arXiv_submissions.submission_id'], ondelete='CASCADE', name='arXiv_submission_view_flag_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], ondelete='CASCADE', name='arXiv_submission_view_flag_ibfk_2'),
        Index('user_id', 'user_id')
    )

    submission_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(INTEGER, primary_key=True, nullable=False)
    flag = Column(TINYINT(1), server_default=text("'0'"))
    updated = Column(DateTime)

    submission = relationship('Submissions', back_populates='arXiv_submission_view_flag')
    user = relationship('TapirUsers', back_populates='arXiv_submission_view_flag')


class VersionsChecksum(Versions):
    __tablename__ = 'arXiv_versions_checksum'
    __table_args__ = (
        ForeignKeyConstraint(['document_id', 'version'], ['arXiv_versions.document_id', 'arXiv_versions.version'], name='arXiv_versions_checksum_ibfk_1'),
        Index('abs_md5sum', 'abs_md5sum'),
        Index('abs_size', 'abs_size'),
        Index('src_md5sum', 'src_md5sum'),
        Index('src_size', 'src_size')
    )

    document_id = Column(MEDIUMINT, primary_key=True, nullable=False, server_default=text("'0'"))
    version = Column(TINYINT, primary_key=True, nullable=False, server_default=text("'0'"))
    flag_abs_present = Column(INTEGER, nullable=False, server_default=text("'0'"))
    abs_size = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_src_present = Column(TINYINT, nullable=False, server_default=text("'0'"))
    src_size = Column(INTEGER, nullable=False, server_default=text("'0'"))
    abs_md5sum = Column(BINARY(16))
    src_md5sum = Column(BINARY(16))


class EndorsementsAudit(Endorsements):
    __tablename__ = 'arXiv_endorsements_audit'
    __table_args__ = (
        ForeignKeyConstraint(['endorsement_id'], ['arXiv_endorsements.endorsement_id'], name='0_732'),
    )

    endorsement_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    session_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    remote_addr = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    flag_knows_personally = Column(INTEGER, nullable=False, server_default=text("'0'"))
    flag_seen_paper = Column(INTEGER, nullable=False, server_default=text("'0'"))
    comment = Column(Text)


class OwnershipRequestsAudit(OwnershipRequests):
    __tablename__ = 'arXiv_ownership_requests_audit'
    __table_args__ = (
        ForeignKeyConstraint(['request_id'], ['arXiv_ownership_requests.request_id'], name='0_737'),
    )

    request_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    session_id = Column(INTEGER, nullable=False, server_default=text("'0'"))
    remote_addr = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    date = Column(INTEGER, nullable=False, server_default=text("'0'"))
