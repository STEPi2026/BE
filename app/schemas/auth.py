from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class AccessTokenResponse(BaseModel):
    """Standard access-token response for future login endpoints."""

    access_token: str
    token_type: Literal["bearer"] = "bearer"


class EmailAvailabilityResponse(BaseModel):
    email: EmailStr
    available: bool


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


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


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        name = value.strip()
        if not name:
            raise ValueError("name must not be blank")
        return name

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("password must not be blank")
        return value


class SignupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    role: str
