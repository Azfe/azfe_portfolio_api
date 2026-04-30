"""Tests for the ApplicationException hierarchy in shared/shared_exceptions."""

import pytest

from app.shared.shared_exceptions import (
    ApplicationException,
    BusinessRuleViolationException,
    DuplicateException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)


class TestApplicationException:
    @pytest.mark.unit
    def test_is_base_exception(self):
        exc = ApplicationException("something went wrong")

        assert isinstance(exc, Exception)

    @pytest.mark.unit
    def test_message_is_stored(self):
        exc = ApplicationException("something went wrong")

        assert exc.message == "something went wrong"

    @pytest.mark.unit
    def test_details_default_to_empty_dict(self):
        exc = ApplicationException("something went wrong")

        assert exc.details == {}

    @pytest.mark.unit
    def test_custom_details_are_stored(self):
        exc = ApplicationException("error", details={"key": "value"})

        assert exc.details == {"key": "value"}

    @pytest.mark.unit
    def test_str_representation_equals_message(self):
        exc = ApplicationException("something went wrong")

        assert str(exc) == "something went wrong"


class TestNotFoundException:
    @pytest.mark.unit
    def test_inherits_from_application_exception(self):
        exc = NotFoundException("Skill", "id-1")

        assert isinstance(exc, ApplicationException)

    @pytest.mark.unit
    def test_message_format(self):
        exc = NotFoundException("Skill", "id-1")

        assert exc.message == "Skill with id 'id-1' not found"

    @pytest.mark.unit
    def test_details_contains_resource_type(self):
        exc = NotFoundException("Skill", "id-1")

        assert exc.details["resource_type"] == "Skill"

    @pytest.mark.unit
    def test_details_contains_resource_id(self):
        exc = NotFoundException("Skill", "id-1")

        assert exc.details["resource_id"] == "id-1"

    @pytest.mark.unit
    def test_details_has_exactly_two_keys(self):
        exc = NotFoundException("Tool", "tool-99")

        assert set(exc.details.keys()) == {"resource_type", "resource_id"}

    @pytest.mark.unit
    def test_different_resource_types(self):
        exc = NotFoundException("Profile", "prof-42")

        assert exc.details["resource_type"] == "Profile"
        assert exc.details["resource_id"] == "prof-42"
        assert "Profile" in exc.message
        assert "prof-42" in exc.message


class TestDuplicateException:
    @pytest.mark.unit
    def test_inherits_from_application_exception(self):
        exc = DuplicateException("Skill", "name", "Python")

        assert isinstance(exc, ApplicationException)

    @pytest.mark.unit
    def test_message_format(self):
        exc = DuplicateException("Skill", "name", "Python")

        assert exc.message == "Skill with name='Python' already exists"

    @pytest.mark.unit
    def test_details_contains_resource_type(self):
        exc = DuplicateException("Tool", "name", "Docker")

        assert exc.details["resource_type"] == "Tool"

    @pytest.mark.unit
    def test_details_contains_field(self):
        exc = DuplicateException("Tool", "name", "Docker")

        assert exc.details["field"] == "name"

    @pytest.mark.unit
    def test_details_contains_value(self):
        exc = DuplicateException("Tool", "name", "Docker")

        assert exc.details["value"] == "Docker"

    @pytest.mark.unit
    def test_details_has_exactly_three_keys(self):
        exc = DuplicateException("Tool", "name", "Docker")

        assert set(exc.details.keys()) == {"resource_type", "field", "value"}


class TestValidationException:
    @pytest.mark.unit
    def test_inherits_from_application_exception(self):
        exc = ValidationException(["Field is required"])

        assert isinstance(exc, ApplicationException)

    @pytest.mark.unit
    def test_message_is_validation_failed(self):
        exc = ValidationException(["Field is required"])

        assert exc.message == "Validation failed"

    @pytest.mark.unit
    def test_details_contains_errors_list(self):
        errors = ["name is required", "order_index must be >= 0"]
        exc = ValidationException(errors)

        assert exc.details["errors"] == errors

    @pytest.mark.unit
    def test_single_error(self):
        exc = ValidationException(["name is required"])

        assert exc.details["errors"] == ["name is required"]

    @pytest.mark.unit
    def test_multiple_errors(self):
        errors = ["name is required", "profile_id is required", "invalid url"]
        exc = ValidationException(errors)

        assert len(exc.details["errors"]) == 3

    @pytest.mark.unit
    def test_empty_errors_list(self):
        exc = ValidationException([])

        assert exc.details["errors"] == []


class TestUnauthorizedException:
    @pytest.mark.unit
    def test_inherits_from_application_exception(self):
        exc = UnauthorizedException()

        assert isinstance(exc, ApplicationException)

    @pytest.mark.unit
    def test_default_message(self):
        exc = UnauthorizedException()

        assert exc.message == "Authentication required"

    @pytest.mark.unit
    def test_custom_message(self):
        exc = UnauthorizedException("Token expired")

        assert exc.message == "Token expired"

    @pytest.mark.unit
    def test_details_default_empty(self):
        exc = UnauthorizedException()

        assert exc.details == {}


class TestForbiddenException:
    @pytest.mark.unit
    def test_inherits_from_application_exception(self):
        exc = ForbiddenException()

        assert isinstance(exc, ApplicationException)

    @pytest.mark.unit
    def test_default_message(self):
        exc = ForbiddenException()

        assert exc.message == "Permission denied"

    @pytest.mark.unit
    def test_custom_message(self):
        exc = ForbiddenException("You cannot delete this resource")

        assert exc.message == "You cannot delete this resource"

    @pytest.mark.unit
    def test_details_default_empty(self):
        exc = ForbiddenException()

        assert exc.details == {}


class TestBusinessRuleViolationException:
    @pytest.mark.unit
    def test_inherits_from_application_exception(self):
        exc = BusinessRuleViolationException("RB-T02: name must be unique per profile")

        assert isinstance(exc, ApplicationException)

    @pytest.mark.unit
    def test_message_format(self):
        exc = BusinessRuleViolationException("name must be unique per profile")

        assert exc.message == "Business rule violation: name must be unique per profile"

    @pytest.mark.unit
    def test_details_default_none_becomes_empty(self):
        exc = BusinessRuleViolationException("some rule")

        assert exc.details == {}

    @pytest.mark.unit
    def test_custom_details_are_stored(self):
        details = {"rule_id": "RB-T02", "field": "name"}
        exc = BusinessRuleViolationException("name must be unique", details=details)

        assert exc.details == details

    @pytest.mark.unit
    def test_details_optional(self):
        exc = BusinessRuleViolationException("order_index must be positive")

        assert isinstance(exc.details, dict)


class TestExceptionHierarchy:
    @pytest.mark.unit
    def test_all_exceptions_inherit_from_application_exception(self):
        exceptions = [
            NotFoundException("X", "1"),
            DuplicateException("X", "name", "val"),
            ValidationException(["err"]),
            UnauthorizedException(),
            ForbiddenException(),
            BusinessRuleViolationException("rule"),
        ]
        for exc in exceptions:
            assert isinstance(
                exc, ApplicationException
            ), f"{type(exc).__name__} does not inherit from ApplicationException"

    @pytest.mark.unit
    def test_all_exceptions_are_python_exceptions(self):
        exceptions = [
            ApplicationException("base"),
            NotFoundException("X", "1"),
            DuplicateException("X", "name", "val"),
            ValidationException(["err"]),
            UnauthorizedException(),
            ForbiddenException(),
            BusinessRuleViolationException("rule"),
        ]
        for exc in exceptions:
            assert isinstance(
                exc, Exception
            ), f"{type(exc).__name__} does not inherit from Exception"

    @pytest.mark.unit
    def test_all_exceptions_can_be_raised_and_caught(self):
        subclasses = [
            NotFoundException("Resource", "id-1"),
            DuplicateException("Resource", "name", "val"),
            ValidationException(["error"]),
            UnauthorizedException(),
            ForbiddenException(),
            BusinessRuleViolationException("rule"),
        ]
        for exc in subclasses:
            with pytest.raises(ApplicationException):
                raise exc
