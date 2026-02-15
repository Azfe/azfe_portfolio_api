"""
Delete ContactMessage Use Case.

Deletes an existing contact message.
"""

from app.application.dto import DeleteContactMessageRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, IContactMessageRepository
from app.shared.shared_exceptions import NotFoundException


class DeleteContactMessageUseCase(
    ICommandUseCase[DeleteContactMessageRequest, SuccessResponse]
):
    """
    Use case for deleting a contact message.

    Business Rules:
    - Message must exist
    - Deletion is permanent

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

    async def execute(self, request: DeleteContactMessageRequest) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete contact message request with message ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If message doesn't exist
        """
        # Attempt to delete
        deleted = await self.message_repo.delete(request.message_id)

        if not deleted:
            raise NotFoundException("ContactMessage", request.message_id)

        return SuccessResponse(message="Contact message deleted successfully")