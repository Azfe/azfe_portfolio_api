"""
Delete AdditionalTraining Use Case.

Deletes an existing additional training entry.
"""

from typing import TYPE_CHECKING

from app.application.dto import DeleteAdditionalTrainingRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import AdditionalTraining as AdditionalTrainingType


class DeleteAdditionalTrainingUseCase(
    ICommandUseCase[DeleteAdditionalTrainingRequest, SuccessResponse]
):
    """
    Use case for deleting additional training.

    Business Rules:
    - Training must exist
    - Deletion is permanent

    Dependencies:
    - IOrderedRepository[AdditionalTraining]: For additional training data access
    """

    def __init__(
        self,
        additional_training_repository: IOrderedRepository["AdditionalTrainingType"],
    ):
        """
        Initialize use case with dependencies.

        Args:
            additional_training_repository: Additional training repository interface
        """
        self.training_repo = additional_training_repository

    async def execute(
        self, request: DeleteAdditionalTrainingRequest
    ) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete training request with training ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If training doesn't exist
        """
        # Attempt to delete
        deleted = await self.training_repo.delete(request.training_id)

        if not deleted:
            raise NotFoundException("AdditionalTraining", request.training_id)

        return SuccessResponse(message="Additional training deleted successfully")
