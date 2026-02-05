"""
Application Layer Exceptions.

This module contains exceptions that bridge the gap between domain exceptions
and infrastructure/presentation layers.

These exceptions are used in use cases and should be mapped to appropriate
HTTP status codes in the API layer.

Exception Hierarchy:
    ApplicationException (base)
    ├── NotFoundException
    ├── ValidationException
    ├── DuplicateException
    ├── UnauthorizedException
    └── ForbiddenException
"""


from typing import Any


class ApplicationException(Exception):
    """
    Base exception for application layer errors.

    All application-level exceptions should inherit from this.
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(ApplicationException):
    """
    Exception raised when a requested resource is not found.

    Maps to HTTP 404.
    """

    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with id '{resource_id}' not found"
        super().__init__(
            message, {"resource_type": resource_type, "resource_id": resource_id}
        )


class ValidationException(ApplicationException):
    """
    Exception raised when request validation fails.

    Maps to HTTP 422 (Unprocessable Entity).
    """

    def __init__(self, errors: list[str]):
        message = "Validation failed"
        super().__init__(message, {"errors": errors})


class DuplicateException(ApplicationException):
    """
    Exception raised when attempting to create a duplicate resource.

    Maps to HTTP 409 (Conflict).
    """

    def __init__(self, resource_type: str, field: str, value: str):
        message = f"{resource_type} with {field}='{value}' already exists"
        super().__init__(
            message, {"resource_type": resource_type, "field": field, "value": value}
        )


class UnauthorizedException(ApplicationException):
    """
    Exception raised when authentication is required but not provided.

    Maps to HTTP 401.
    """

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message)


class ForbiddenException(ApplicationException):
    """
    Exception raised when user doesn't have permission for an action.

    Maps to HTTP 403.
    """

    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class BusinessRuleViolationException(ApplicationException):
    """
    Exception raised when a business rule is violated.

    Maps to HTTP 400 (Bad Request).
    """

    def __init__(self, rule: str, details: dict[str, Any] | None = None):
        message = f"Business rule violation: {rule}"
        super().__init__(message, details)


__all__ = [
    "ApplicationException",
    "NotFoundException",
    "ValidationException",
    "DuplicateException",
    "UnauthorizedException",
    "ForbiddenException",
    "BusinessRuleViolationException",
]
