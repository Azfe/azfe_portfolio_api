"""
Edit Project Use Case.

Updates an existing project.
"""

from typing import TYPE_CHECKING

from app.application.dto import EditProjectRequest, ProjectResponse
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Project as ProjectType


class EditProjectUseCase(ICommandUseCase[EditProjectRequest, ProjectResponse]):
    """
    Use case for editing a project.

    Business Rules:
    - Project must exist
    - Only provided fields are updated
    - Validations are performed by the entity

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

    async def execute(self, request: EditProjectRequest) -> ProjectResponse:
        """
        Execute the use case.

        Args:
            request: Edit project request with fields to update

        Returns:
            ProjectResponse with updated project data

        Raises:
            NotFoundException: If project doesn't exist
            DomainError: If validation fails
        """
        # Get existing project
        project = await self.project_repo.get_by_id(request.project_id)

        if not project:
            raise NotFoundException("Project", request.project_id)

        # Update basic info (entity validates)
        project.update_info(
            title=request.title,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Update URLs if provided
        if request.live_url is not None or request.repo_url is not None:
            project.update_urls(
                live_url=request.live_url,
                repo_url=request.repo_url,
            )

        # Update technologies if provided
        if request.technologies is not None:
            project.update_technologies(request.technologies)

        # Persist changes
        updated_project = await self.project_repo.update(project)

        # Convert to DTO and return
        return ProjectResponse.from_entity(updated_project)
