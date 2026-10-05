from pydantic import BaseModel


class AIErrorDetail(BaseModel):
    code: str
    message: str


class AIErrorResponse(BaseModel):
    request_id: str
    success: bool = False
    error: AIErrorDetail
