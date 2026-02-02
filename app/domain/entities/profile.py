"""
Profile Entity.

Represents the professional profile of the portfolio owner.
This is the core entity of the system - only ONE profile can exist.

Business Rules Applied:
- RB-P01: name is required (1-100 chars)
- RB-P02: headline is required (1-100 chars)
- RB-P03: bio is optional (max 1000 chars)
- RB-P04: location is optional (max 100 chars)
- RB-P05: avatarUrl is optional, must be valid URL if provided
"""

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..exceptions import (
    EmptyFieldError,
    InvalidLengthError,
    InvalidURLError,
)


@dataclass
class Profile:
    """
    Profile entity representing the portfolio owner's professional profile.

    This is a rich domain entity that maintains its own invariants.
    Only one profile can exist in the system (enforced at repository level).
    """

    id: str
    name: str
    headline: str
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_NAME_LENGTH = 100
    MAX_HEADLINE_LENGTH = 100
    MAX_BIO_LENGTH = 1000
    MAX_LOCATION_LENGTH = 100
    URL_PATTERN = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_name()
        self._validate_headline()
        self._validate_bio()
        self._validate_location()
        self._validate_avatar_url()

    @staticmethod
    def create(
        name: str,
        headline: str,
        bio: Optional[str] = None,
        location: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> "Profile":
        """
        Factory method to create a new Profile.

        Args:
            name: Full name of the professional
            headline: Professional headline/tagline
            bio: Optional biography
            location: Optional location
            avatar_url: Optional avatar image URL

        Returns:
            A new Profile instance with generated UUID
        """
        return Profile(
            id=str(uuid.uuid4()),
            name=name,
            headline=headline,
            bio=bio,
            location=location,
            avatar_url=avatar_url,
        )

    def update_basic_info(
        self,
        name: Optional[str] = None,
        headline: Optional[str] = None,
        bio: Optional[str] = None,
        location: Optional[str] = None,
    ) -> None:
        """
        Update basic profile information.

        Args:
            name: New name (optional)
            headline: New headline (optional)
            bio: New bio (optional)
            location: New location (optional)
        """
        if name is not None:
            self.name = name
            self._validate_name()

        if headline is not None:
            self.headline = headline
            self._validate_headline()

        if bio is not None:
            self.bio = bio
            self._validate_bio()

        if location is not None:
            self.location = location
            self._validate_location()

        self._mark_as_updated()

    def update_avatar(self, avatar_url: Optional[str]) -> None:
        """
        Update profile avatar URL.

        Args:
            avatar_url: New avatar URL or None to remove
        """
        self.avatar_url = avatar_url
        self._validate_avatar_url()
        self._mark_as_updated()

    def _validate_name(self) -> None:
        """Validate name field according to business rules."""
        if not self.name or not self.name.strip():
            raise EmptyFieldError("name")

        if len(self.name) > self.MAX_NAME_LENGTH:
            raise InvalidLengthError("name", max_length=self.MAX_NAME_LENGTH)

    def _validate_headline(self) -> None:
        """Validate headline field according to business rules."""
        if not self.headline or not self.headline.strip():
            raise EmptyFieldError("headline")

        if len(self.headline) > self.MAX_HEADLINE_LENGTH:
            raise InvalidLengthError("headline", max_length=self.MAX_HEADLINE_LENGTH)

    def _validate_bio(self) -> None:
        """Validate bio field according to business rules."""
        if self.bio is not None:
            if self.bio.strip() == "":
                self.bio = None  # Treat empty string as None
            elif len(self.bio) > self.MAX_BIO_LENGTH:
                raise InvalidLengthError("bio", max_length=self.MAX_BIO_LENGTH)

    def _validate_location(self) -> None:
        """Validate location field according to business rules."""
        if self.location is not None:
            if self.location.strip() == "":
                self.location = None  # Treat empty string as None
            elif len(self.location) > self.MAX_LOCATION_LENGTH:
                raise InvalidLengthError(
                    "location", max_length=self.MAX_LOCATION_LENGTH
                )

    def _validate_avatar_url(self) -> None:
        """Validate avatar URL format."""
        if self.avatar_url is not None:
            if self.avatar_url.strip() == "":
                self.avatar_url = None
            elif not self.URL_PATTERN.match(self.avatar_url):
                raise InvalidURLError(self.avatar_url)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Profile(id={self.id}, name={self.name}, headline={self.headline})"
