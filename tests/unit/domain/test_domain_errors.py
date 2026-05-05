"""
Tests for domain error classes.

Covers all branches of InvalidLengthError and verifies each domain error
is a proper subclass of DomainError.
"""

import pytest

from app.domain.exceptions.domain_errors import (
    DomainError,
    DuplicateValueError,
    EmptyFieldError,
    InvalidCategoryError,
    InvalidCompanyError,
    InvalidDateRangeError,
    InvalidDescriptionError,
    InvalidEmailError,
    InvalidInstitutionError,
    InvalidIssuerError,
    InvalidLanguageProficiencyError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
    InvalidPhoneError,
    InvalidPlatformError,
    InvalidProgrammingLanguageLevelError,
    InvalidProviderError,
    InvalidRoleError,
    InvalidSkillLevelError,
    InvalidTitleError,
    InvalidURLError,
)


@pytest.mark.unit
class TestInvalidLengthErrorMessages:
    """Test InvalidLengthError message branches."""

    def test_min_length_message(self):
        """Should produce 'at least N characters' message when min_length given."""
        err = InvalidLengthError("description", min_length=10)

        assert "at least 10 characters" in str(err)
        assert "description" in str(err)

    def test_max_length_message(self):
        """Should produce 'exceeds maximum length' message when max_length given."""
        err = InvalidLengthError("name", max_length=50)

        assert "exceeds maximum length of 50" in str(err)
        assert "name" in str(err)

    def test_no_length_message(self):
        """Should produce generic message when neither min nor max given."""
        err = InvalidLengthError("field")

        assert "Invalid length for field" in str(err)

    def test_is_domain_error(self):
        """InvalidLengthError should be a DomainError."""
        err = InvalidLengthError("field", max_length=100)

        assert isinstance(err, DomainError)


@pytest.mark.unit
class TestDomainErrorSubclasses:
    """Verify all domain error classes are proper DomainError subclasses."""

    @pytest.mark.parametrize(
        "error_class",
        [
            EmptyFieldError,
            InvalidURLError,
            InvalidDateRangeError,
            InvalidOrderIndexError,
            InvalidNameError,
            InvalidTitleError,
            InvalidDescriptionError,
            InvalidCategoryError,
            InvalidSkillLevelError,
            InvalidRoleError,
            InvalidCompanyError,
            InvalidIssuerError,
            InvalidInstitutionError,
            InvalidEmailError,
            InvalidPhoneError,
            InvalidPlatformError,
            InvalidProviderError,
            DuplicateValueError,
            InvalidProgrammingLanguageLevelError,
            InvalidLanguageProficiencyError,
        ],
    )
    def test_is_domain_error_subclass(self, error_class):
        """Every domain error should be a subclass of DomainError."""
        assert issubclass(error_class, DomainError)

    def test_empty_field_error_message(self):
        """EmptyFieldError should store the field name."""
        err = EmptyFieldError("email")
        assert "email" in str(err)

    def test_invalid_url_error_message(self):
        """InvalidURLError should store the bad URL."""
        err = InvalidURLError("ftp://bad.url")
        assert "ftp://bad.url" in str(err)
