"""
Add Project Use Case.

Adds a new project to the profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import AddProjectRequest, ProjectResponse
from app.domain.entities import Project
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import BusinessRuleViolationException

if TYPE_CHECKING:
    from app.domain.entities import Project as ProjectType


class AddProjectUseCase(ICommandUseCase[AddProjectRequest, ProjectResponse]):
    """
    Use case for adding a project.

    Business Rules:
    - orderIndex must be unique per profile
    - Title and description are required
    - Date range must be valid

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

    async def execute(self, request: AddProjectRequest) -> ProjectResponse:
        """
        Execute the use case.

        Args:
            request: Add project request with project data

        Returns:
            ProjectResponse with created project data

        Raises:
            BusinessRuleViolationException: If orderIndex already exists
            DomainError: If validation fails
        """
        # Check orderIndex uniqueness
        existing = await self.project_repo.get_by_order_index(
            request.profile_id, request.order_index
        )
        if existing:
            raise BusinessRuleViolationException(
                "orderIndex must be unique per profile",
                {"orderIndex": request.order_index},
            )

        # Create domain entity (validates automatically)
        project = Project.create(
            profile_id=request.profile_id,
            title=request.title,
            description=request.description,
            start_date=request.start_date,
            order_index=request.order_index,
            end_date=request.end_date,
            live_url=request.live_url,
            repo_url=request.repo_url,
            technologies=request.technologies,
        )

        # Persist the project
        created_project = await self.project_repo.add(project)

        # Convert to DTO and return
        return ProjectResponse.from_entity(created_project)