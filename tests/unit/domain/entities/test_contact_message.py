"""
Unit tests for ContactMessage Entity.

Tests cover:
- Entity creation with factory method
- Field validation (name, email, message)
- Email format validation
- Status management and transitions
- Query methods
- Business rules enforcement
- Append-only nature (no updates after creation)
"""

import pytest
from datetime import datetime
import uuid

from app.domain.entities.contact_message import ContactMessage, VALID_MESSAGE_STATUSES
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidEmailError,
    InvalidLengthError,
    InvalidNameError,
    DomainError,
)


# ==========================================
# VALID CONTACT MESSAGE CREATION TESTS
# ==========================================

class TestContactMessageCreation:
    """Tests for valid ContactMessage entity creation."""

    def test_create_with_all_required_fields(self, valid_email):
        """Should create ContactMessage with all required fields."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        assert message.id is not None
        assert message.name == "John Doe"
        assert message.email == valid_email
        assert message.message == "This is a test message with enough characters to be valid."
        assert message.status == "pending"
        assert message.created_at is not None
        assert message.read_at is None
        assert message.replied_at is None

    def test_create_generates_unique_id(self, valid_email):
        """Should generate unique UUID for each message."""
        message1 = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="First message with enough characters to be valid.",
        )
        message2 = ContactMessage.create(
            name="Jane Doe",
            email=valid_email,
            message="Second message with enough characters to be valid.",
        )

        assert message1.id != message2.id
        # Verify they are valid UUIDs
        uuid.UUID(message1.id)
        uuid.UUID(message2.id)

    def test_create_sets_timestamp(self, valid_email):
        """Should set created_at timestamp."""
        before = datetime.utcnow()
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )
        after = datetime.utcnow()

        assert before <= message.created_at <= after

    def test_create_sets_pending_status(self, valid_email):
        """Should set status to 'pending' on creation."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        assert message.status == "pending"
        assert message.is_pending()


# ==========================================
# NAME VALIDATION TESTS
# ==========================================

class TestContactMessageNameValidation:
    """Tests for ContactMessage name validation."""

    def test_empty_name_raises_error(self, valid_email):
        """Should raise InvalidNameError for empty name."""
        with pytest.raises(InvalidNameError):
            ContactMessage.create(
                name="",
                email=valid_email,
                message="This is a test message with enough characters to be valid.",
            )

    def test_whitespace_name_raises_error(self, valid_email):
        """Should raise InvalidNameError for whitespace-only name."""
        with pytest.raises(InvalidNameError):
            ContactMessage.create(
                name="   ",
                email=valid_email,
                message="This is a test message with enough characters to be valid.",
            )

    def test_too_long_name_raises_error(self, valid_email):
        """Should raise InvalidLengthError for name exceeding max length."""
        long_name = "A" * 101

        with pytest.raises(InvalidLengthError) as exc_info:
            ContactMessage.create(
                name=long_name,
                email=valid_email,
                message="This is a test message with enough characters to be valid.",
            )

        assert "name" in str(exc_info.value)

    def test_max_length_name_is_valid(self, valid_email):
        """Should accept name at exact max length."""
        max_name = "A" * 100

        message = ContactMessage.create(
            name=max_name,
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        assert message.name == max_name
        assert len(message.name) == 100


# ==========================================
# EMAIL VALIDATION TESTS
# ==========================================

class TestContactMessageEmailValidation:
    """Tests for ContactMessage email validation."""

    def test_empty_email_raises_error(self):
        """Should raise EmptyFieldError for empty email."""
        with pytest.raises(EmptyFieldError) as exc_info:
            ContactMessage.create(
                name="John Doe",
                email="",
                message="This is a test message with enough characters to be valid.",
            )

        assert "email" in str(exc_info.value)

    def test_whitespace_email_raises_error(self):
        """Should raise EmptyFieldError for whitespace-only email."""
        with pytest.raises(EmptyFieldError):
            ContactMessage.create(
                name="John Doe",
                email="   ",
                message="This is a test message with enough characters to be valid.",
            )

    def test_invalid_email_format_raises_error(self, invalid_email):
        """Should raise InvalidEmailError for invalid email format."""
        with pytest.raises(InvalidEmailError):
            ContactMessage.create(
                name="John Doe",
                email=invalid_email,
                message="This is a test message with enough characters to be valid.",
            )

    def test_email_without_at_raises_error(self):
        """Should raise InvalidEmailError for email without @ symbol."""
        with pytest.raises(InvalidEmailError):
            ContactMessage.create(
                name="John Doe",
                email="notanemail.com",
                message="This is a test message with enough characters to be valid.",
            )

    def test_email_without_domain_raises_error(self):
        """Should raise InvalidEmailError for email without domain."""
        with pytest.raises(InvalidEmailError):
            ContactMessage.create(
                name="John Doe",
                email="user@",
                message="This is a test message with enough characters to be valid.",
            )

    def test_email_without_tld_raises_error(self):
        """Should raise InvalidEmailError for email without TLD."""
        with pytest.raises(InvalidEmailError):
            ContactMessage.create(
                name="John Doe",
                email="user@domain",
                message="This is a test message with enough characters to be valid.",
            )

    def test_valid_email_formats(self):
        """Should accept various valid email formats."""
        valid_emails = [
            "test@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user123@test-domain.com",
            "first.last@subdomain.example.com",
        ]

        for email in valid_emails:
            message = ContactMessage.create(
                name="John Doe",
                email=email,
                message="This is a test message with enough characters to be valid.",
            )
            assert message.email == email


# ==========================================
# MESSAGE VALIDATION TESTS
# ==========================================

class TestContactMessageMessageValidation:
    """Tests for ContactMessage message content validation."""

    def test_empty_message_raises_error(self, valid_email):
        """Should raise EmptyFieldError for empty message."""
        with pytest.raises(EmptyFieldError) as exc_info:
            ContactMessage.create(
                name="John Doe",
                email=valid_email,
                message="",
            )

        assert "message" in str(exc_info.value)

    def test_whitespace_message_raises_error(self, valid_email):
        """Should raise EmptyFieldError for whitespace-only message."""
        with pytest.raises(EmptyFieldError):
            ContactMessage.create(
                name="John Doe",
                email=valid_email,
                message="   ",
            )

    def test_too_short_message_raises_error(self, valid_email):
        """Should raise InvalidLengthError for message below minimum length."""
        short_message = "Too short"  # 9 chars, min is 10

        with pytest.raises(InvalidLengthError) as exc_info:
            ContactMessage.create(
                name="John Doe",
                email=valid_email,
                message=short_message,
            )

        assert "message" in str(exc_info.value)

    def test_min_length_message_is_valid(self, valid_email):
        """Should accept message at exact minimum length."""
        min_message = "A" * 10  # Exactly 10 chars

        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message=min_message,
        )

        assert message.message == min_message
        assert len(message.message) == 10

    def test_too_long_message_raises_error(self, valid_email):
        """Should raise InvalidLengthError for message exceeding max length."""
        long_message = "A" * 2001  # Max is 2000

        with pytest.raises(InvalidLengthError) as exc_info:
            ContactMessage.create(
                name="John Doe",
                email=valid_email,
                message=long_message,
            )

        assert "message" in str(exc_info.value)

    def test_max_length_message_is_valid(self, valid_email):
        """Should accept message at exact max length."""
        max_message = "A" * 2000

        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message=max_message,
        )

        assert message.message == max_message
        assert len(message.message) == 2000


# ==========================================
# STATUS VALIDATION TESTS
# ==========================================

class TestContactMessageStatusValidation:
    """Tests for ContactMessage status validation."""

    def test_invalid_status_raises_error(self, valid_email):
        """Should raise DomainError for invalid status."""
        with pytest.raises(DomainError) as exc_info:
            ContactMessage(
                id=str(uuid.uuid4()),
                name="John Doe",
                email=valid_email,
                message="This is a test message with enough characters to be valid.",
                status="invalid_status",
            )

        assert "Invalid status" in str(exc_info.value)

    def test_valid_statuses_are_accepted(self, valid_email):
        """Should accept all valid statuses."""
        for status in VALID_MESSAGE_STATUSES:
            message = ContactMessage(
                id=str(uuid.uuid4()),
                name="John Doe",
                email=valid_email,
                message="This is a test message with enough characters to be valid.",
                status=status,
            )
            assert message.status == status


# ==========================================
# STATUS TRANSITION TESTS
# ==========================================

class TestContactMessageStatusTransitions:
    """Tests for ContactMessage status transitions."""

    def test_mark_as_read_from_pending(self, valid_email):
        """Should mark message as read from pending status."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        assert message.status == "pending"
        assert message.read_at is None

        before = datetime.utcnow()
        message.mark_as_read()
        after = datetime.utcnow()

        assert message.status == "read"
        assert message.read_at is not None
        assert before <= message.read_at <= after

    def test_mark_as_read_when_already_read_does_nothing(self, valid_email):
        """Should not change status when already read."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        message.mark_as_read()
        original_read_at = message.read_at

        # Try to mark as read again
        import time
        time.sleep(0.01)
        message.mark_as_read()

        assert message.status == "read"
        # read_at should not change
        assert message.read_at == original_read_at

    def test_mark_as_replied_from_pending(self, valid_email):
        """Should mark message as replied from pending status."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        assert message.status == "pending"
        assert message.read_at is None
        assert message.replied_at is None

        before = datetime.utcnow()
        message.mark_as_replied()
        after = datetime.utcnow()

        assert message.status == "replied"
        assert message.replied_at is not None
        assert message.read_at is not None  # Auto-set when replying
        assert before <= message.replied_at <= after
        assert message.read_at == message.replied_at

    def test_mark_as_replied_from_read(self, valid_email):
        """Should mark message as replied from read status."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        message.mark_as_read()
        original_read_at = message.read_at

        import time
        time.sleep(0.01)

        before = datetime.utcnow()
        message.mark_as_replied()
        after = datetime.utcnow()

        assert message.status == "replied"
        assert message.replied_at is not None
        assert before <= message.replied_at <= after
        # read_at should remain unchanged
        assert message.read_at == original_read_at

    def test_mark_as_replied_when_already_replied_does_nothing(self, valid_email):
        """Should not change status when already replied."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        message.mark_as_replied()
        original_replied_at = message.replied_at

        # Try to mark as replied again
        import time
        time.sleep(0.01)
        message.mark_as_replied()

        assert message.status == "replied"
        # replied_at should not change
        assert message.replied_at == original_replied_at


# ==========================================
# QUERY METHODS TESTS
# ==========================================

class TestContactMessageQueryMethods:
    """Tests for ContactMessage query methods."""

    def test_is_pending_returns_true_for_pending_status(self, valid_email):
        """Should return True for is_pending when status is pending."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        assert message.is_pending() is True

    def test_is_pending_returns_false_for_read_status(self, valid_email):
        """Should return False for is_pending when status is read."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )
        message.mark_as_read()

        assert message.is_pending() is False

    def test_is_pending_returns_false_for_replied_status(self, valid_email):
        """Should return False for is_pending when status is replied."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )
        message.mark_as_replied()

        assert message.is_pending() is False

    def test_is_read_returns_false_for_pending_status(self, valid_email):
        """Should return False for is_read when status is pending."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        assert message.is_read() is False

    def test_is_read_returns_true_for_read_status(self, valid_email):
        """Should return True for is_read when status is read."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )
        message.mark_as_read()

        assert message.is_read() is True

    def test_is_read_returns_true_for_replied_status(self, valid_email):
        """Should return True for is_read when status is replied (replied implies read)."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )
        message.mark_as_replied()

        assert message.is_read() is True

    def test_is_replied_returns_false_for_pending_status(self, valid_email):
        """Should return False for is_replied when status is pending."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        assert message.is_replied() is False

    def test_is_replied_returns_false_for_read_status(self, valid_email):
        """Should return False for is_replied when status is read."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )
        message.mark_as_read()

        assert message.is_replied() is False

    def test_is_replied_returns_true_for_replied_status(self, valid_email):
        """Should return True for is_replied when status is replied."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )
        message.mark_as_replied()

        assert message.is_replied() is True


# ==========================================
# ENTITY REPRESENTATION TESTS
# ==========================================

class TestContactMessageRepresentation:
    """Tests for ContactMessage entity representation."""

    def test_repr_contains_key_information(self, valid_email):
        """Should include key fields in __repr__."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        repr_str = repr(message)

        assert "ContactMessage" in repr_str
        assert message.id in repr_str
        assert "John Doe" in repr_str
        assert "pending" in repr_str


# ==========================================
# EDGE CASES TESTS
# ==========================================

class TestContactMessageEdgeCases:
    """Tests for ContactMessage edge cases."""

    def test_create_with_exact_boundary_lengths(self, valid_email):
        """Should accept fields at exact boundary lengths."""
        message = ContactMessage.create(
            name="A" * 100,  # Max name length
            email=valid_email,
            message="B" * 2000,  # Max message length
        )

        assert len(message.name) == 100
        assert len(message.message) == 2000

    def test_message_with_minimum_length(self, valid_email):
        """Should accept message with exactly minimum length."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="1234567890",  # Exactly 10 chars
        )

        assert len(message.message) == 10

    def test_status_transitions_preserve_timestamps(self, valid_email):
        """Should preserve timestamps during status transitions."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a test message with enough characters to be valid.",
        )

        created_at = message.created_at

        message.mark_as_read()
        assert message.created_at == created_at

        message.mark_as_replied()
        assert message.created_at == created_at

    def test_email_with_subdomain(self):
        """Should accept email with subdomain."""
        message = ContactMessage.create(
            name="John Doe",
            email="user@mail.example.com",
            message="This is a test message with enough characters to be valid.",
        )

        assert message.email == "user@mail.example.com"

    def test_email_with_plus_addressing(self):
        """Should accept email with plus addressing."""
        message = ContactMessage.create(
            name="John Doe",
            email="user+tag@example.com",
            message="This is a test message with enough characters to be valid.",
        )

        assert message.email == "user+tag@example.com"

    def test_message_with_special_characters(self, valid_email):
        """Should accept message with special characters."""
        special_message = "Hello! How are you? I'm interested in your work. Contact me at: user@example.com"

        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message=special_message,
        )

        assert message.message == special_message
