"""
Delete ContactInformation Use Case.

Deletes contact information for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import DeleteContactInformationRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, IRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import ContactInformation as ContactInformationType


class DeleteContactInformationUseCase(
    ICommandUseCase[DeleteContactInformationRequest, SuccessResponse]
):
    """
    Use case for deleting contact information.

    Business Rules:
    - Contact information must exist for the profile
    - Deletion is permanent

    Dependencies:
    - IRepository[ContactInformation]: For contact information data access
    """

    def __init__(
        self,
        contact_information_repository: IRepository["ContactInformationType"],
    ):
        """
        Initialize use case with dependencies.

        Args:
            contact_information_repository: Contact information repository interface
        """
        self.contact_info_repo = contact_information_repository

    async def execute(
        self, request: DeleteContactInformationRequest
    ) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete contact information request with profile ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If contact information doesn't exist for profile
        """
        # Find existing contact information
        results = await self.contact_info_repo.find_by(profile_id=request.profile_id)

        if not results:
            raise NotFoundException("ContactInformation", request.profile_id)

        # Delete
        await self.contact_info_repo.delete(results[0].id)

        return SuccessResponse(message="Contact information deleted successfully")
