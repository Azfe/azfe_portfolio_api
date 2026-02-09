"""
ProgrammingLanguage DTOs.

Data Transfer Objects for ProgrammingLanguage use cases.
"""

from dataclasses import dataclass


@dataclass
class AddProgrammingLanguageRequest:
    """Request to add a programming language."""

    profile_id: str
    name: str
    order_index: int
    level: str | None = None


@dataclass
class EditProgrammingLanguageRequest:
    """Request to edit a programming language."""

    programming_language_id: str
    name: str | None = None
    level: str | None = None


@dataclass
class DeleteProgrammingLanguageRequest:
    """Request to delete a programming language."""

    programming_language_id: str


@dataclass
class ListProgrammingLanguagesRequest:
    """Request to list programming languages."""

    profile_id: str
    ascending: bool = True


@dataclass
class ProgrammingLanguageResponse:
    """Response containing programming language data."""

    id: str
    profile_id: str
    name: str
    order_index: int
    level: str | None
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity) -> "ProgrammingLanguageResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            name=entity.name,
            order_index=entity.order_index,
            level=entity.level,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
        )


@dataclass
class ProgrammingLanguageListResponse:
    """Response containing list of programming languages."""

    programming_languages: list[ProgrammingLanguageResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "ProgrammingLanguageListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            programming_languages=[
                ProgrammingLanguageResponse.from_entity(e) for e in entities
            ],
            total=len(entities),
        )
