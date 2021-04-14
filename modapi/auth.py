from typing import Optional, Literal
from fastapi import Cookie, Depends, Header, HTTPException
import jwt

import modapi.userstore as userstore
import modapi.config as config

from pydantic import BaseModel

import logging
log = logging.getLogger(__name__)

User = userstore.User


class Auth(BaseModel):
    """ See arxiv-auth users/arxiv/users/auth/sessions/store.py
    generate_cookie() """

    user_id: int
    session_id: str
    nonce: str
    expires: str


class RawAuth:
    rawjwt: str
    via: Literal["cookie", "header"]
    key: str
    bearer: bool


def decode(token: str, secret: str):
    """Decode an auth token to access session information."""
    data = dict(jwt.decode(token, secret, algorithms=["HS256"]))
    return data


def encode(user: Auth, secret: str) -> str:
    return jwt.encode(user.dict(), secret)


def user_jwt(user_id: int) -> str:
    """For use in testing to make a jwt."""
    return encode(
        Auth(
            user_id=user_id, session_id="fakesessionid",
            nonce="peaceout", expires="0"
        ),
        config.jwt_secret,
    )


async def mod_header_user(modkey: Optional[str] = Header(None)
                          ) -> Optional[User]:
    """Gets the modkey header that is used for testing"""
    if not modkey or not modkey.startswith('mod-'):
        return None
    else:
        return await userstore.getuser_by_nick(modkey.lstrip('mod-'))


async def ng_jwt_cookie(
    ARXIVNG_SESSION_ID: Optional[str] = Cookie(None),
) -> Optional[RawAuth]:
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


async def ng_jwt_header(
    Authorization: Optional[str] = Header(None),
) -> Optional[RawAuth]:
    """Gets the NG session undecoded JWT via HTTP header"""
    if Authorization:
        bearer = Authorization.startswith("Bearer ")
        if bearer:
            Authorization = Authorization[len(bearer):]

        return {
            "rawjwt": Authorization,
            "via": "header",
            "key": "Authorization",
            "bearer": bearer,
        }
    else:
        return None


async def rawauth(
    ng_jwt_cookie: Optional[RawAuth] = Depends(ng_jwt_cookie),
    ng_jwt_header: Optional[RawAuth] = Depends(ng_jwt_header),
) -> Optional[RawAuth]:
    """Gets the JWT from cookie or header"""
    if ng_jwt_cookie or ng_jwt_header:
        return ng_jwt_cookie or ng_jwt_header
    else:
        return None


async def auth(rawauth: Optional[RawAuth] = Depends(rawauth)) -> Optional[Auth]:
    """Gets the auth object from the unencoded JWT auth object.

    Use this when you want the request to be authenticated and/or you
    want just the user_id. If you want a User object, use auth_user.

    """
    try:
        if not rawauth:
            return None
        data = decode(rawauth["rawjwt"], config.jwt_secret)
        return Auth(**data)
    except Exception as ex:
        raise HTTPException(
            status_code=401,
            detail=f'Unauthorized, invalid token via {rawauth["via"]}'
        ) from ex


async def auth_user(auth: Optional[Auth] = Depends(auth),
                    mod: Optional[User] = Depends(mod_header_user)
                    ) -> User:
    """Check authentication, ensure mod or admin, and gets a User object.

    Use this if you want the request authenticated and you also want a
    User object. If you do not need the User object, just use auth()

    """
    try:
        if mod and (mod.is_admin or mod.is_moderator):
            return mod

        if auth and auth.user_id:
            user = await userstore.getuser(auth.user_id)
            if user:
                if user.user_id and (user.is_admin or user.is_moderator):
                    return user
                else:
                    log.debug("User %d is not mod or admin", auth.user_id)
                    
            else:
                log.debug("User %d is not in userstore", auth.user_id)
    except Exception as ex:
        # raise HTTPException(status_code=401,
        # detail="Unauthorized a_u_e") from ex
        raise ex
    raise HTTPException(status_code=401, detail="Unauthorized a_u")
