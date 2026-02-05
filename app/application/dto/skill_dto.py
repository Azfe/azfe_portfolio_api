"""
Skill DTOs.

Data Transfer Objects for Skill use cases.
"""

from dataclasses import dataclass


@dataclass
class AddSkillRequest:
    """Request to add a skill."""

    profile_id: str
    name: str
    category: str
    order_index: int
    level: str | None = None


@dataclass
class EditSkillRequest:
    """Request to edit a skill."""

    skill_id: str
    name: str | None = None
    category: str | None = None
    level: str | None = None


@dataclass
class DeleteSkillRequest:
    """Request to delete a skill."""

    skill_id: str


@dataclass
class ListSkillsRequest:
    """Request to list skills."""

    profile_id: str
    category: str | None = None  # Filter by category
    ascending: bool = False  # Default: newest first


@dataclass
class SkillResponse:
    """Response containing skill data."""

    id: str
    profile_id: str
    name: str
    category: str
    order_index: int
    level: str | None
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity) -> "SkillResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            name=entity.name,
            category=entity.category,
            order_index=entity.order_index,
            level=entity.level,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
        )


@dataclass
class SkillListResponse:
    """Response containing list of skills."""

    skills: list[SkillResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "SkillListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            skills=[SkillResponse.from_entity(s) for s in entities],
            total=len(entities),
        )
