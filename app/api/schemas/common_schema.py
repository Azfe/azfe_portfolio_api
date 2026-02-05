from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

# Generic type para responses
T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Respuesta exitosa genérica"""

    success: bool = True
    data: T
    message: str | None = None


class ErrorResponse(BaseModel):
    """Respuesta de error"""

    success: bool = False
    error: str
    message: str
    code: str | None = None


class MessageResponse(BaseModel):
    """Respuesta simple con mensaje"""

    success: bool = True
    message: str


class TimestampMixin(BaseModel):
    """Mixin para campos de timestamp"""

    created_at: datetime | None = None
    updated_at: datetime | None = None
