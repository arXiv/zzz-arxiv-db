import secrets
from typing import Union

from pydantic import (
    BaseSettings,
    AnyHttpUrl,
    SecretStr
)


class Settings(BaseSettings):
    classic_db_uri: str = 'mysql://not-set-check-config/0000'
    """arXiv legacy DB URL.

     As of 2021-06-03 no longer using aiomysql driver"""

    reload: bool = False
    """Sets uvicorn reloading on code changes, Do not use in produciton."""

    uvicorn_debug: bool = False
    """Sets uvicorn debugging output, Avoid using in produciton."""

    debug: bool = False
    """Sets log level to DEBUG for modapi"""

    echo_sql: bool = False
    """Sets SQLAlchemy to echo debugging"""

    collab_debug: bool = False
    """Debugging of the socketio collab app"""

    jwt_secret: SecretStr = "not-set-" + secrets.token_urlsafe(16)
    """NG JWT_SECRET from arxiv-auth login service"""

    legacy_url_prefix: AnyHttpUrl = "https://arxiv.org"
    """URL Prefix to use for calls to legacy system"""

    time_url: str = f"{legacy_url_prefix}/localtime"
    """URL to use as source of publish times"""

    earliest_announce_url: str = f"{legacy_url_prefix}/modapi/earliest_announce"
    """URL to use for legacy earliest announcement service"""

    enable_modkey: bool = False
    """Enable access via modkey. Do not run in production"""

    collab_updates: bool = True
    """Allows disabling of change updates sent via socketio"""

    allow_emails: bool = False
    """Allows modapi to send emails."""

    smtp_host: str = 'localhost'
    """SMTP host used to send emails."""

    email_log: Union[None, str] = None
    """Logs emails to a file. Only for debugging"""

    allow_origins = [
        "https://mod.arxiv.org",
        "https://dev.arxiv.org",
        "http://dev.arxiv.org:8001",
        "https://services.dev.arxiv.org",
        "http://services.dev.arxiv.org:8001",
        "https://api.beta.arxiv.org",
        "http://api.beta.arxiv.org:8001",
        "https://beta.arxiv.org",
        "https://arxiv.org",
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    """Origins allowed for CORS"""

    class Config:
        env_file = "env"
        """File to read environment from"""

        case_sensitive = False


config = Settings()
"""Settings build from defaults, env file, and env vars.

Environment vars have the higest precedence, defaults the lowest."""
