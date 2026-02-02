"""
AdditionalTraining Entity.

Represents additional training, courses, or workshops in the portfolio.

Business Rules Applied:
- RB-AT01: title is required (1-100 chars)
- RB-AT02: provider is required (1-100 chars)
- RB-AT03: completionDate is required
- RB-AT04: duration is optional (max 50 chars, e.g., "40 hours", "2 months")
- RB-AT05: certificateUrl is optional, must be valid URL if provided
- RB-AT06: description is optional (max 500 chars)
- RB-AT07: orderIndex is required and must be unique per profile
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
    InvalidTitleError,
    InvalidProviderError,
    InvalidOrderIndexError,
)


@dataclass
class AdditionalTraining:
    """
    AdditionalTraining entity representing courses, workshops, or other training.
    
    This entity represents non-formal education and professional development.
    """

    id: str
    profile_id: str
    title: str
    provider: str
    completion_date: datetime
    order_index: int
    duration: Optional[str] = None
    certificate_url: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_TITLE_LENGTH = 100
    MAX_PROVIDER_LENGTH = 100
    MAX_DURATION_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 500
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
        self._validate_title()
        self._validate_provider()
        self._validate_duration()
        self._validate_certificate_url()
        self._validate_description()
        self._validate_order_index()

    @staticmethod
    def create(
        profile_id: str,
        title: str,
        provider: str,
        completion_date: datetime,
        order_index: int,
        duration: Optional[str] = None,
        certificate_url: Optional[str] = None,
        description: Optional[str] = None,
    ) -> "AdditionalTraining":
        """
        Factory method to create a new AdditionalTraining.
        
        Args:
            profile_id: Reference to the Profile
            title: Training/course title
            provider: Organization/platform providing the training
            completion_date: When the training was completed
            order_index: Position in the ordered list
            duration: Training duration (e.g., "40 hours")
            certificate_url: URL to certificate
            description: Optional description
            
        Returns:
            A new AdditionalTraining instance with generated UUID
        """
        return AdditionalTraining(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            title=title,
            provider=provider,
            completion_date=completion_date,
            order_index=order_index,
            duration=duration,
            certificate_url=certificate_url,
            description=description,
        )

    def update_info(
        self,
        title: Optional[str] = None,
        provider: Optional[str] = None,
        completion_date: Optional[datetime] = None,
        duration: Optional[str] = None,
        certificate_url: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Update training information.
        
        Args:
            title: New title (optional)
            provider: New provider (optional)
            completion_date: New completion date (optional)
            duration: New duration (optional)
            certificate_url: New certificate URL (optional)
            description: New description (optional)
        """
        if title is not None:
            self.title = title
            self._validate_title()
        
        if provider is not None:
            self.provider = provider
            self._validate_provider()
        
        if completion_date is not None:
            self.completion_date = completion_date
        
        if duration is not None:
            self.duration = duration
            self._validate_duration()
        
        if certificate_url is not None:
            self.certificate_url = certificate_url
            self._validate_certificate_url()
        
        if description is not None:
            self.description = description
            self._validate_description()
        
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

    def _validate_title(self) -> None:
        """Validate title field according to business rules."""
        if not self.title or not self.title.strip():
            raise InvalidTitleError("Title cannot be empty")
        
        if len(self.title) > self.MAX_TITLE_LENGTH:
            raise InvalidLengthError("title", max_length=self.MAX_TITLE_LENGTH)

    def _validate_provider(self) -> None:
        """Validate provider field according to business rules."""
        if not self.provider or not self.provider.strip():
            raise InvalidProviderError("Provider cannot be empty")
        
        if len(self.provider) > self.MAX_PROVIDER_LENGTH:
            raise InvalidLengthError("provider", max_length=self.MAX_PROVIDER_LENGTH)

    def _validate_duration(self) -> None:
        """Validate duration field."""
        if self.duration is not None:
            if self.duration.strip() == "":
                self.duration = None
            elif len(self.duration) > self.MAX_DURATION_LENGTH:
                raise InvalidLengthError("duration", max_length=self.MAX_DURATION_LENGTH)

    def _validate_certificate_url(self) -> None:
        """Validate certificate URL format."""
        if self.certificate_url is not None:
            if self.certificate_url.strip() == "":
                self.certificate_url = None
            elif not self.URL_PATTERN.match(self.certificate_url):
                raise InvalidURLError(self.certificate_url)

    def _validate_description(self) -> None:
        """Validate description field."""
        if self.description is not None:
            if self.description.strip() == "":
                self.description = None
            elif len(self.description) > self.MAX_DESCRIPTION_LENGTH:
                raise InvalidLengthError("description", max_length=self.MAX_DESCRIPTION_LENGTH)

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"AdditionalTraining(id={self.id}, title={self.title}, provider={self.provider})"