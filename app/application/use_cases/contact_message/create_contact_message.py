"""
Create ContactMessage Use Case.

Creates a new contact message from a visitor.
"""

from app.application.dto import ContactMessageResponse, CreateContactMessageRequest
from app.domain.entities import ContactMessage
from app.shared.interfaces import ICommandUseCase, IContactMessageRepository


class CreateContactMessageUseCase(
    ICommandUseCase[CreateContactMessageRequest, ContactMessageResponse]
):
    """
    Use case for creating a contact message.

    Business Rules:
    - Messages are append-only
    - Name, email, and message are required
    - Status defaults to "pending"

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
        self, request: CreateContactMessageRequest
    ) -> ContactMessageResponse:
        """
        Execute the use case.

        Args:
            request: Create contact message request with message data

        Returns:
            ContactMessageResponse with created message data

        Raises:
            DomainError: If validation fails
        """
        # Create domain entity (validates automatically)
        message = ContactMessage.create(
            name=request.name,
            email=request.email,
            message=request.message,
        )

        # Persist the message
        created_message = await self.message_repo.add(message)

        # Convert to DTO and return
        return ContactMessageResponse.from_entity(created_message)
