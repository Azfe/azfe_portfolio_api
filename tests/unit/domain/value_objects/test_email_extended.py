"""
Extended tests for Email Value Object.

Covers uncovered methods: try_create(), get_local_part(), get_domain(),
is_from_domain(), and __repr__/__hash__.
"""

import pytest

from app.domain.exceptions import EmptyFieldError, InvalidEmailError
from app.domain.value_objects.email import Email


@pytest.mark.value_object
class TestEmailTryCreate:
    """Test try_create() factory method."""

    def test_try_create_valid_returns_email(self):
        """try_create() with valid email should return Email instance."""
        result = Email.try_create("user@example.com")

        assert result is not None
        assert result.value == "user@example.com"

    def test_try_create_invalid_returns_none(self):
        """try_create() with invalid email should return None."""
        result = Email.try_create("not-an-email")

        assert result is None

    def test_try_create_empty_returns_none(self):
        """try_create() with empty string should return None."""
        result = Email.try_create("")

        assert result is None

    def test_try_create_normalizes_case(self):
        """try_create() should normalize to lowercase."""
        result = Email.try_create("USER@DOMAIN.COM")

        assert result is not None
        assert result.value == "user@domain.com"


@pytest.mark.value_object
class TestEmailLocalAndDomain:
    """Test get_local_part() and get_domain() methods."""

    def test_get_local_part(self):
        """Should return the part before @."""
        email = Email.create("alex@example.com")

        assert email.get_local_part() == "alex"

    def test_get_local_part_complex(self):
        """Should handle complex local parts."""
        email = Email.create("alex.zapata+portfolio@mail.example.com")

        assert email.get_local_part() == "alex.zapata+portfolio"

    def test_get_domain(self):
        """Should return the part after @."""
        email = Email.create("user@gmail.com")

        assert email.get_domain() == "gmail.com"

    def test_get_domain_subdomain(self):
        """Should return full domain including subdomains."""
        email = Email.create("user@mail.company.org")

        assert email.get_domain() == "mail.company.org"


@pytest.mark.value_object
class TestEmailIsFromDomain:
    """Test is_from_domain() method."""

    def test_is_from_matching_domain(self):
        """Should return True when email is from the specified domain."""
        email = Email.create("user@gmail.com")

        assert email.is_from_domain("gmail.com") is True

    def test_is_not_from_different_domain(self):
        """Should return False when email is from a different domain."""
        email = Email.create("user@gmail.com")

        assert email.is_from_domain("outlook.com") is False

    def test_is_from_domain_case_insensitive(self):
        """is_from_domain() should be case-insensitive."""
        email = Email.create("user@gmail.com")

        assert email.is_from_domain("GMAIL.COM") is True
        assert email.is_from_domain("Gmail.Com") is True


@pytest.mark.value_object
class TestEmailHashAndRepr:
    """Test __hash__ and __repr__ methods."""

    def test_hash_equal_for_same_email(self):
        """Two equal emails should have the same hash."""
        email1 = Email.create("user@example.com")
        email2 = Email.create("user@example.com")

        assert hash(email1) == hash(email2)

    def test_hash_allows_use_in_set(self):
        """Email should be usable in sets."""
        email1 = Email.create("user@example.com")
        email2 = Email.create("user@example.com")
        email3 = Email.create("other@example.com")

        email_set = {email1, email2, email3}

        assert len(email_set) == 2

    def test_repr(self):
        """__repr__ should return a useful debug representation."""
        email = Email.create("user@example.com")

        assert repr(email) == "Email('user@example.com')"

    def test_str(self):
        """__str__ should return the email value."""
        email = Email.create("user@example.com")

        assert str(email) == "user@example.com"


@pytest.mark.value_object
class TestEmailNotEqualToOtherType:
    """Test equality edge cases."""

    def test_not_equal_to_string(self):
        """Email should not be equal to a plain string."""
        email = Email.create("user@example.com")

        assert email != "user@example.com"

    def test_not_equal_to_none(self):
        """Email should not be equal to None."""
        email = Email.create("user@example.com")

        assert email != None  # noqa: E711
