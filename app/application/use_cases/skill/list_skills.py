"""
List Skills Use Case.

Retrieves all skills for a profile, optionally filtered by category.
"""

from app.shared.interfaces import IQueryUseCase, IUniqueNameRepository
from app.application.dto import ListSkillsRequest, SkillListResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import Skill as SkillType


class ListSkillsUseCase(IQueryUseCase[ListSkillsRequest, SkillListResponse]):
    """
    Use case for listing all skills.
    
    Business Rules:
    - Returns all skills for the profile
    - Optional filter by category
    - Ordered by orderIndex (configurable direction)
    
    Dependencies:
    - IUniqueNameRepository[Skill]: For skill data access
    """

    def __init__(self, skill_repository: IUniqueNameRepository['SkillType']):
        """
        Initialize use case with dependencies.
        
        Args:
            skill_repository: Skill repository interface
        """
        self.skill_repo = skill_repository

    async def execute(self, request: ListSkillsRequest) -> SkillListResponse:
        """
        Execute the use case.
        
        Args:
            request: List skills request with profile ID and optional filters
            
        Returns:
            SkillListResponse with list of skills and metadata
        """
        # Get skills (filtered by category if provided)
        if request.category:
            skills = await self.skill_repo.find_by(
                profile_id=request.profile_id,
                category=request.category
            )
        else:
            skills = await self.skill_repo.find_by(profile_id=request.profile_id)
        
        # Sort by order_index
        skills.sort(key=lambda s: s.order_index, reverse=not request.ascending)
        
        # Convert to DTO and return
        return SkillListResponse.from_entities(skills)