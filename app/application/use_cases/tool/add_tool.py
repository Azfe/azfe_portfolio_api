"""
Add Tool Use Case.

Adds a new tool to the profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import AddToolRequest, ToolResponse
from app.domain.entities import Tool
from app.shared.interfaces import ICommandUseCase, IUniqueNameRepository
from app.shared.shared_exceptions import DuplicateException

if TYPE_CHECKING:
    from app.domain.entities import Tool as ToolType


class AddToolUseCase(ICommandUseCase[AddToolRequest, ToolResponse]):
    """
    Use case for adding a tool.

    Business Rules:
    - Name must be unique per profile
    - Category is required

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

    async def execute(self, request: AddToolRequest) -> ToolResponse:
        """
        Execute the use case.

        Args:
            request: Add tool request with tool data

        Returns:
            ToolResponse with created tool data

        Raises:
            DuplicateException: If tool name already exists
            DomainError: If validation fails
        """
        # Check name uniqueness
        if await self.tool_repo.exists_by_name(request.profile_id, request.name):
            raise DuplicateException("Tool", "name", request.name)

        # Create domain entity (validates automatically)
        tool = Tool.create(
            profile_id=request.profile_id,
            name=request.name,
            category=request.category,
            order_index=request.order_index,
            icon_url=request.icon_url,
        )

        # Persist the tool
        created_tool = await self.tool_repo.add(tool)

        # Convert to DTO and return
        return ToolResponse.from_entity(created_tool)
