"""
List ContactMessages Use Case.

Retrieves all contact messages.
"""

from app.application.dto import ContactMessageListResponse, ListContactMessagesRequest
from app.shared.interfaces import IContactMessageRepository, IQueryUseCase


class ListContactMessagesUseCase(
    IQueryUseCase[ListContactMessagesRequest, ContactMessageListResponse]
):
    """
    Use case for listing all contact messages.

    Business Rules:
    - Returns all contact messages
    - Default ordering: newest first (by created_at desc)

    Dependencies:
    - IContactMessageRepository: For contact message data access
    """

    def __init__(self, contact_message_repository: IContactMessageRepository):
        """
        Initialize use case with dependencies.

        Args:
            contact_message_repository: Contact message repository interface
        """
        self.message_repo = contact_message_repository

    async def execute(
        self, request: ListContactMessagesRequest
    ) -> ContactMessageListResponse:
        """
        Execute the use case.

        Args:
            request: List contact messages request

        Returns:
            ContactMessageListResponse with list of messages and metadata
        """
        # Get all messages
        messages = await self.message_repo.list_all()

        # Sort by created_at
        messages.sort(key=lambda m: m.created_at, reverse=not request.ascending)

        # Convert to DTO and return
        return ContactMessageListResponse.from_entities(messages)
