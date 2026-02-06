"""
Education DTOs.

Data Transfer Objects for Education use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddEducationRequest:
    """Request to add education."""

    profile_id: str
    institution: str
    degree: str
    field: str
    start_date: datetime
    order_index: int
    description: str | None = None
    end_date: datetime | None = None


@dataclass
class EditEducationRequest:
    """Request to edit education."""

    education_id: str
    institution: str | None = None
    degree: str | None = None
    field: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


@dataclass
class DeleteEducationRequest:
    """Request to delete education."""

    education_id: str


@dataclass
class ListEducationRequest:
    """Request to list education entries."""

    profile_id: str
    ascending: bool = False  # Default: newest first


@dataclass
class EducationResponse:
    """Response containing education data."""

    id: str
    profile_id: str
    institution: str
    degree: str
    field: str
    start_date: datetime
    end_date: datetime | None
    description: str | None
    order_index: int
    created_at: datetime
    updated_at: datetime
    is_ongoing: bool

    @classmethod
    def from_entity(cls, entity) -> "EducationResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            institution=entity.institution,
            degree=entity.degree,
            field=entity.field,
            start_date=entity.start_date,
            end_date=entity.end_date,
            description=entity.description,
            order_index=entity.order_index,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_ongoing=entity.is_ongoing(),
        )


@dataclass
class EducationListResponse:
    """Response containing list of education entries."""

    education: list[EducationResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "EducationListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            education=[EducationResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
