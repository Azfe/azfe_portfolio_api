"""
Education Entity.

Represents a formal education entry in the portfolio.

Business Rules Applied:
- RB-E01: institution is required (1-100 chars)
- RB-E02: degree is required (1-100 chars)
- RB-E03: field is required (1-100 chars)
- RB-E04: startDate is required
- RB-E05: endDate is optional (must be after startDate if provided)
- RB-E06: description is optional (max 1000 chars)
- RB-E07: orderIndex is required and must be unique per profile
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..exceptions import (
    EmptyFieldError,
    InvalidDateRangeError,
    InvalidInstitutionError,
    InvalidLengthError,
    InvalidOrderIndexError,
)


@dataclass
class Education:
    """
    Education entity representing formal academic education.

    This entity maintains temporal coherence and ordering invariants.
    """

    id: str
    profile_id: str
    institution: str
    degree: str
    field: str
    start_date: datetime
    order_index: int
    description: Optional[str] = None
    end_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_INSTITUTION_LENGTH = 100
    MAX_DEGREE_LENGTH = 100
    MAX_FIELD_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 1000

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_profile_id()
        self._validate_institution()
        self._validate_degree()
        self._validate_field()
        self._validate_description()
        self._validate_dates()
        self._validate_order_index()

    @staticmethod
    def create(
        profile_id: str,
        institution: str,
        degree: str,
        field: str,
        start_date: datetime,
        order_index: int,
        description: Optional[str] = None,
        end_date: Optional[datetime] = None,
    ) -> "Education":
        """
        Factory method to create a new Education entry.

        Args:
            profile_id: Reference to the Profile
            institution: Educational institution name
            degree: Degree obtained or pursued
            field: Field of study
            start_date: When the education started
            order_index: Position in the ordered list
            description: Optional description
            end_date: When the education ended (None if ongoing)

        Returns:
            A new Education instance with generated UUID
        """
        return Education(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            institution=institution,
            degree=degree,
            field=field,
            start_date=start_date,
            order_index=order_index,
            description=description,
            end_date=end_date,
        )

    def update_info(
        self,
        institution: Optional[str] = None,
        degree: Optional[str] = None,
        field: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> None:
        """
        Update education information.

        Args:
            institution: New institution (optional)
            degree: New degree (optional)
            field: New field (optional)
            description: New description (optional)
            start_date: New start date (optional)
            end_date: New end date (optional)
        """
        if institution is not None:
            self.institution = institution
            self._validate_institution()

        if degree is not None:
            self.degree = degree
            self._validate_degree()

        if field is not None:
            self.field = field
            self._validate_field()

        if description is not None:
            self.description = description
            self._validate_description()

        if start_date is not None:
            self.start_date = start_date

        if end_date is not None:
            self.end_date = end_date

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

    def is_ongoing(self) -> bool:
        """Check if this education is ongoing (no end date)."""
        return self.end_date is None

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_institution(self) -> None:
        """Validate institution field according to business rules."""
        if not self.institution or not self.institution.strip():
            raise InvalidInstitutionError("Institution cannot be empty")

        if len(self.institution) > self.MAX_INSTITUTION_LENGTH:
            raise InvalidLengthError(
                "institution", max_length=self.MAX_INSTITUTION_LENGTH
            )

    def _validate_degree(self) -> None:
        """Validate degree field according to business rules."""
        if not self.degree or not self.degree.strip():
            raise EmptyFieldError("degree")

        if len(self.degree) > self.MAX_DEGREE_LENGTH:
            raise InvalidLengthError("degree", max_length=self.MAX_DEGREE_LENGTH)

    def _validate_field(self) -> None:
        """Validate field field according to business rules."""
        if not self.field or not self.field.strip():
            raise EmptyFieldError("field")

        if len(self.field) > self.MAX_FIELD_LENGTH:
            raise InvalidLengthError("field", max_length=self.MAX_FIELD_LENGTH)

    def _validate_description(self) -> None:
        """Validate description field."""
        if self.description is not None:
            if self.description.strip() == "":
                self.description = None
            elif len(self.description) > self.MAX_DESCRIPTION_LENGTH:
                raise InvalidLengthError(
                    "description", max_length=self.MAX_DESCRIPTION_LENGTH
                )

    def _validate_dates(self) -> None:
        """Validate date range coherence."""
        if self.end_date is not None and self.end_date <= self.start_date:
            raise InvalidDateRangeError(str(self.start_date), str(self.end_date))

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Education(id={self.id}, degree={self.degree}, institution={self.institution})"
