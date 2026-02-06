"""
Edit Experience Use Case.

Updates an existing work experience.
"""

from typing import TYPE_CHECKING

from app.application.dto import EditExperienceRequest, WorkExperienceResponse
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import WorkExperience as WorkExperienceType


class EditExperienceUseCase(
    ICommandUseCase[EditExperienceRequest, WorkExperienceResponse]
):
    """
    Use case for editing a work experience.

    Business Rules:
    - Experience must exist
    - Only provided fields are updated
    - Validations are performed by the entity

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

    async def execute(self, request: EditExperienceRequest) -> WorkExperienceResponse:
        """
        Execute the use case.

        Args:
            request: Edit experience request with fields to update

        Returns:
            WorkExperienceResponse with updated experience data

        Raises:
            NotFoundException: If experience doesn't exist
            DomainError: If validation fails
        """
        # Get existing experience
        experience = await self.experience_repo.get_by_id(request.experience_id)

        if not experience:
            raise NotFoundException("WorkExperience", request.experience_id)

        # Update info (entity validates)
        experience.update_info(
            role=request.role,
            company=request.company,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
        )

        # Update responsibilities if provided
        if request.responsibilities is not None:
            experience.update_responsibilities(request.responsibilities)

        # Persist changes
        updated_experience = await self.experience_repo.update(experience)

        # Convert to DTO and return
        return WorkExperienceResponse.from_entity(updated_experience)
