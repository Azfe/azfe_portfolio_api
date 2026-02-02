"""
Profile DTOs.

Data Transfer Objects for Profile use cases.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateProfileRequest:
    """Request to create a profile."""
    name: str
    headline: str
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None


@dataclass
class UpdateProfileRequest:
    """Request to update profile information."""
    name: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None


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
    bio: Optional[str]
    location: Optional[str]
    avatar_url: Optional[str]
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