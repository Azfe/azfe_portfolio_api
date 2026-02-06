"""
Delete Skill Use Case.

Deletes an existing skill.
"""

from typing import TYPE_CHECKING

from app.application.dto import DeleteSkillRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, IUniqueNameRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Skill as SkillType


class DeleteSkillUseCase(ICommandUseCase[DeleteSkillRequest, SuccessResponse]):
    """
    Use case for deleting a skill.

    Business Rules:
    - Skill must exist
    - Deletion is permanent

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

    async def execute(self, request: DeleteSkillRequest) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete skill request with skill ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If skill doesn't exist
        """
        # Attempt to delete
        deleted = await self.skill_repo.delete(request.skill_id)

        if not deleted:
            raise NotFoundException("Skill", request.skill_id)

        return SuccessResponse(message="Skill deleted successfully")
