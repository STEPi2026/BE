from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.auth import (
    AuthenticationErrorResponse,
    AuthenticationStatusResponse,
    EmailAvailabilityResponse,
    SignupRequest,
    SignupResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": AuthenticationErrorResponse,
            "description": "Authentication failed",
        }
    },
)


@router.get(
    "/status",
    response_model=AuthenticationStatusResponse,
    summary="Authentication foundation status",
)
def authentication_status() -> AuthenticationStatusResponse:
    """Expose a non-authenticating readiness endpoint until auth flows are added."""
    return AuthenticationStatusResponse(status="ready")


@router.get("/check-email", response_model=EmailAvailabilityResponse, summary="Check email availability")
def check_email(email: EmailStr, db: Session = Depends(get_db)) -> EmailAvailabilityResponse:
    normalized_email = str(email).lower()
    user = db.scalar(select(User).where(User.email == normalized_email))
    return EmailAvailabilityResponse(email=normalized_email, available=user is None)


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=SignupResponse,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Email is already registered",
        }
    },
    summary="Sign up a student account",
)
def signup(signup_request: SignupRequest, db: Session = Depends(get_db)) -> User:
    email = str(signup_request.email).lower()
    existing_user = db.scalar(select(User).where(User.email == email))

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    user = User(
        email=email,
        password_hash=hash_password(signup_request.password),
        name=signup_request.name,
        role="STUDENT",
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from exc

    db.refresh(user)
    return user
