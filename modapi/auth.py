from typing import Optional, Literal
from fastapi import Cookie, Depends, Header
import jwt


class Auth:
    rawjwt: str
    via: Literal["cookie", "header"]
    key: str
    bearer: bool


def decode(token: str, secret: str):
    """Decode an auth token to access session information."""
    data = dict(jwt.decode(token, secret, algorithms=["HS256"]))
    return data


async def ng_jwt_cookie(
    ARXIVNG_SESSION_ID: Optional[str] = Cookie(None),
) -> Optional[Auth]:
    """Gets the NG session undecoded JWT via a HTTP cookie"""
    if ARXIVNG_SESSION_ID:
        return {
            "rawjwt": ARXIVNG_SESSION_ID,
            "via": "cookie",
            "key": "ARXIVNG_SESSION_ID",
            "bearer": False,
        }
    else:
        return None


async def ng_jwt_header(Authorization: Optional[str] = Header(None)) -> Optional[Auth]:
    """Gets the NG session undecoded JWT via HTTP header"""
    if Authorization:
        bearer = Authorization.startswith("Bearer ")
        return {
            "rawjwt": Authorization.removeprefix("Bearer "),
            "via": "header",
            "key": "Authorization",
            "bearer": bearer,
        }
    else:
        return None


async def auth(
    ng_jwt_cookie: Optional[Auth] = Depends(ng_jwt_cookie),
    ng_jwt_header: Optional[Auth] = Depends(ng_jwt_header),
) -> Optional[Auth]:
    """Gets the JWT from cookie or header"""
    return ng_jwt_cookie or ng_jwt_header or None
