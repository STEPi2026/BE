from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings


password_hasher = PasswordHash.recommended()


class AuthenticationError(HTTPException):
    """Base exception for authentication failures exposed by the API."""

    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str) -> str:
    """Return a one-way Argon2 password hash without logging the password."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Safely verify a password against a stored hash."""
    try:
        return password_hasher.verify(password, password_hash)
    except (ValueError, TypeError):
        return False


def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
) -> str:
    """Create an access token containing only its subject and temporal claims."""
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + (
        expires_delta
        or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": str(subject), "iat": issued_at, "exp": expires_at}

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Validate and decode an access token using the configured algorithm only."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["exp", "iat", "sub"]},
        )
    except ExpiredSignatureError as exc:
        raise AuthenticationError("Access token has expired") from exc
    except InvalidTokenError as exc:
        raise AuthenticationError("Could not validate credentials") from exc

    if not isinstance(payload.get("sub"), str) or not payload["sub"]:
        raise AuthenticationError("Access token subject is invalid")

    return payload
