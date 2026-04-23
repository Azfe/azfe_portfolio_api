"""
List AdditionalTrainings Use Case.

Retrieves all additional trainings for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import (
    AdditionalTrainingListResponse,
    ListAdditionalTrainingsRequest,
)
from app.shared.interfaces import IOrderedRepository, IQueryUseCase

if TYPE_CHECKING:
    from app.domain.entities import AdditionalTraining as AdditionalTrainingType


class ListAdditionalTrainingsUseCase(
    IQueryUseCase[ListAdditionalTrainingsRequest, AdditionalTrainingListResponse]
):
    """
    Use case for listing all additional trainings.

    Business Rules:
    - Returns all trainings for the profile
    - Ordered by orderIndex (configurable direction)

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
        self, request: ListAdditionalTrainingsRequest
    ) -> AdditionalTrainingListResponse:
        """
        Execute the use case.

        Args:
            request: List trainings request with profile ID

        Returns:
            AdditionalTrainingListResponse with list of trainings and metadata
        """
        # Get trainings
        trainings = await self.training_repo.find_by(profile_id=request.profile_id)

        # Sort by order_index
        trainings.sort(key=lambda t: t.order_index, reverse=not request.ascending)

        # Convert to DTO and return
        return AdditionalTrainingListResponse.from_entities(trainings)
