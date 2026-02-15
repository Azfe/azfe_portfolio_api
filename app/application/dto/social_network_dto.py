"""
SocialNetwork DTOs.

Data Transfer Objects for SocialNetwork use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddSocialNetworkRequest:
    """Request to add a social network."""

    profile_id: str
    platform: str
    url: str
    order_index: int
    username: str | None = None


@dataclass
class EditSocialNetworkRequest:
    """Request to edit a social network."""

    social_network_id: str
    platform: str | None = None
    url: str | None = None
    username: str | None = None


@dataclass
class DeleteSocialNetworkRequest:
    """Request to delete a social network."""

    social_network_id: str


@dataclass
class ListSocialNetworksRequest:
    """Request to list social networks."""

    profile_id: str
    ascending: bool = True  # Default: by order_index ASC


@dataclass
class SocialNetworkResponse:
    """Response containing social network data."""

    id: str
    profile_id: str
    platform: str
    url: str
    order_index: int
    username: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity) -> "SocialNetworkResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            platform=entity.platform,
            url=entity.url,
            order_index=entity.order_index,
            username=entity.username,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


@dataclass
class SocialNetworkListResponse:
    """Response containing list of social networks."""

    social_networks: list[SocialNetworkResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "SocialNetworkListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            social_networks=[SocialNetworkResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
