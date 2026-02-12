"""
Global exception handlers for FastAPI.

Maps domain and application exceptions to standardized HTTP error responses.
All responses follow the ErrorResponse schema for consistency.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.exceptions.domain_errors import DomainError
from app.shared.shared_exceptions import (
    ApplicationException,
    BusinessRuleViolationException,
    DuplicateException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)

logger = logging.getLogger(__name__)


def _error_response(
    status_code: int,
    error: str,
    message: str,
    code: str | None = None,
) -> JSONResponse:
    """Build a standardized error response."""
    body: dict[str, object] = {
        "success": False,
        "error": error,
        "message": message,
    }
    if code is not None:
        body["code"] = code
    return JSONResponse(status_code=status_code, content=body)


# ==================== APPLICATION EXCEPTION HANDLERS ====================


async def not_found_exception_handler(
    _request: Request, exc: NotFoundException
) -> JSONResponse:
    """NotFoundException → 404"""
    return _error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        error="Not Found",
        message=exc.message,
        code="NOT_FOUND",
    )


async def validation_exception_handler(
    _request: Request, exc: ValidationException
) -> JSONResponse:
    """ValidationException → 422"""
    return _error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error="Validation Error",
        message=exc.message,
        code="VALIDATION_ERROR",
    )


async def duplicate_exception_handler(
    _request: Request, exc: DuplicateException
) -> JSONResponse:
    """DuplicateException → 409"""
    return _error_response(
        status_code=status.HTTP_409_CONFLICT,
        error="Conflict",
        message=exc.message,
        code="DUPLICATE",
    )


async def unauthorized_exception_handler(
    _request: Request, exc: UnauthorizedException
) -> JSONResponse:
    """UnauthorizedException → 401"""
    return _error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        error="Unauthorized",
        message=exc.message,
        code="UNAUTHORIZED",
    )


async def forbidden_exception_handler(
    _request: Request, exc: ForbiddenException
) -> JSONResponse:
    """ForbiddenException → 403"""
    return _error_response(
        status_code=status.HTTP_403_FORBIDDEN,
        error="Forbidden",
        message=exc.message,
        code="FORBIDDEN",
    )


async def business_rule_exception_handler(
    _request: Request, exc: BusinessRuleViolationException
) -> JSONResponse:
    """BusinessRuleViolationException → 400"""
    return _error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        error="Bad Request",
        message=exc.message,
        code="BUSINESS_RULE_VIOLATION",
    )


async def application_exception_handler(
    _request: Request, exc: ApplicationException
) -> JSONResponse:
    """Catch-all for any ApplicationException not handled above → 500"""
    logger.error("Unhandled application exception: %s", exc.message)
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error="Internal Server Error",
        message=exc.message,
        code="APPLICATION_ERROR",
    )


# ==================== DOMAIN EXCEPTION HANDLER ====================


async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    """DomainError (any) → 400"""
    return _error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        error="Bad Request",
        message=str(exc),
        code="DOMAIN_ERROR",
    )


# ==================== FASTAPI / PYDANTIC HANDLERS ====================


async def request_validation_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Pydantic RequestValidationError → 422 with clean message."""
    errors = []
    for err in exc.errors():
        loc = " → ".join(str(part) for part in err["loc"])
        errors.append(f"{loc}: {err['msg']}")

    return _error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error="Validation Error",
        message="; ".join(errors),
        code="VALIDATION_ERROR",
    )


# ==================== GENERIC FALLBACK ====================


async def generic_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unexpected exceptions → 500. Logs full traceback."""
    logger.exception("Unhandled exception: %s", exc)
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error="Internal Server Error",
        message="An unexpected error occurred",
        code="INTERNAL_ERROR",
    )


# ==================== REGISTRATION ====================


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app.

    Order matters: specific exceptions must be registered before their
    base classes so FastAPI matches the most specific handler first.
    """
    # Application-layer (specific → generic)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ValidationException, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DuplicateException, duplicate_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ForbiddenException, forbidden_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(BusinessRuleViolationException, business_rule_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ApplicationException, application_exception_handler)  # type: ignore[arg-type]

    # Domain-layer
    app.add_exception_handler(DomainError, domain_error_handler)  # type: ignore[arg-type]

    # FastAPI / Pydantic validation
    app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore[arg-type]

    # Generic fallback
    app.add_exception_handler(Exception, generic_exception_handler)
