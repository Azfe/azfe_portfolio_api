"""
Add Skill Use Case.

Adds a new skill to the profile.
"""

from app.shared.interfaces import ICommandUseCase, IUniqueNameRepository
from app.shared.shared_exceptions import DuplicateException
from app.application.dto import AddSkillRequest, SkillResponse
from app.domain.entities import Skill
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import Skill as SkillType


class AddSkillUseCase(ICommandUseCase[AddSkillRequest, SkillResponse]):
    """
    Use case for adding a skill.
    
    Business Rules:
    - Name must be unique per profile
    - orderIndex must be unique per profile
    - Category is required
    - Level is optional
    
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

    async def execute(self, request: AddSkillRequest) -> SkillResponse:
        """
        Execute the use case.
        
        Args:
            request: Add skill request with skill data
            
        Returns:
            SkillResponse with created skill data
            
        Raises:
            DuplicateException: If skill name already exists
            DomainError: If validation fails
        """
        # Check name uniqueness
        if await self.skill_repo.exists_by_name(request.profile_id, request.name):
            raise DuplicateException("Skill", "name", request.name)
        
        # Create domain entity (validates automatically)
        skill = Skill.create(
            profile_id=request.profile_id,
            name=request.name,
            category=request.category,
            order_index=request.order_index,
            level=request.level,
        )
        
        # Persist the skill
        created_skill = await self.skill_repo.add(skill)
        
        # Convert to DTO and return
        return SkillResponse.from_entity(created_skill)