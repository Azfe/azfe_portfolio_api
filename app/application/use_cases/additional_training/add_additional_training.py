"""
Add AdditionalTraining Use Case.

Adds a new additional training entry to the profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import AddAdditionalTrainingRequest, AdditionalTrainingResponse
from app.domain.entities import AdditionalTraining
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import BusinessRuleViolationException

if TYPE_CHECKING:
    from app.domain.entities import AdditionalTraining as AdditionalTrainingType


class AddAdditionalTrainingUseCase(
    ICommandUseCase[AddAdditionalTrainingRequest, AdditionalTrainingResponse]
):
    """
    Use case for adding additional training.

    Business Rules:
    - orderIndex must be unique per profile
    - Title and provider are required

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
        self, request: AddAdditionalTrainingRequest
    ) -> AdditionalTrainingResponse:
        """
        Execute the use case.

        Args:
            request: Add additional training request with training data

        Returns:
            AdditionalTrainingResponse with created training data

        Raises:
            BusinessRuleViolationException: If orderIndex already exists
            DomainError: If validation fails
        """
        # Check orderIndex uniqueness
        existing = await self.training_repo.get_by_order_index(
            request.profile_id, request.order_index
        )
        if existing:
            raise BusinessRuleViolationException(
                "orderIndex must be unique per profile",
                {"orderIndex": request.order_index},
            )

        # Create domain entity (validates automatically)
        training = AdditionalTraining.create(
            profile_id=request.profile_id,
            title=request.title,
            provider=request.provider,
            completion_date=request.completion_date,
            order_index=request.order_index,
            duration=request.duration,
            certificate_url=request.certificate_url,
            description=request.description,
        )

        # Persist the training
        created_training = await self.training_repo.add(training)

        # Convert to DTO and return
        return AdditionalTrainingResponse.from_entity(created_training)
