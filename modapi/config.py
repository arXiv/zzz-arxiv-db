import os
import secrets

db_url = os.environ.get('CLASSIC_DATABASE_URI', 'mysql+aiomysql://not-set-check-config.py/0000')  # arXiv legacy DB URL, must use aiomysql driver


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

reload = bool(os.environ.get("RELOAD", False))
"""Sets uvicorn reloading on code changes, Do not use in produciton."""

uvicorn_debug = bool(os.environ.get("UVICORN_DEBUG", False))
"""Sets uvicorn debugging output, Avoid using in produciton."""

debug = bool(os.environ.get("DEBUG", False))
"""Sets log level to DEBUG for modapi"""

echo_sql = bool(os.environ.get("ECHOSQL",False))
"""Sets SQLAlchemy to echo debugging"""

jwt_secret = os.environ.get("JWT_SECRET", "not-set-" + secrets.token_urlsafe(16))
"""NG JWT_SECRET from arxiv-auth login service"""

legacy_url_prefix = os.environ.get("LEGACY_URL_PREFIX", "https://arxiv.org")
"""URL Prefix to use for calls to legacy system"""

time_url = os.environ.get("TIMEURL", f"{legacy_url_prefix}/localtime")
"""URL to use as source of publish times"""

earliest_announce_url = os.environ.get("EARLIEST_ANNOUNCE_URL", f"{legacy_url_prefix}/modapi/earliest_announce")
"""URL to use for legacy earliest announcement service"""
