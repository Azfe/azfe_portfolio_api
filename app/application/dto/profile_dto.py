"""
Profile DTOs.

Data Transfer Objects for Profile use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateProfileRequest:
    """Request to create a profile."""

    name: str
    headline: str
    bio: str | None = None
    location: str | None = None
    avatar_url: str | None = None


@dataclass
class UpdateProfileRequest:
    """Request to update profile information."""

    name: str | None = None
    headline: str | None = None
    bio: str | None = None
    location: str | None = None
    avatar_url: str | None = None


@dataclass
class GetProfileRequest:
    """Request to get the profile (no parameters needed)."""

    pass


@dataclass
class ProfileResponse:
    """Response containing profile data."""

    id: str
    name: str
    headline: str
    bio: str | None
    location: str | None
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity) -> "ProfileResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            name=entity.name,
            headline=entity.headline,
            bio=entity.bio,
            location=entity.location,
            avatar_url=entity.avatar_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
