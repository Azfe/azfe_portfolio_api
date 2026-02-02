"""
Work Experience DTOs.

Data Transfer Objects for Work Experience use cases.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class AddExperienceRequest:
    """Request to add a work experience."""
    profile_id: str
    role: str
    company: str
    start_date: datetime
    order_index: int
    description: Optional[str] = None
    end_date: Optional[datetime] = None
    responsibilities: List[str] = None

    def __post_init__(self):
        if self.responsibilities is None:
            self.responsibilities = []


@dataclass
class EditExperienceRequest:
    """Request to edit a work experience."""
    experience_id: str
    role: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    responsibilities: Optional[List[str]] = None


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
    end_date: Optional[datetime]
    description: Optional[str]
    responsibilities: List[str]
    order_index: int
    created_at: datetime
    updated_at: datetime
    is_current: bool

    @classmethod
    def from_entity(cls, entity) -> "WorkExperienceResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            role=entity.role,
            company=entity.company,
            start_date=entity.start_date,
            end_date=entity.end_date,
            description=entity.description,
            responsibilities=entity.responsibilities.copy(),
            order_index=entity.order_index,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_current=entity.is_current_position(),
        )


@dataclass
class WorkExperienceListResponse:
    """Response containing list of work experiences."""
    experiences: List[WorkExperienceResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "WorkExperienceListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            experiences=[WorkExperienceResponse.from_entity(e) for e in entities],
            total=len(entities),
        )