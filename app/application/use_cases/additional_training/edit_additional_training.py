"""
Edit AdditionalTraining Use Case.

Updates an existing additional training entry.
"""

from typing import TYPE_CHECKING

from app.application.dto import AdditionalTrainingResponse, EditAdditionalTrainingRequest
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import AdditionalTraining as AdditionalTrainingType


class EditAdditionalTrainingUseCase(
    ICommandUseCase[EditAdditionalTrainingRequest, AdditionalTrainingResponse]
):
    """
    Use case for editing additional training.

    Business Rules:
    - Training must exist
    - Only provided fields are updated
    - Validations are performed by the entity

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
        self, request: EditAdditionalTrainingRequest
    ) -> AdditionalTrainingResponse:
        """
        Execute the use case.

        Args:
            request: Edit training request with fields to update

        Returns:
            AdditionalTrainingResponse with updated training data

        Raises:
            NotFoundException: If training doesn't exist
            DomainError: If validation fails
        """
        # Get existing training
        training = await self.training_repo.get_by_id(request.training_id)

        if not training:
            raise NotFoundException("AdditionalTraining", request.training_id)

        # Update info (entity validates)
        training.update_info(
            title=request.title,
            provider=request.provider,
            completion_date=request.completion_date,
            duration=request.duration,
            certificate_url=request.certificate_url,
            description=request.description,
        )

        # Persist changes
        updated_training = await self.training_repo.update(training)

        # Convert to DTO and return
        return AdditionalTrainingResponse.from_entity(updated_training)