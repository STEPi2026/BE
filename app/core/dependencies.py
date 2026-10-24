from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import AuthenticationError, decode_access_token
from app.db.database import get_db
from app.db.models.user import User


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Return the user identified by a valid Bearer access token."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError()

    payload = decode_access_token(credentials.credentials)
    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError) as exc:
        raise AuthenticationError("Access token subject is invalid") from exc

    if user_id <= 0:
        raise AuthenticationError("Access token subject is invalid")

    user = db.get(User, user_id)
    if user is None:
        raise AuthenticationError()

    return user
