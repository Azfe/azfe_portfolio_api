"""
Edit Tool Use Case.

Updates an existing tool.
"""

from typing import TYPE_CHECKING

from app.application.dto import EditToolRequest, ToolResponse
from app.shared.interfaces import ICommandUseCase, IUniqueNameRepository
from app.shared.shared_exceptions import DuplicateException, NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Tool as ToolType


class EditToolUseCase(ICommandUseCase[EditToolRequest, ToolResponse]):
    """
    Use case for editing a tool.

    Business Rules:
    - Tool must exist
    - Name must be unique if changed
    - Only provided fields are updated

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

    async def execute(self, request: EditToolRequest) -> ToolResponse:
        """
        Execute the use case.

        Args:
            request: Edit tool request with fields to update

        Returns:
            ToolResponse with updated tool data

        Raises:
            NotFoundException: If tool doesn't exist
            DuplicateException: If new name already exists
            DomainError: If validation fails
        """
        # Get existing tool
        tool = await self.tool_repo.get_by_id(request.tool_id)

        if not tool:
            raise NotFoundException("Tool", request.tool_id)

        # Check name uniqueness if changing name
        if (
            request.name
            and request.name != tool.name
            and await self.tool_repo.exists_by_name(tool.profile_id, request.name)
        ):
            raise DuplicateException("Tool", "name", request.name)

        # Update info (entity validates)
        tool.update_info(
            name=request.name,
            category=request.category,
            icon_url=request.icon_url,
        )

        # Persist changes
        updated_tool = await self.tool_repo.update(tool)

        # Convert to DTO and return
        return ToolResponse.from_entity(updated_tool)
