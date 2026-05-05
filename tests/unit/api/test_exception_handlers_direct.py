"""
Direct unit tests for exception handler functions.

These tests call the handler functions directly (not via HTTP) to achieve
high coverage of each handler branch without requiring the full ASGI stack.
"""

import json
from unittest.mock import MagicMock

import pytest

from app.api.exception_handlers import (
    application_exception_handler,
    business_rule_exception_handler,
    domain_error_handler,
    duplicate_exception_handler,
    forbidden_exception_handler,
    generic_exception_handler,
    not_found_exception_handler,
    request_validation_handler,
    unauthorized_exception_handler,
    validation_exception_handler,
)
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


def _make_request():
    """Return a minimal mock Request object."""
    return MagicMock()


def _parse(response):
    """Decode JSONResponse body."""
    return json.loads(response.body)


@pytest.mark.unit
class TestNotFoundHandlerDirect:
    """Direct tests for not_found_exception_handler."""

    @pytest.mark.asyncio
    async def test_status_code_is_404(self):
        response = await not_found_exception_handler(
            _make_request(), NotFoundException("Profile", "abc")
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_body_fields(self):
        response = await not_found_exception_handler(
            _make_request(), NotFoundException("Skill", "sk1")
        )
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Not Found"
        assert body["code"] == "NOT_FOUND"
        assert isinstance(body["message"], str)


@pytest.mark.unit
class TestValidationHandlerDirect:
    """Direct tests for validation_exception_handler."""

    @pytest.mark.asyncio
    async def test_status_code_is_422(self):
        response = await validation_exception_handler(
            _make_request(), ValidationException(["bad input"])
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_body_fields(self):
        response = await validation_exception_handler(
            _make_request(), ValidationException(["name is required"])
        )
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Validation Error"
        assert body["code"] == "VALIDATION_ERROR"


@pytest.mark.unit
class TestDuplicateHandlerDirect:
    """Direct tests for duplicate_exception_handler."""

    @pytest.mark.asyncio
    async def test_status_code_is_409(self):
        response = await duplicate_exception_handler(
            _make_request(), DuplicateException("Tool", "name", "Docker")
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_body_fields(self):
        response = await duplicate_exception_handler(
            _make_request(), DuplicateException("Tool", "name", "Docker")
        )
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Conflict"
        assert body["code"] == "DUPLICATE"


@pytest.mark.unit
class TestUnauthorizedHandlerDirect:
    """Direct tests for unauthorized_exception_handler."""

    @pytest.mark.asyncio
    async def test_status_code_is_401(self):
        response = await unauthorized_exception_handler(
            _make_request(), UnauthorizedException("token expired")
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_body_fields(self):
        response = await unauthorized_exception_handler(
            _make_request(), UnauthorizedException("not authenticated")
        )
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Unauthorized"
        assert body["code"] == "UNAUTHORIZED"


@pytest.mark.unit
class TestForbiddenHandlerDirect:
    """Direct tests for forbidden_exception_handler."""

    @pytest.mark.asyncio
    async def test_status_code_is_403(self):
        response = await forbidden_exception_handler(
            _make_request(), ForbiddenException("access denied")
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_body_fields(self):
        response = await forbidden_exception_handler(
            _make_request(), ForbiddenException("not allowed")
        )
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Forbidden"
        assert body["code"] == "FORBIDDEN"


@pytest.mark.unit
class TestBusinessRuleHandlerDirect:
    """Direct tests for business_rule_exception_handler."""

    @pytest.mark.asyncio
    async def test_status_code_is_400(self):
        response = await business_rule_exception_handler(
            _make_request(), BusinessRuleViolationException("rule violated")
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_body_fields(self):
        response = await business_rule_exception_handler(
            _make_request(), BusinessRuleViolationException("cannot delete profile")
        )
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Bad Request"
        assert body["code"] == "BUSINESS_RULE_VIOLATION"


@pytest.mark.unit
class TestApplicationExceptionHandlerDirect:
    """Direct tests for application_exception_handler (500 catch-all)."""

    @pytest.mark.asyncio
    async def test_status_code_is_500(self):
        response = await application_exception_handler(
            _make_request(), ApplicationException("unexpected")
        )
        assert response.status_code == 500

    @pytest.mark.asyncio
    async def test_body_fields(self):
        response = await application_exception_handler(
            _make_request(), ApplicationException("internal error")
        )
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Internal Server Error"
        assert body["code"] == "APPLICATION_ERROR"


@pytest.mark.unit
class TestDomainErrorHandlerDirect:
    """Direct tests for domain_error_handler."""

    @pytest.mark.asyncio
    async def test_status_code_is_400(self):
        class SomeDomainError(DomainError):
            def __init__(self):
                super().__init__("invariant violated")

        response = await domain_error_handler(_make_request(), SomeDomainError())
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_body_fields(self):
        class SomeDomainError(DomainError):
            def __init__(self):
                super().__init__("name cannot be empty")

        response = await domain_error_handler(_make_request(), SomeDomainError())
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Bad Request"
        assert body["code"] == "DOMAIN_ERROR"
        assert "name cannot be empty" in body["message"]


@pytest.mark.unit
class TestGenericExceptionHandlerDirect:
    """Direct tests for generic_exception_handler (final fallback)."""

    @pytest.mark.asyncio
    async def test_status_code_is_500(self):
        response = await generic_exception_handler(
            _make_request(), RuntimeError("boom")
        )
        assert response.status_code == 500

    @pytest.mark.asyncio
    async def test_body_fields(self):
        response = await generic_exception_handler(
            _make_request(), ValueError("unexpected state")
        )
        body = _parse(response)
        assert body["success"] is False
        assert body["error"] == "Internal Server Error"
        assert body["code"] == "INTERNAL_ERROR"
        assert "unexpected" in body["message"].lower()


@pytest.mark.unit
class TestRequestValidationHandlerDirect:
    """Direct tests for request_validation_handler."""

    @pytest.mark.asyncio
    async def test_status_code_is_422(self):
        from fastapi.exceptions import RequestValidationError

        exc = RequestValidationError(
            errors=[
                {
                    "loc": ("body", "name"),
                    "msg": "field required",
                    "type": "value_error.missing",
                    "input": {},
                    "url": "",
                }
            ]
        )
        response = await request_validation_handler(_make_request(), exc)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_combines_multiple_errors_into_message(self):
        from fastapi.exceptions import RequestValidationError

        exc = RequestValidationError(
            errors=[
                {
                    "loc": ("body", "email"),
                    "msg": "field required",
                    "type": "value_error.missing",
                    "input": {},
                    "url": "",
                },
                {
                    "loc": ("body", "name"),
                    "msg": "field required",
                    "type": "value_error.missing",
                    "input": {},
                    "url": "",
                },
            ]
        )
        response = await request_validation_handler(_make_request(), exc)
        body = _parse(response)

        assert body["code"] == "VALIDATION_ERROR"
        # Both field names should appear in the combined message
        assert "email" in body["message"]
        assert "name" in body["message"]

    @pytest.mark.asyncio
    async def test_body_has_expected_structure(self):
        from fastapi.exceptions import RequestValidationError

        exc = RequestValidationError(
            errors=[
                {
                    "loc": ("body", "order_index"),
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                    "input": "abc",
                    "url": "",
                }
            ]
        )
        response = await request_validation_handler(_make_request(), exc)
        body = _parse(response)

        assert body["success"] is False
        assert body["error"] == "Validation Error"
        assert "order_index" in body["message"]
