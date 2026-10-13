from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AccessTokenResponse(BaseModel):
    """Standard access-token response for future login endpoints."""

    access_token: str
    token_type: Literal["bearer"] = "bearer"


class AccessTokenPayload(BaseModel):
    """Claims expected in an access token after verification."""

    model_config = ConfigDict(extra="ignore")

    sub: str = Field(description="User identifier")
    iat: datetime
    exp: datetime


class AuthenticationErrorResponse(BaseModel):
    detail: str


class AuthenticationStatusResponse(BaseModel):
    status: Literal["ready"]
