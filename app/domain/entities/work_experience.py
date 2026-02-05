"""
WorkExperience Entity.

Represents a professional work experience entry in the portfolio.

Business Rules Applied:
- RB-W01: role is required (1-100 chars)
- RB-W02: company is required (1-100 chars)
- RB-W03: description is optional (max 2000 chars)
- RB-W04: startDate is required
- RB-W05: endDate is optional (must be after startDate if provided)
- RB-W06: responsibilities is optional array (max 20 items, each max 500 chars)
- RB-W07: orderIndex is required and must be unique per profile
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import (
    EmptyFieldError,
    InvalidCompanyError,
    InvalidDateRangeError,
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidRoleError,
)


@dataclass
class WorkExperience:
    """
    WorkExperience entity representing a professional role.

    This entity maintains temporal coherence and ordering invariants.
    """

    id: str
    profile_id: str
    role: str
    company: str
    start_date: datetime
    order_index: int
    description: str | None = None
    end_date: datetime | None = None
    responsibilities: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_ROLE_LENGTH = 100
    MAX_COMPANY_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 2000
    MAX_RESPONSIBILITIES = 20
    MAX_RESPONSIBILITY_LENGTH = 500

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_profile_id()
        self._validate_role()
        self._validate_company()
        self._validate_description()
        self._validate_dates()
        self._validate_responsibilities()
        self._validate_order_index()

    @staticmethod
    def create(
        profile_id: str,
        role: str,
        company: str,
        start_date: datetime,
        order_index: int,
        description: str | None = None,
        end_date: datetime | None = None,
        responsibilities: list[str] | None = None,
    ) -> "WorkExperience":
        """
        Factory method to create a new WorkExperience.

        Args:
            profile_id: Reference to the Profile
            role: Job title/role
            company: Company name
            start_date: When the role started
            order_index: Position in the ordered list
            description: Optional job description
            end_date: When the role ended (None if current)
            responsibilities: Optional list of responsibilities

        Returns:
            A new WorkExperience instance with generated UUID
        """
        return WorkExperience(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            role=role,
            company=company,
            start_date=start_date,
            order_index=order_index,
            description=description,
            end_date=end_date,
            responsibilities=responsibilities or [],
        )

    def update_info(
        self,
        role: str | None = None,
        company: str | None = None,
        description: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> None:
        """
        Update work experience information.

        Args:
            role: New role (optional)
            company: New company (optional)
            description: New description (optional)
            start_date: New start date (optional)
            end_date: New end date (optional)
        """
        if role is not None:
            self.role = role
            self._validate_role()

        if company is not None:
            self.company = company
            self._validate_company()

        if description is not None:
            self.description = description
            self._validate_description()

        if start_date is not None:
            self.start_date = start_date

        if end_date is not None:
            self.end_date = end_date

        self._validate_dates()
        self._mark_as_updated()

    def update_responsibilities(self, responsibilities: list[str]) -> None:
        """
        Update responsibilities list.

        Args:
            responsibilities: New list of responsibilities
        """
        self.responsibilities = responsibilities
        self._validate_responsibilities()
        self._mark_as_updated()

    def add_responsibility(self, responsibility: str) -> None:
        """
        Add a single responsibility.

        Args:
            responsibility: Responsibility text to add
        """
        if len(self.responsibilities) >= self.MAX_RESPONSIBILITIES:
            raise InvalidLengthError(
                "responsibilities", max_length=self.MAX_RESPONSIBILITIES
            )

        if not responsibility or not responsibility.strip():
            raise EmptyFieldError("responsibility")

        if len(responsibility) > self.MAX_RESPONSIBILITY_LENGTH:
            raise InvalidLengthError(
                "responsibility", max_length=self.MAX_RESPONSIBILITY_LENGTH
            )

        self.responsibilities.append(responsibility)
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

    def is_current_position(self) -> bool:
        """Check if this is a current position (no end date)."""
        return self.end_date is None

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_role(self) -> None:
        """Validate role field according to business rules."""
        if not self.role or not self.role.strip():
            raise InvalidRoleError("Role cannot be empty")

        if len(self.role) > self.MAX_ROLE_LENGTH:
            raise InvalidLengthError("role", max_length=self.MAX_ROLE_LENGTH)

    def _validate_company(self) -> None:
        """Validate company field according to business rules."""
        if not self.company or not self.company.strip():
            raise InvalidCompanyError("Company name cannot be empty")

        if len(self.company) > self.MAX_COMPANY_LENGTH:
            raise InvalidLengthError("company", max_length=self.MAX_COMPANY_LENGTH)

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

    def _validate_responsibilities(self) -> None:
        """Validate responsibilities list."""
        if len(self.responsibilities) > self.MAX_RESPONSIBILITIES:
            raise InvalidLengthError(
                "responsibilities", max_length=self.MAX_RESPONSIBILITIES
            )

        for resp in self.responsibilities:
            if not resp or not resp.strip():
                raise EmptyFieldError("responsibility item")
            if len(resp) > self.MAX_RESPONSIBILITY_LENGTH:
                raise InvalidLengthError(
                    "responsibility item", max_length=self.MAX_RESPONSIBILITY_LENGTH
                )

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"WorkExperience(id={self.id}, role={self.role}, company={self.company})"
