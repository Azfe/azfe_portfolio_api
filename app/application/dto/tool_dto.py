"""
Tool DTOs.

Data Transfer Objects for Tool use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddToolRequest:
    """Request to add a tool."""

    profile_id: str
    name: str
    category: str
    order_index: int
    icon_url: str | None = None


@dataclass
class EditToolRequest:
    """Request to edit a tool."""

    tool_id: str
    name: str | None = None
    category: str | None = None
    icon_url: str | None = None


@dataclass
class DeleteToolRequest:
    """Request to delete a tool."""

    tool_id: str


@dataclass
class ListToolsRequest:
    """Request to list tools."""

    profile_id: str
    category: str | None = None  # Filter by category
    ascending: bool = True  # Default: by order_index ASC


@dataclass
class ToolResponse:
    """Response containing tool data."""

    id: str
    profile_id: str
    name: str
    category: str
    order_index: int
    icon_url: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity) -> "ToolResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            name=entity.name,
            category=entity.category,
            order_index=entity.order_index,
            icon_url=entity.icon_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


@dataclass
class ToolListResponse:
    """Response containing list of tools."""

    tools: list[ToolResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "ToolListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            tools=[ToolResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
