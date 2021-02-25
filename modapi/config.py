import os

allow_origins = [
    "https://beta.arxiv.org",
    "https://arxiv.org",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

debug = bool(os.environ.get("DEBUG", False))
