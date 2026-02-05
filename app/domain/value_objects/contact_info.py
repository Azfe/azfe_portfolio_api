"""
ContactInfo Value Object.

Represents validated contact information (email and optional phone).

Value Object Principles:
- Immutability: Cannot be changed after creation
- Self-validation: Validates components on construction
- Equality by value: Two ContactInfo are equal if all components match
- Composition: Composed of Email and Phone VOs
"""

from dataclasses import dataclass

from .email import Email
from .phone import Phone


@dataclass(frozen=True)
class ContactInfo:
    """
    ContactInfo Value Object representing contact details.

    Attributes:
        email: Email address (required)
        phone: Phone number (optional)

    Business Rules:
        - Email is required
        - Phone is optional
        - Both must be valid if provided
        - Immutable after creation

    Examples:
        >>> info = ContactInfo.create(
        ...     email="john@example.com",
        ...     phone="+34612345678"
        ... )
        >>> info.email.value
        'john@example.com'
    """

    email: Email
    phone: Phone | None = None

    @staticmethod
    def create(email: str, phone: str | None = None) -> "ContactInfo":
        """
        Factory method to create ContactInfo.

        Args:
            email: Email address string
            phone: Phone number string (optional)

        Returns:
            A new ContactInfo instance

        Raises:
            InvalidEmailError: If email format is invalid
            InvalidPhoneError: If phone format is invalid
        """
        email_vo = Email.create(email)
        phone_vo = Phone.create(phone) if phone else None

        return ContactInfo(email=email_vo, phone=phone_vo)

    @staticmethod
    def from_value_objects(email: Email, phone: Phone | None = None) -> "ContactInfo":
        """
        Create ContactInfo from existing Email and Phone VOs.

        Args:
            email: Email value object
            phone: Phone value object (optional)

        Returns:
            A new ContactInfo instance
        """
        return ContactInfo(email=email, phone=phone)

    @staticmethod
    def email_only(email: str) -> "ContactInfo":
        """
        Create ContactInfo with only email.

        Args:
            email: Email address string

        Returns:
            A new ContactInfo instance with no phone
        """
        return ContactInfo.create(email=email, phone=None)

    def has_phone(self) -> bool:
        """Check if phone number is provided."""
        return self.phone is not None

    def get_email_value(self) -> str:
        """Get the email address as string."""
        return self.email.value

    def get_phone_value(self) -> str | None:
        """Get the phone number as string (None if not provided)."""
        return self.phone.value if self.phone else None

    def with_phone(self, phone: str) -> "ContactInfo":
        """
        Create a new ContactInfo with a different phone.

        Args:
            phone: New phone number string

        Returns:
            A new ContactInfo instance
        """
        phone_vo = Phone.create(phone)
        return ContactInfo(email=self.email, phone=phone_vo)

    def without_phone(self) -> "ContactInfo":
        """
        Create a new ContactInfo without phone.

        Returns:
            A new ContactInfo instance with no phone
        """
        return ContactInfo(email=self.email, phone=None)

    def with_email(self, email: str) -> "ContactInfo":
        """
        Create a new ContactInfo with a different email.

        Args:
            email: New email address string

        Returns:
            A new ContactInfo instance
        """
        email_vo = Email.create(email)
        return ContactInfo(email=email_vo, phone=self.phone)

    def __str__(self) -> str:
        """String representation for display."""
        if self.has_phone():
            return f"Email: {self.email}, Phone: {self.phone}"
        return f"Email: {self.email}"

    def __repr__(self) -> str:
        """String representation for debugging."""
        phone_repr = f", phone={self.phone!r}" if self.phone else ""
        return f"ContactInfo(email={self.email!r}{phone_repr})"

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, ContactInfo):
            return False
        return self.email == other.email and self.phone == other.phone

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash((self.email, self.phone))
