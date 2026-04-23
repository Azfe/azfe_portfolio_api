"""
ContactInformation Entity.

Represents the official contact information of the portfolio owner.

Business Rules Applied:
- RB-CI01: email is required and must be valid format
- RB-CI02: phone is optional, must be valid format if provided
- RB-CI03: linkedin is optional, must be valid URL if provided
- RB-CI04: github is optional, must be valid URL if provided
- RB-CI05: website is optional, must be valid URL if provided
- RB-CI06: Only one ContactInformation per Profile
"""

from dataclasses import dataclass, field
from datetime import datetime
import re
import uuid

from ..exceptions import (
    EmptyFieldError,
    InvalidEmailError,
    InvalidPhoneError,
    InvalidURLError,
)


@dataclass
class ContactInformation:
    """
    ContactInformation entity representing official contact details.

    This is a value-rich entity that maintains format validation for all contact methods.
    Only one ContactInformation instance should exist per Profile.
    """

    id: str
    profile_id: str
    email: str
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    website: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Validation patterns
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    PHONE_PATTERN = re.compile(
        r"^\+?[1-9]\d{1,14}$"  # E.164 format (international phone numbers)
    )
    URL_PATTERN = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_profile_id()
        self._validate_email()
        self._validate_phone()
        self._validate_linkedin()
        self._validate_github()
        self._validate_website()

    @staticmethod
    def create(
        profile_id: str,
        email: str,
        phone: str | None = None,
        linkedin: str | None = None,
        github: str | None = None,
        website: str | None = None,
    ) -> "ContactInformation":
        """
        Factory method to create new ContactInformation.

        Args:
            profile_id: Reference to the Profile
            email: Primary email address
            phone: Phone number (optional)
            linkedin: LinkedIn profile URL (optional)
            github: GitHub profile URL (optional)
            website: Personal website URL (optional)

        Returns:
            A new ContactInformation instance with generated UUID
        """
        return ContactInformation(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            email=email,
            phone=phone,
            linkedin=linkedin,
            github=github,
            website=website,
        )

    def update_email(self, email: str) -> None:
        """
        Update email address.

        Args:
            email: New email address
        """
        self.email = email
        self._validate_email()
        self._mark_as_updated()

    def update_phone(self, phone: str | None) -> None:
        """
        Update phone number.

        Args:
            phone: New phone number or None to remove
        """
        self.phone = phone
        self._validate_phone()
        self._mark_as_updated()

    def update_social_links(
        self,
        linkedin: str | None = None,
        github: str | None = None,
        website: str | None = None,
    ) -> None:
        """
        Update social and web links.

        Args:
            linkedin: LinkedIn URL (optional)
            github: GitHub URL (optional)
            website: Website URL (optional)
        """
        if linkedin is not None:
            self.linkedin = linkedin
            self._validate_linkedin()

        if github is not None:
            self.github = github
            self._validate_github()

        if website is not None:
            self.website = website
            self._validate_website()

        self._mark_as_updated()

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_email(self) -> None:
        """Validate email format."""
        if not self.email or not self.email.strip():
            raise EmptyFieldError("email")

        if not self.EMAIL_PATTERN.match(self.email):
            raise InvalidEmailError(self.email)

    def _validate_phone(self) -> None:
        """Validate phone format if provided."""
        if self.phone is not None:
            if self.phone.strip() == "":
                self.phone = None
            else:
                # Remove common separators for validation
                phone_digits = (
                    self.phone.replace(" ", "")
                    .replace("-", "")
                    .replace("(", "")
                    .replace(")", "")
                )
                if not self.PHONE_PATTERN.match(phone_digits):
                    raise InvalidPhoneError(self.phone)

    def _validate_linkedin(self) -> None:
        """Validate LinkedIn URL format."""
        if self.linkedin is not None:
            if self.linkedin.strip() == "":
                self.linkedin = None
            elif not self.URL_PATTERN.match(self.linkedin):
                raise InvalidURLError(self.linkedin)

    def _validate_github(self) -> None:
        """Validate GitHub URL format."""
        if self.github is not None:
            if self.github.strip() == "":
                self.github = None
            elif not self.URL_PATTERN.match(self.github):
                raise InvalidURLError(self.github)

    def _validate_website(self) -> None:
        """Validate website URL format."""
        if self.website is not None:
            if self.website.strip() == "":
                self.website = None
            elif not self.URL_PATTERN.match(self.website):
                raise InvalidURLError(self.website)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"ContactInformation(id={self.id}, email={self.email})"
