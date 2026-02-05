"""
Add Experience Use Case.

Adds a new work experience to the profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import AddExperienceRequest, WorkExperienceResponse
from app.domain.entities import WorkExperience
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import BusinessRuleViolationException

if TYPE_CHECKING:
    from app.domain.entities import WorkExperience as WorkExperienceType


class AddExperienceUseCase(
    ICommandUseCase[AddExperienceRequest, WorkExperienceResponse]
):
    """
    Use case for adding a work experience.

    Business Rules:
    - orderIndex must be unique per profile
    - All required fields must be provided
    - Date range must be valid

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

    async def execute(self, request: AddExperienceRequest) -> WorkExperienceResponse:
        """
        Execute the use case.

        Args:
            request: Add experience request with experience data

        Returns:
            WorkExperienceResponse with created experience data

        Raises:
            BusinessRuleViolationException: If orderIndex already exists
            DomainError: If validation fails
        """
        # Check if orderIndex is already used
        existing = await self.experience_repo.get_by_order_index(
            request.profile_id, request.order_index
        )
        if existing:
            raise BusinessRuleViolationException(
                "orderIndex must be unique per profile",
                {"orderIndex": request.order_index},
            )

        # Create domain entity (validates automatically)
        experience = WorkExperience.create(
            profile_id=request.profile_id,
            role=request.role,
            company=request.company,
            start_date=request.start_date,
            order_index=request.order_index,
            description=request.description,
            end_date=request.end_date,
            responsibilities=request.responsibilities,
        )

        # Persist the experience
        created_experience = await self.experience_repo.add(experience)

        # Convert to DTO and return
        return WorkExperienceResponse.from_entity(created_experience)
