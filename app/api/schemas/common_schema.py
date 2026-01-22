from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from datetime import datetime

# Generic type para responses
T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
    """Respuesta exitosa genérica"""
    success: bool = True
    data: T
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Respuesta de error"""
    success: bool = False
    error: str
    message: str
    code: Optional[str] = None


class MessageResponse(BaseModel):
    """Respuesta simple con mensaje"""
    success: bool = True
    message: str


class TimestampMixin(BaseModel):
    """Mixin para campos de timestamp"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None