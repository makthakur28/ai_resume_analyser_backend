from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar

T = TypeVar("T")

class ErrorDetail(BaseModel):
    message: str
    details: Optional[dict] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail

class SuccessResponse(BaseModel, Generic[T]):
    data: T
    message: str = "Success"
