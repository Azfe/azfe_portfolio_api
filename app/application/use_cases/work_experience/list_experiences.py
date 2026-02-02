"""
List Experiences Use Case.

Retrieves all work experiences for a profile, ordered by orderIndex.
"""

from app.shared.interfaces import IQueryUseCase, IOrderedRepository
from app.application.dto import ListExperiencesRequest, WorkExperienceListResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import WorkExperience as WorkExperienceType


class ListExperiencesUseCase(IQueryUseCase[ListExperiencesRequest, WorkExperienceListResponse]):
    """
    Use case for listing all work experiences.
    
    Business Rules:
    - Returns all experiences for the profile
    - Ordered by orderIndex (configurable direction)
    
    Dependencies:
    - IOrderedRepository[WorkExperience]: For experience data access
    """

    def __init__(self, experience_repository: IOrderedRepository['WorkExperienceType']):
        """
        Initialize use case with dependencies.
        
        Args:
            experience_repository: Work experience repository interface
        """
        self.experience_repo = experience_repository

    async def execute(self, request: ListExperiencesRequest) -> WorkExperienceListResponse:
        """
        Execute the use case.
        
        Args:
            request: List experiences request with profile ID and sort order
            
        Returns:
            WorkExperienceListResponse with list of experiences
        """
        # Get all experiences ordered by orderIndex
        experiences = await self.experience_repo.get_all_ordered(
            profile_id=request.profile_id,
            ascending=request.ascending
        )
        
        # Convert to DTO and return
        return WorkExperienceListResponse.from_entities(experiences)