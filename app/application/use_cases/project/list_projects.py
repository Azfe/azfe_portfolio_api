"""
List Projects Use Case.

Retrieves all projects for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import ListProjectsRequest, ProjectListResponse
from app.shared.interfaces import IOrderedRepository, IQueryUseCase

if TYPE_CHECKING:
    from app.domain.entities import Project as ProjectType


class ListProjectsUseCase(IQueryUseCase[ListProjectsRequest, ProjectListResponse]):
    """
    Use case for listing all projects.

    Business Rules:
    - Returns all projects for the profile
    - Ordered by orderIndex (configurable direction)

    Dependencies:
    - IOrderedRepository[Project]: For project data access
    """

    def __init__(self, project_repository: IOrderedRepository["ProjectType"]):
        """
        Initialize use case with dependencies.

        Args:
            project_repository: Project repository interface
        """
        self.project_repo = project_repository

    async def execute(self, request: ListProjectsRequest) -> ProjectListResponse:
        """
        Execute the use case.

        Args:
            request: List projects request with profile ID

        Returns:
            ProjectListResponse with list of projects and metadata
        """
        # Get projects
        projects = await self.project_repo.find_by(profile_id=request.profile_id)

        # Sort by order_index
        projects.sort(key=lambda p: p.order_index, reverse=not request.ascending)

        # Convert to DTO and return
        return ProjectListResponse.from_entities(projects)
