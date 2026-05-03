"""
Work Experience DTOs.

Data Transfer Objects for Work Experience use cases.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AddExperienceRequest:
    """Request to add a work experience."""

    profile_id: str
    role: str
    company: str
    start_date: datetime
    order_index: int
    description: str | None = None
    end_date: datetime | None = None
    location: str | None = None
    responsibilities: list[str] = field(default_factory=list)


@dataclass
class EditExperienceRequest:
    """Request to edit a work experience."""

    experience_id: str
    role: str | None = None
    company: str | None = None
    description: str | None = None
    location: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    responsibilities: list[str] | None = None


@dataclass
class DeleteExperienceRequest:
    """Request to delete a work experience."""

    experience_id: str


@dataclass
class ListExperiencesRequest:
    """Request to list work experiences."""

    profile_id: str
    ascending: bool = False  # Default: newest first


@dataclass
class WorkExperienceResponse:
    """Response containing work experience data."""

    id: str
    profile_id: str
    role: str
    company: str
    start_date: datetime
    end_date: datetime | None
    description: str | None
    location: str | None
    responsibilities: list[str]
    order_index: int
    created_at: datetime
    updated_at: datetime
    is_current: bool
    duration_months: int

    @classmethod
    def from_entity(cls, entity) -> "WorkExperienceResponse":
        """Create DTO from domain entity."""
        start = entity.start_date
        end = entity.end_date if entity.end_date is not None else datetime.utcnow()
        duration_months = (end.year - start.year) * 12 + (end.month - start.month)

        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            role=entity.role,
            company=entity.company,
            start_date=entity.start_date,
            end_date=entity.end_date,
            description=entity.description,
            location=entity.location,
            responsibilities=entity.responsibilities.copy(),
            order_index=entity.order_index,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_current=entity.is_current_position(),
            duration_months=duration_months,
        )


@dataclass
class WorkExperienceListResponse:
    """Response containing list of work experiences."""

    experiences: list[WorkExperienceResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "WorkExperienceListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            experiences=[WorkExperienceResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
