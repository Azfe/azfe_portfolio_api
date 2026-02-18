"""
Email Value Object.

Represents a validated email address following RFC 5322 (simplified).

Value Object Principles:
- Immutability: Cannot be changed after creation
- Self-validation: Validates format on construction
- Equality by value: Two Emails are equal if addresses match
"""

from dataclasses import dataclass
import re

from ..exceptions import EmptyFieldError, InvalidEmailError


@dataclass(frozen=True)
class Email:
    """
    Email Value Object representing a validated email address.

    Attributes:
        value: The email address string

    Business Rules:
        - Must be non-empty
        - Must match valid email pattern
        - Case-insensitive comparison
        - Normalized to lowercase
    """

    value: str

    # Email validation pattern (simplified RFC 5322)
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    def __post_init__(self):
        """Validate and normalize email after initialization."""
        # Use object.__setattr__ because dataclass is frozen
        object.__setattr__(self, "value", self.value.strip().lower())
        self._validate()

    @staticmethod
    def create(value: str) -> "Email":
        """
        Factory method to create an Email.

        Args:
            value: Email address string

        Returns:
            A new Email instance

        Raises:
            EmptyFieldError: If value is empty
            InvalidEmailError: If format is invalid
        """
        return Email(value=value)

    @staticmethod
    def try_create(value: str) -> "Email | None":
        """
        Try to create an Email, returning None if invalid.

        Args:
            value: Email address string

        Returns:
            Email instance or None if invalid
        """
        try:
            return Email.create(value)
        except (InvalidEmailError, EmptyFieldError):
            return None

    def get_local_part(self) -> str:
        """
        Get the local part (before @) of the email.

        Returns:
            Local part of email (e.g., 'user' from 'user@example.com')
        """
        return self.value.split("@")[0]

    def get_domain(self) -> str:
        """
        Get the domain part (after @) of the email.

        Returns:
            Domain part of email (e.g., 'example.com' from 'user@example.com')
        """
        return self.value.split("@")[1]

    def is_from_domain(self, domain: str) -> bool:
        """
        Check if email is from a specific domain.

        Args:
            domain: Domain to check (e.g., 'gmail.com')

        Returns:
            True if email is from the specified domain
        """
        return self.get_domain().lower() == domain.lower()

    def _validate(self) -> None:
        """Validate the email format."""
        if not self.value:
            raise EmptyFieldError("email")

        if not self.EMAIL_PATTERN.match(self.value):
            raise InvalidEmailError(self.value)

    def __str__(self) -> str:
        """String representation for display."""
        return self.value

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Email('{self.value}')"

    def __eq__(self, other) -> bool:
        """Equality comparison (case-insensitive)."""
        if not isinstance(other, Email):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.value)
