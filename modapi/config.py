import os

db_url = os.environ['CLASSIC_DATABASE_URI']  # arXiv legacy DB URL

allow_origins = [
    "https://api.beta.arxiv.org",
    "http://api.beta.arxiv.org:8001",
    "https://beta.arxiv.org",
    "https://arxiv.org",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:3000",
]

debug = bool(os.environ.get("DEBUG", False))

jwt_secret = os.environ['JWT_SECRET'] # NG JWT_SECRET
