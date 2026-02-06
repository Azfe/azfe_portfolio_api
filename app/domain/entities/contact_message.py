"""
ContactMessage Entity.

Represents a message sent by an external user through the contact form.

Business Rules Applied:
- RB-CM01: name is required (1-100 chars)
- RB-CM02: email is required and must be valid format
- RB-CM03: message is required (10-2000 chars)
- RB-CM04: status is optional (pending, read, replied)
- RB-CM05: createdAt is automatically set
- RB-CM06: Messages are append-only (no updates after creation)
"""

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import (
    EmptyFieldError,
    InvalidEmailError,
    InvalidLengthError,
    InvalidNameError,
)

# Valid message statuses
VALID_MESSAGE_STATUSES = {"pending", "read", "replied"}


@dataclass
class ContactMessage:
    """
    ContactMessage entity representing an inquiry from a visitor.

    This is an append-only entity - messages should not be modified after creation.
    """

    id: str
    name: str
    email: str
    message: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "pending"
    read_at: datetime | None = None
    replied_at: datetime | None = None

    # Constants
    MAX_NAME_LENGTH = 100
    MIN_MESSAGE_LENGTH = 10
    MAX_MESSAGE_LENGTH = 2000
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_name()
        self._validate_email()
        self._validate_message()
        self._validate_status()

    @staticmethod
    def create(
        name: str,
        email: str,
        message: str,
    ) -> "ContactMessage":
        """
        Factory method to create a new ContactMessage.

        Args:
            name: Sender's name
            email: Sender's email
            message: Message content

        Returns:
            A new ContactMessage instance with generated UUID and pending status
        """
        return ContactMessage(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            message=message,
            status="pending",
        )

    def mark_as_read(self) -> None:
        """Mark the message as read."""
        if self.status == "pending":
            self.status = "read"
            self.read_at = datetime.utcnow()

    def mark_as_replied(self) -> None:
        """Mark the message as replied."""
        if self.status in {"pending", "read"}:
            self.status = "replied"
            self.replied_at = datetime.utcnow()
            if self.read_at is None:
                self.read_at = self.replied_at

    def is_pending(self) -> bool:
        """Check if message is pending."""
        return self.status == "pending"

    def is_read(self) -> bool:
        """Check if message has been read."""
        return self.status in {"read", "replied"}

    def is_replied(self) -> bool:
        """Check if message has been replied to."""
        return self.status == "replied"

    def _validate_name(self) -> None:
        """Validate name field according to business rules."""
        if not self.name or not self.name.strip():
            raise InvalidNameError("Name cannot be empty")

        if len(self.name) > self.MAX_NAME_LENGTH:
            raise InvalidLengthError("name", max_length=self.MAX_NAME_LENGTH)

    def _validate_email(self) -> None:
        """Validate email format."""
        if not self.email or not self.email.strip():
            raise EmptyFieldError("email")

        if not self.EMAIL_PATTERN.match(self.email):
            raise InvalidEmailError(self.email)

    def _validate_message(self) -> None:
        """Validate message field according to business rules."""
        if not self.message or not self.message.strip():
            raise EmptyFieldError("message")

        if len(self.message) < self.MIN_MESSAGE_LENGTH:
            raise InvalidLengthError("message", min_length=self.MIN_MESSAGE_LENGTH)

        if len(self.message) > self.MAX_MESSAGE_LENGTH:
            raise InvalidLengthError("message", max_length=self.MAX_MESSAGE_LENGTH)

    def _validate_status(self) -> None:
        """Validate status field."""
        if self.status not in VALID_MESSAGE_STATUSES:
            from ..exceptions import DomainError

            raise DomainError(
                f"Invalid status: '{self.status}'. Must be one of: {', '.join(VALID_MESSAGE_STATUSES)}"
            )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"ContactMessage(id={self.id}, from={self.name}, status={self.status})"
