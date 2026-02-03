"""
Edit Education Use Case.

Updates an existing education entry.
"""

from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException
from app.application.dto import EditEducationRequest, EducationResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import Education as EducationType


class EditEducationUseCase(ICommandUseCase[EditEducationRequest, EducationResponse]):
    """
    Use case for editing education.
    
    Business Rules:
    - Education must exist
    - Only provided fields are updated
    - Validations are performed by the entity
    
    Dependencies:
    - IOrderedRepository[Education]: For education data access
    """

    def __init__(self, education_repository: IOrderedRepository['EducationType']):
        """
        Initialize use case with dependencies.
        
        Args:
            education_repository: Education repository interface
        """
        self.education_repo = education_repository

    async def execute(self, request: EditEducationRequest) -> EducationResponse:
        """
        Execute the use case.
        
        Args:
            request: Edit education request with fields to update
            
        Returns:
            EducationResponse with updated education data
            
        Raises:
            NotFoundException: If education doesn't exist
            DomainError: If validation fails
        """
        # Get existing education
        education = await self.education_repo.get_by_id(request.education_id)
        
        if not education:
            raise NotFoundException("Education", request.education_id)
        
        # Update info (entity validates)
        education.update_info(
            institution=request.institution,
            degree=request.degree,
            field=request.field,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        
        # Persist changes
        updated_education = await self.education_repo.update(education)
        
        # Convert to DTO and return
        return EducationResponse.from_entity(updated_education)