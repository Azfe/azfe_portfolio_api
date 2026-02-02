"""
Edit Skill Use Case.

Updates an existing skill.
"""

from app.shared.interfaces import ICommandUseCase, IUniqueNameRepository
from app.shared.exceptions import DuplicateException, NotFoundException
from app.application.dto import EditSkillRequest, SkillResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import Skill as SkillType


class EditSkillUseCase(ICommandUseCase[EditSkillRequest, SkillResponse]):
    """
    Use case for editing a skill.
    
    Business Rules:
    - Skill must exist
    - Name must be unique if changed
    - Only provided fields are updated
    - Validations are performed by the entity
    
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

    async def execute(self, request: EditSkillRequest) -> SkillResponse:
        """
        Execute the use case.
        
        Args:
            request: Edit skill request with fields to update
            
        Returns:
            SkillResponse with updated skill data
            
        Raises:
            NotFoundException: If skill doesn't exist
            DuplicateException: If new name already exists
            DomainError: If validation fails
        """
        # Get existing skill
        skill = await self.skill_repo.get_by_id(request.skill_id)
        
        if not skill:
            raise NotFoundException("Skill", request.skill_id)
        
        # Check name uniqueness if changing name
        if request.name and request.name != skill.name:
            if await self.skill_repo.exists_by_name(skill.profile_id, request.name):
                raise DuplicateException("Skill", "name", request.name)
        
        # Update info (entity validates)
        skill.update_info(
            name=request.name,
            category=request.category,
            level=request.level,
        )
        
        # Persist changes
        updated_skill = await self.skill_repo.update(skill)
        
        # Convert to DTO and return
        return SkillResponse.from_entity(updated_skill)