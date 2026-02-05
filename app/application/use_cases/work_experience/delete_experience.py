"""
Delete Experience Use Case.

Deletes an existing work experience.
"""

from typing import TYPE_CHECKING

from app.application.dto import DeleteExperienceRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import WorkExperience as WorkExperienceType


class DeleteExperienceUseCase(
    ICommandUseCase[DeleteExperienceRequest, SuccessResponse]
):
    """
    Use case for deleting a work experience.

    Business Rules:
    - Experience must exist
    - Deletion is permanent

    Dependencies:
    - IOrderedRepository[WorkExperience]: For experience data access
    """

    def __init__(self, experience_repository: IOrderedRepository["WorkExperienceType"]):
        """
        Initialize use case with dependencies.

        Args:
            experience_repository: Work experience repository interface
        """
        self.experience_repo = experience_repository

    async def execute(self, request: DeleteExperienceRequest) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete experience request with experience ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If experience doesn't exist
        """
        # Attempt to delete
        deleted = await self.experience_repo.delete(request.experience_id)

        if not deleted:
            raise NotFoundException("WorkExperience", request.experience_id)

        return SuccessResponse(message="Work experience deleted successfully")
