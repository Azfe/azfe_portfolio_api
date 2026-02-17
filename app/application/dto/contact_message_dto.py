"""
ContactMessage DTOs.

Data Transfer Objects for ContactMessage use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateContactMessageRequest:
    """Request to create a contact message."""

    name: str
    email: str
    message: str


@dataclass
class ListContactMessagesRequest:
    """Request to list contact messages."""

    ascending: bool = False  # Default: newest first


@dataclass
class DeleteContactMessageRequest:
    """Request to delete a contact message."""

    message_id: str


@dataclass
class ContactMessageResponse:
    """Response containing contact message data."""

    id: str
    name: str
    email: str
    message: str
    status: str
    created_at: datetime
    read_at: datetime | None
    replied_at: datetime | None

    @classmethod
    def from_entity(cls, entity) -> "ContactMessageResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            message=entity.message,
            status=entity.status,
            created_at=entity.created_at,
            read_at=entity.read_at,
            replied_at=entity.replied_at,
        )


@dataclass
class ContactMessageListResponse:
    """Response containing list of contact messages."""

    messages: list[ContactMessageResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "ContactMessageListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            messages=[ContactMessageResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
