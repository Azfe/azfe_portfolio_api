"""
Delete Tool Use Case.

Deletes an existing tool.
"""

from typing import TYPE_CHECKING

from app.application.dto import DeleteToolRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, IUniqueNameRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Tool as ToolType


class DeleteToolUseCase(ICommandUseCase[DeleteToolRequest, SuccessResponse]):
    """
    Use case for deleting a tool.

    Business Rules:
    - Tool must exist
    - Deletion is permanent

    Dependencies:
    - IUniqueNameRepository[Tool]: For tool data access
    """

    def __init__(self, tool_repository: IUniqueNameRepository["ToolType"]):
        """
        Initialize use case with dependencies.

        Args:
            tool_repository: Tool repository interface
        """
        self.tool_repo = tool_repository

    async def execute(self, request: DeleteToolRequest) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete tool request with tool ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If tool doesn't exist
        """
        # Attempt to delete
        deleted = await self.tool_repo.delete(request.tool_id)

        if not deleted:
            raise NotFoundException("Tool", request.tool_id)

        return SuccessResponse(message="Tool deleted successfully")