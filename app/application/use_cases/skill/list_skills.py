"""
List Skills Use Case.

Retrieves all skills for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import ListSkillsRequest, SkillListResponse
from app.shared.interfaces import IQueryUseCase, IUniqueNameRepository

if TYPE_CHECKING:
    from app.domain.entities import Skill as SkillType


class ListSkillsUseCase(IQueryUseCase[ListSkillsRequest, SkillListResponse]):
    """
    Use case for listing all skills.

    Business Rules:
    - Returns all skills for the profile
    - Ordered by orderIndex (configurable direction)

    Dependencies:
    - IUniqueNameRepository[Skill]: For skill data access
    """

    def __init__(self, skill_repository: IUniqueNameRepository["SkillType"]):
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
            request: List skills request with profile ID

        Returns:
            SkillListResponse with list of skills and metadata
        """
        skills = await self.skill_repo.find_by(profile_id=request.profile_id)

        # Sort by order_index
        skills.sort(key=lambda s: s.order_index, reverse=not request.ascending)

        # Convert to DTO and return
        return SkillListResponse.from_entities(skills)
