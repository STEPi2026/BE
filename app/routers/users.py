from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.user import CurrentUserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=CurrentUserResponse, summary="Get current user")
def get_me(current_user: User = Depends(get_current_user)) -> User:
    """Return the authenticated user's account information without credentials."""
    return current_user
