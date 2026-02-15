"""
List Tools Use Case.

Retrieves all tools for a profile, optionally filtered by category.
"""

from typing import TYPE_CHECKING

from app.application.dto import ListToolsRequest, ToolListResponse
from app.shared.interfaces import IQueryUseCase, IUniqueNameRepository

if TYPE_CHECKING:
    from app.domain.entities import Tool as ToolType


class ListToolsUseCase(IQueryUseCase[ListToolsRequest, ToolListResponse]):
    """
    Use case for listing all tools.

    Business Rules:
    - Returns all tools for the profile
    - Optional filter by category
    - Ordered by orderIndex (configurable direction)

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

    async def execute(self, request: ListToolsRequest) -> ToolListResponse:
        """
        Execute the use case.

        Args:
            request: List tools request with profile ID and optional filters

        Returns:
            ToolListResponse with list of tools and metadata
        """
        # Get tools (filtered by category if provided)
        if request.category:
            tools = await self.tool_repo.find_by(
                profile_id=request.profile_id, category=request.category
            )
        else:
            tools = await self.tool_repo.find_by(profile_id=request.profile_id)

        # Sort by order_index
        tools.sort(key=lambda t: t.order_index, reverse=not request.ascending)

        # Convert to DTO and return
        return ToolListResponse.from_entities(tools)
