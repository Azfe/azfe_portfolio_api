"""
Delete Education Use Case.

Deletes an existing education entry.
"""

from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.exceptions import NotFoundException
from app.application.dto import DeleteEducationRequest, SuccessResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import Education as EducationType


class DeleteEducationUseCase(ICommandUseCase[DeleteEducationRequest, SuccessResponse]):
    """
    Use case for deleting education.
    
    Business Rules:
    - Education must exist
    - Deletion is permanent
    
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

    async def execute(self, request: DeleteEducationRequest) -> SuccessResponse:
        """
        Execute the use case.
        
        Args:
            request: Delete education request with education ID
            
        Returns:
            SuccessResponse confirming deletion
            
        Raises:
            NotFoundException: If education doesn't exist
        """
        # Attempt to delete
        deleted = await self.education_repo.delete(request.education_id)
        
        if not deleted:
            raise NotFoundException("Education", request.education_id)
        
        return SuccessResponse(message="Education deleted successfully")