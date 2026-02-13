"""
Language DTOs.

Data Transfer Objects for Language use cases.
"""

from dataclasses import dataclass


@dataclass
class AddLanguageRequest:
    """Request to add a language."""

    profile_id: str
    name: str
    order_index: int
    proficiency: str | None = None


@dataclass
class EditLanguageRequest:
    """Request to edit a language."""

    language_id: str
    name: str | None = None
    proficiency: str | None = None


@dataclass
class DeleteLanguageRequest:
    """Request to delete a language."""

    language_id: str


@dataclass
class ListLanguagesRequest:
    """Request to list languages."""

    profile_id: str
    ascending: bool = True


@dataclass
class LanguageResponse:
    """Response containing language data."""

    id: str
    profile_id: str
    name: str
    order_index: int
    proficiency: str | None
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity) -> "LanguageResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            name=entity.name,
            order_index=entity.order_index,
            proficiency=entity.proficiency,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
        )


@dataclass
class LanguageListResponse:
    """Response containing list of languages."""

    languages: list[LanguageResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "LanguageListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            languages=[LanguageResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
