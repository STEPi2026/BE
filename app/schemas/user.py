from pydantic import BaseModel, ConfigDict, EmailStr


class CurrentUserResponse(BaseModel):
    """Safe public representation of the authenticated user."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    role: str
