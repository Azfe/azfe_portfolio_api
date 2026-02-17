"""
ContactInformation DTOs.

Data Transfer Objects for ContactInformation use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetContactInformationRequest:
    """Request to get contact information."""

    profile_id: str


@dataclass
class CreateContactInformationRequest:
    """Request to create contact information."""

    profile_id: str
    email: str
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    website: str | None = None


@dataclass
class UpdateContactInformationRequest:
    """Request to update contact information."""

    profile_id: str
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    website: str | None = None


@dataclass
class DeleteContactInformationRequest:
    """Request to delete contact information."""

    profile_id: str


@dataclass
class ContactInformationResponse:
    """Response containing contact information data."""

    id: str
    profile_id: str
    email: str
    phone: str | None
    linkedin: str | None
    github: str | None
    website: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity) -> "ContactInformationResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            email=entity.email,
            phone=entity.phone,
            linkedin=entity.linkedin,
            github=entity.github,
            website=entity.website,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
