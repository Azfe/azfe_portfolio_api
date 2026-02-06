"""
Certification Entity.

Represents a professional certification in the portfolio.

Business Rules Applied:
- RB-C01: title is required (1-100 chars)
- RB-C02: issuer is required (1-100 chars)
- RB-C03: issueDate is required
- RB-C04: expiryDate is optional (must be after issueDate if provided)
- RB-C05: credentialId is optional (max 100 chars)
- RB-C06: credentialUrl is optional, must be valid URL if provided
- RB-C07: orderIndex is required and must be unique per profile
"""

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import (
    EmptyFieldError,
    InvalidDateRangeError,
    InvalidIssuerError,
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidTitleError,
    InvalidURLError,
)


@dataclass
class Certification:
    """
    Certification entity representing a professional certification.

    This entity maintains temporal coherence and credential validation.
    """

    id: str
    profile_id: str
    title: str
    issuer: str
    issue_date: datetime
    order_index: int
    expiry_date: datetime | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_TITLE_LENGTH = 100
    MAX_ISSUER_LENGTH = 100
    MAX_CREDENTIAL_ID_LENGTH = 100
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
        self._validate_title()
        self._validate_issuer()
        self._validate_dates()
        self._validate_credential_id()
        self._validate_credential_url()
        self._validate_order_index()

    @staticmethod
    def create(
        profile_id: str,
        title: str,
        issuer: str,
        issue_date: datetime,
        order_index: int,
        expiry_date: datetime | None = None,
        credential_id: str | None = None,
        credential_url: str | None = None,
    ) -> "Certification":
        """
        Factory method to create a new Certification.

        Args:
            profile_id: Reference to the Profile
            title: Certification title
            issuer: Organization that issued the certification
            issue_date: When the certification was issued
            order_index: Position in the ordered list
            expiry_date: When the certification expires (None if no expiry)
            credential_id: Certification credential ID
            credential_url: URL to verify the credential

        Returns:
            A new Certification instance with generated UUID
        """
        return Certification(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            title=title,
            issuer=issuer,
            issue_date=issue_date,
            order_index=order_index,
            expiry_date=expiry_date,
            credential_id=credential_id,
            credential_url=credential_url,
        )

    def update_info(
        self,
        title: str | None = None,
        issuer: str | None = None,
        issue_date: datetime | None = None,
        expiry_date: datetime | None = None,
        credential_id: str | None = None,
        credential_url: str | None = None,
    ) -> None:
        """
        Update certification information.

        Args:
            title: New title (optional)
            issuer: New issuer (optional)
            issue_date: New issue date (optional)
            expiry_date: New expiry date (optional)
            credential_id: New credential ID (optional)
            credential_url: New credential URL (optional)
        """
        if title is not None:
            self.title = title
            self._validate_title()

        if issuer is not None:
            self.issuer = issuer
            self._validate_issuer()

        if issue_date is not None:
            self.issue_date = issue_date

        if expiry_date is not None:
            self.expiry_date = expiry_date

        if credential_id is not None:
            self.credential_id = credential_id
            self._validate_credential_id()

        if credential_url is not None:
            self.credential_url = credential_url
            self._validate_credential_url()

        self._validate_dates()
        self._mark_as_updated()

    def update_order(self, new_order_index: int) -> None:
        """
        Update the order index.

        Args:
            new_order_index: New position in the list
        """
        self.order_index = new_order_index
        self._validate_order_index()
        self._mark_as_updated()

    def is_expired(self) -> bool:
        """Check if certification has expired."""
        if self.expiry_date is None:
            return False
        return datetime.utcnow() > self.expiry_date

    def has_no_expiry(self) -> bool:
        """Check if certification has no expiry date."""
        return self.expiry_date is None

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_title(self) -> None:
        """Validate title field according to business rules."""
        if not self.title or not self.title.strip():
            raise InvalidTitleError("Title cannot be empty")

        if len(self.title) > self.MAX_TITLE_LENGTH:
            raise InvalidLengthError("title", max_length=self.MAX_TITLE_LENGTH)

    def _validate_issuer(self) -> None:
        """Validate issuer field according to business rules."""
        if not self.issuer or not self.issuer.strip():
            raise InvalidIssuerError("Issuer cannot be empty")

        if len(self.issuer) > self.MAX_ISSUER_LENGTH:
            raise InvalidLengthError("issuer", max_length=self.MAX_ISSUER_LENGTH)

    def _validate_dates(self) -> None:
        """Validate date range coherence."""
        if self.expiry_date is not None and self.expiry_date <= self.issue_date:
            raise InvalidDateRangeError(str(self.issue_date), str(self.expiry_date))

    def _validate_credential_id(self) -> None:
        """Validate credential ID field."""
        if self.credential_id is not None:
            if self.credential_id.strip() == "":
                self.credential_id = None
            elif len(self.credential_id) > self.MAX_CREDENTIAL_ID_LENGTH:
                raise InvalidLengthError(
                    "credential_id", max_length=self.MAX_CREDENTIAL_ID_LENGTH
                )

    def _validate_credential_url(self) -> None:
        """Validate credential URL format."""
        if self.credential_url is not None:
            if self.credential_url.strip() == "":
                self.credential_url = None
            elif not self.URL_PATTERN.match(self.credential_url):
                raise InvalidURLError(self.credential_url)

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Certification(id={self.id}, title={self.title}, issuer={self.issuer})"
