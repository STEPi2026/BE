from fastapi import APIRouter, status

from app.schemas.auth import AuthenticationErrorResponse, AuthenticationStatusResponse


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
