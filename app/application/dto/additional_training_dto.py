"""
AdditionalTraining DTOs.

Data Transfer Objects for AdditionalTraining use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddAdditionalTrainingRequest:
    """Request to add additional training."""

    profile_id: str
    title: str
    provider: str
    completion_date: datetime
    order_index: int
    duration: str | None = None
    certificate_url: str | None = None
    description: str | None = None


@dataclass
class EditAdditionalTrainingRequest:
    """Request to edit additional training."""

    training_id: str
    title: str | None = None
    provider: str | None = None
    completion_date: datetime | None = None
    duration: str | None = None
    certificate_url: str | None = None
    description: str | None = None


@dataclass
class DeleteAdditionalTrainingRequest:
    """Request to delete additional training."""

    training_id: str


@dataclass
class ListAdditionalTrainingsRequest:
    """Request to list additional trainings."""

    profile_id: str
    ascending: bool = True  # Default: by order_index ASC


@dataclass
class AdditionalTrainingResponse:
    """Response containing additional training data."""

    id: str
    profile_id: str
    title: str
    provider: str
    completion_date: datetime
    order_index: int
    duration: str | None
    certificate_url: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity) -> "AdditionalTrainingResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            title=entity.title,
            provider=entity.provider,
            completion_date=entity.completion_date,
            order_index=entity.order_index,
            duration=entity.duration,
            certificate_url=entity.certificate_url,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


@dataclass
class AdditionalTrainingListResponse:
    """Response containing list of additional trainings."""

    trainings: list[AdditionalTrainingResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "AdditionalTrainingListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            trainings=[AdditionalTrainingResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
