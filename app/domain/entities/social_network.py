"""
SocialNetwork Entity.

Represents a social network profile link associated with the portfolio.

Business Rules Applied:
- RB-SN01: platform is required (1-50 chars, e.g., "LinkedIn", "Twitter")
- RB-SN02: platform must be unique per profile
- RB-SN03: url is required and must be valid
- RB-SN04: username is optional (max 100 chars)
- RB-SN05: orderIndex is required for display ordering
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import re
import uuid

from ..exceptions import (
    EmptyFieldError,
    InvalidLengthError,
    InvalidURLError,
    InvalidPlatformError,
    InvalidOrderIndexError,
)


@dataclass
class SocialNetwork:
    """
    SocialNetwork entity representing a social media profile.
    
    This entity maintains uniqueness by platform and validates URLs.
    """

    id: str
    profile_id: str
    platform: str
    url: str
    order_index: int
    username: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_PLATFORM_LENGTH = 50
    MAX_USERNAME_LENGTH = 100
    URL_PATTERN = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_profile_id()
        self._validate_platform()
        self._validate_url()
        self._validate_username()
        self._validate_order_index()

    @staticmethod
    def create(
        profile_id: str,
        platform: str,
        url: str,
        order_index: int,
        username: Optional[str] = None,
    ) -> "SocialNetwork":
        """
        Factory method to create a new SocialNetwork.
        
        Args:
            profile_id: Reference to the Profile
            platform: Social network platform name (e.g., "LinkedIn", "GitHub")
            url: Profile URL on the platform
            order_index: Position in the ordered list
            username: Username on the platform (optional)
            
        Returns:
            A new SocialNetwork instance with generated UUID
        """
        return SocialNetwork(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            platform=platform,
            url=url,
            order_index=order_index,
            username=username,
        )

    def update_info(
        self,
        platform: Optional[str] = None,
        url: Optional[str] = None,
        username: Optional[str] = None,
    ) -> None:
        """
        Update social network information.
        
        Args:
            platform: New platform name (optional)
            url: New URL (optional)
            username: New username (optional)
        """
        if platform is not None:
            self.platform = platform
            self._validate_platform()
        
        if url is not None:
            self.url = url
            self._validate_url()
        
        if username is not None:
            self.username = username
            self._validate_username()
        
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

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_platform(self) -> None:
        """Validate platform field according to business rules."""
        if not self.platform or not self.platform.strip():
            raise InvalidPlatformError("Platform cannot be empty")
        
        if len(self.platform) > self.MAX_PLATFORM_LENGTH:
            raise InvalidLengthError("platform", max_length=self.MAX_PLATFORM_LENGTH)

    def _validate_url(self) -> None:
        """Validate URL format."""
        if not self.url or not self.url.strip():
            raise EmptyFieldError("url")
        
        if not self.URL_PATTERN.match(self.url):
            raise InvalidURLError(self.url)

    def _validate_username(self) -> None:
        """Validate username field if provided."""
        if self.username is not None:
            if self.username.strip() == "":
                self.username = None
            elif len(self.username) > self.MAX_USERNAME_LENGTH:
                raise InvalidLengthError("username", max_length=self.MAX_USERNAME_LENGTH)

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"SocialNetwork(id={self.id}, platform={self.platform})"