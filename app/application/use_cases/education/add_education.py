"""
Add Education Use Case.

Adds a new education entry to the profile.
"""

from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import BusinessRuleViolationException
from app.application.dto import AddEducationRequest, EducationResponse
from app.domain.entities import Education
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import Education as EducationType


class AddEducationUseCase(ICommandUseCase[AddEducationRequest, EducationResponse]):
    """
    Use case for adding education.
    
    Business Rules:
    - orderIndex must be unique per profile
    - All required fields must be provided
    - Date range must be valid
    
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

    async def execute(self, request: AddEducationRequest) -> EducationResponse:
        """
        Execute the use case.
        
        Args:
            request: Add education request with education data
            
        Returns:
            EducationResponse with created education data
            
        Raises:
            BusinessRuleViolationException: If orderIndex already exists
            DomainError: If validation fails
        """
        # Check orderIndex uniqueness
        existing = await self.education_repo.get_by_order_index(
            request.profile_id,
            request.order_index
        )
        if existing:
            raise BusinessRuleViolationException(
                "orderIndex must be unique per profile",
                {"orderIndex": request.order_index}
            )
        
        # Create domain entity (validates automatically)
        education = Education.create(
            profile_id=request.profile_id,
            institution=request.institution,
            degree=request.degree,
            field=request.field,
            start_date=request.start_date,
            order_index=request.order_index,
            description=request.description,
            end_date=request.end_date,
        )
        
        # Persist the education
        created_education = await self.education_repo.add(education)
        
        # Convert to DTO and return
        return EducationResponse.from_entity(created_education)