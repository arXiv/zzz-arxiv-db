"""Utility functions for building and sending emails."""
import smtplib
from typing import List
from email.message import EmailMessage

from .config import config

def send_email(msg: EmailMessage):
    """Send an email."""
    if not config.allow_emails:
        return
    try:
        smtp = smtplib.SMTP(config.smtp_host)
        smtp.send_message(msg)
        smtp.quit()
    except Exception as ex:
        print(f"Error sending email: {ex}")

def build_reject_cross_email(to_address: str, categories: List[str]) -> EmailMessage:
    """Build email for rejected cross."""
    msg = EmailMessage()
    cat_str = str.join(', ', categories)
    msg['Subject'] = "Cross-list declined"
    msg['From'] = "moderation@arxiv.org"
    msg['Reply-to'] = msg['From']
    msg['To'] = to_address
    body = "Dear arXiv user,\n\n" \
           "Your secondary category cross-list has been declined upon a notice from our\n" \
           "moderators. The moderators determined the submission to be inappropriate\n" \
           f"for the following categor{'ies' if len(categories) > 1 else 'y'}:\n\n" \
           f"{cat_str}\n\n" \
           "For more information on our moderation policies, see:\n" \
           "https://arxiv.org/help/moderation\n\n" \
           "Regards,\narXiv moderation"
    msg.set_content(body)
    return msg
