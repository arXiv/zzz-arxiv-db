from typing import Optional, Literal
from fastapi import Cookie, Depends, Header, HTTPException
import jwt
from sqlalchemy.orm import Session

import modapi.userstore as userstore
from modapi.config import config
from modapi.db import get_db
from .gcp_token_check import verify_token, email_from_idinfo

from pydantic import BaseModel

import logging
log = logging.getLogger(__name__)

if config.debug:
    log.setLevel(logging.DEBUG)

User = userstore.User


class Auth(BaseModel):
    """ See arxiv-auth users/arxiv/users/auth/sessions/store.py
    generate_cookie() """
    user_id: int
    session_id: str
    nonce: str
    expires: str


class RawAuth(BaseModel):
    rawjwt: str
    rawheader: Optional[str]
    via: Literal["cookie", "header"]
    key: str


def decode(token: str, secret: str):
    """Decode an auth token to access session information."""
    try:
        data = dict(jwt.decode(token, secret, algorithms=["HS256"]))
        return data
    except Exception as ex:
        log.debug('decode() Failed: %s' , ex)


def encode(user: Auth, secret: str) -> str:
    return jwt.encode(user.dict(), secret)


def user_jwt(user_id: int) -> str:
    """For use in testing to make a jwt."""
    return encode(
        Auth(
            user_id=user_id, session_id="fakesessionid",
            nonce="peaceout", expires="0"
        ),
        config.jwt_secret.get_secret_value(),
    )

if config.enable_modkey:
    log.info("modkey enabled")
    async def mod_header_user(modkey: Optional[str] = Header(None),
                              db: Session = Depends(get_db)
                              ) -> Optional[User]:
        """Gets the modkey header that is used for testing."""
        if not config.enable_modkey or not modkey or not modkey.startswith('mod-'):
            return None
        else:
            return await userstore.getuser_by_nick(modkey.lstrip('mod-'), db)
else:
    log.info("modkey disabled")
    async def mod_header_user() -> Optional[User]:
        return None


async def ng_jwt_cookie(
    ARXIVNG_SESSION_ID: Optional[str] = Cookie(None),
) -> Optional[RawAuth]:
    """Gets the NG session undecoded JWT via a HTTP cookie.

    As of Feb 2022 arxiv-check uses the ARXIVNG_SESSION_ID cookie for auth.
    Mods will log in to arxiv.org/login, get the cookie set, go to mod.arxiv.org/ui,
    and that will make REST calls to mod.arxiv.org/{ENDPOINT}."""
    if ARXIVNG_SESSION_ID:
        log.debug("Got a arxiv NG cookie named ARXIVNG_SESSION_ID")
        return RawAuth(rawjwt= ARXIVNG_SESSION_ID,
                       rawheader=None,
                       via= "cookie",
                       key= "ARXIVNG_SESSION_ID",
                       )
    else:
        return None


async def jwt_header(
    Authorization: Optional[str] = Header(None),
) -> Optional[RawAuth]:
    """Gets JWT from OAuth2.0 style Authorization Bearer header."""
    if not Authorization:
        return None

    parts = Authorization.split()
    if parts[0].lower() != "bearer":
        log.debug("Authorization header Failed, lacked bearer")
        return None
    if len(parts) != 2:
        log.debug("Authorization header Failed, not 2 parts")
        return None
    else:
        log.debug("Got header:Authorization with a JWT")
        log.debug("jwt_header(): %s", Authorization)
        return RawAuth(rawjwt= parts[1],
                       rawheader=Authorization,
                       via= "header",
                       key= "Authorization",
                       )


async def rawauth(
    ng_jwt_cookie: Optional[RawAuth] = Depends(ng_jwt_cookie),
    jwt_header: Optional[RawAuth] = Depends(jwt_header),
) -> Optional[RawAuth]:
    """Gets the JWT from cookie or header"""
    if ng_jwt_cookie:
        log.debug("rawauth(): using Cookie")
        return ng_jwt_cookie
    if jwt_header:
        log.debug("rawauth(): using Authorization header")
        return jwt_header
    else:
        return None


async def auth(rawauth: Optional[RawAuth] = Depends(rawauth),
               db: Session = Depends(get_db)) -> Optional[Auth]:
    """Gets a User object from the unencoded JWT auth object or None.

    This does not ensure that the user is a mod or admin. Use
    auth_user for that.

    This will try to decode with the JWT_SECRET then try GCP.

    Use this when you want the request to be authenticated and you
    want just the User. If you want a mod or admin user, use auth_user.
    """
    if not rawauth:
        log.debug("auth() Failed, no rawauth")
        return None
    try:
        data = decode(rawauth.rawjwt, config.jwt_secret.get_secret_value())
        #FYI: don't try GCP if the JWT decodes with JWT_SECRET
        if data:
            log.debug("auth(), found and decoded JWT with JWT_SECRET")
            user_id = data['user_id']
            user = await userstore.getuser(user_id, db)
            if not user:
                log.debug("auth() Failed: user %s is does not exist", user_id)
                return None
            else:
                return user

    except Exception as ex:
        log.debug("auth() Exception during NG JWT %s", ex)
        
    log.debug("auth() Unable to auth with NG JWT or cookie, trying GCP JWT")    
    try:
        idinfo = verify_token(config.audience, rawauth.rawjwt)
        if not idinfo:
            log.debug("auth() failed: Invalid JWT, No idinfo from GCP")
            return None
        else:
            log.debug("auth(): valid JWT from GCP")
            email = email_from_idinfo(idinfo)
            if not email:
                log.debug("auth() failed: no email from GCP")
                return None
            user = await userstore.get_user_by_email(email, db)
            if user:
                log.debug("auth() found arXiv user via GCP JWT")
                return user
            else:
                log.debug("auth() failed: no user with email %s", email)
                return None
    except Exception as ex:
        log.debug("auth() Exception during GCP JWT validation: %s", ex)

    log.debug("auth() Unable to auth with GCP JWT")
    return None


async def auth_user(auth: Optional[User] = Depends(auth),
                    mod: Optional[User] = Depends(mod_header_user)
                    ) -> User:
    """Check ensure authenticatoin and user is a mod or admin and gets a
    User object.

    This is the depends that you almost always want to use in modapi3.
    Use this if you want the request authenticated and you want to
    ensure a mod or admin and you also want a User object.
    """
    try:
        if mod and (mod.is_admin or mod.is_moderator):
            log.debug("auth_user(): Success via mod key")
            return mod
        
        if auth and (auth.is_admin or auth.is_moderator):
            log.debug("auth_user(): success via NG JWT, GCP JWT or cookie")
            return auth

        log.debug("auth_user(): Failed")

    except Exception as ex:
        raise HTTPException(status_code=401,
                            detail="Unauthorized a_u_e") from ex
    else:
        raise HTTPException(status_code=401, detail="Unauthorized a_u")
