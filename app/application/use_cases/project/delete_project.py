"""
Delete Project Use Case.

Deletes an existing project.
"""

from typing import TYPE_CHECKING

from app.application.dto import DeleteProjectRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Project as ProjectType


class DeleteProjectUseCase(ICommandUseCase[DeleteProjectRequest, SuccessResponse]):
    """
    Use case for deleting a project.

    Business Rules:
    - Project must exist
    - Deletion is permanent

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

    async def execute(self, request: DeleteProjectRequest) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete project request with project ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If project doesn't exist
        """
        # Attempt to delete
        deleted = await self.project_repo.delete(request.project_id)

        if not deleted:
            raise NotFoundException("Project", request.project_id)

        return SuccessResponse(message="Project deleted successfully")
