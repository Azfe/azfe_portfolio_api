"""
Project DTOs.

Data Transfer Objects for Project use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddProjectRequest:
    """Request to add a project."""

    profile_id: str
    title: str
    description: str
    start_date: datetime
    order_index: int
    end_date: datetime | None = None
    live_url: str | None = None
    repo_url: str | None = None
    technologies: list[str] | None = None


@dataclass
class EditProjectRequest:
    """Request to edit a project."""

    project_id: str
    title: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    live_url: str | None = None
    repo_url: str | None = None
    technologies: list[str] | None = None


@dataclass
class DeleteProjectRequest:
    """Request to delete a project."""

    project_id: str


@dataclass
class ListProjectsRequest:
    """Request to list projects."""

    profile_id: str
    ascending: bool = True  # Default: by order_index ASC


@dataclass
class ProjectResponse:
    """Response containing project data."""

    id: str
    profile_id: str
    title: str
    description: str
    start_date: datetime
    order_index: int
    end_date: datetime | None
    live_url: str | None
    repo_url: str | None
    technologies: list[str]
    created_at: datetime
    updated_at: datetime
    is_ongoing: bool

    @classmethod
    def from_entity(cls, entity) -> "ProjectResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            title=entity.title,
            description=entity.description,
            start_date=entity.start_date,
            order_index=entity.order_index,
            end_date=entity.end_date,
            live_url=entity.live_url,
            repo_url=entity.repo_url,
            technologies=entity.technologies,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_ongoing=entity.is_ongoing(),
        )


@dataclass
class ProjectListResponse:
    """Response containing list of projects."""

    projects: list[ProjectResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "ProjectListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            projects=[ProjectResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
