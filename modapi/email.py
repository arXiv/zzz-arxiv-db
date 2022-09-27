"""Utility functions for building and sending emails."""
import smtplib
from typing import List
from email.message import EmailMessage
from threading import Lock

from .config import config

import logging

logger = logging.getLogger(__name__)


def send_email(msg: EmailMessage):
    """Send an email."""
    if not config.allow_emails:
        return
    try:
        smtp = smtplib.SMTP(config.smtp_host)
        smtp.send_message(msg)
        smtp.quit()
        _log_email(msg)
    except Exception as ex:
        logger.error(f"Error sending email: {ex}")
        _log_email(msg, more=f"Email Not sent due to {ex}: ")


def build_reject_cross_email(to_address: str, submission_id: int, categories: List[str]) -> EmailMessage:
    """Build email for rejected cross."""
    msg = EmailMessage()
    cat_str = str.join(", ", categories)
    msg["Subject"] = f"Cross-list for {submission_id} declined by moderators"
    msg["From"] = "moderation@arxiv.org"
    msg["Reply-to"] = msg["From"]
    msg["To"] = to_address
    body = (
        "Dear arXiv user,\n\n"
        "Your secondary category cross-list has been declined upon a notice from our\n"
        "moderators. The moderators determined the submission to be inappropriate\n"
        f"for the following categor{'ies' if len(categories) > 1 else 'y'}:\n\n"
        f"{cat_str}\n\n"
        "For more information on our moderation policies, see:\n"
        "https://arxiv.org/help/moderation\n\n"
        "Regards,\narXiv moderation"
    )
    msg.set_content(body)
    return msg


email_log_lock = Lock()


def _log_email(msg: EmailMessage, more=""):
    if not config.email_log:
        return
    try:
        with email_log_lock:
            with open(config.email_log, "a") as elfs:
                if not more.endswith("\n"):
                    more += "\n"
                elfs.write(more + msg.as_string())
    except Exception as ex:
        logger.error(f"Could not log email to file {config.email_log} due to {ex}")
