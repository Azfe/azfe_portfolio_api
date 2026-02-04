"""
Tests for Email Value Object.
"""

import pytest
from app.domain.value_objects.email import Email
from app.domain.exceptions import InvalidEmailError, EmptyFieldError


@pytest.mark.value_object
class TestEmailCreation:
    """Test Email creation."""

    def test_create_valid_email(self, valid_email):
        """Should create email with valid format."""
        email = Email.create(valid_email)
        
        assert email.value == valid_email.lower()

    def test_email_normalized_to_lowercase(self):
        """Should normalize to lowercase."""
        email = Email.create("TEST@EXAMPLE.COM")
        
        assert email.value == "test@example.com"


@pytest.mark.value_object
class TestEmailValidation:
    """Test Email validation."""

    def test_empty_email_raises_error(self):
        """Should raise error for empty email."""
        with pytest.raises(EmptyFieldError):
            Email.create("")

    def test_whitespace_email_raises_error(self):
        """Should raise error for whitespace."""
        with pytest.raises(EmptyFieldError):
            Email.create("   ")

    def test_missing_at_raises_error(self):
        """Should raise error without @."""
        with pytest.raises(InvalidEmailError):
            Email.create("notemail.com")

    def test_missing_domain_raises_error(self):
        """Should raise error without domain."""
        with pytest.raises(InvalidEmailError):
            Email.create("test@")


@pytest.mark.value_object
class TestEmailEquality:
    """Test Email equality."""

    def test_same_emails_equal(self):
        """Should be equal for same value."""
        email1 = Email.create("test@example.com")
        email2 = Email.create("test@example.com")
        
        assert email1 == email2

    def test_case_insensitive_equality(self):
        """Should be equal regardless of case."""
        email1 = Email.create("TEST@example.com")
        email2 = Email.create("test@EXAMPLE.com")
        
        assert email1 == email2


@pytest.mark.value_object  
class TestEmailImmutability:
    """Test Email immutability."""

    def test_email_is_immutable(self):
        """Should not allow modification."""
        email = Email.create("test@example.com")
        
        with pytest.raises(AttributeError):
            email.value = "new@example.com"