"""
Get ContactInformation Use Case.

Retrieves contact information for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import ContactInformationResponse, GetContactInformationRequest
from app.shared.interfaces import IQueryUseCase, IRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import ContactInformation as ContactInformationType


class GetContactInformationUseCase(
    IQueryUseCase[GetContactInformationRequest, ContactInformationResponse]
):
    """
    Use case for getting contact information.

    Business Rules:
    - Only one contact information per profile
    - Returns the contact information for the specified profile

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
        self, request: GetContactInformationRequest
    ) -> ContactInformationResponse:
        """
        Execute the use case.

        Args:
            request: Get contact information request with profile ID

        Returns:
            ContactInformationResponse with contact information data

        Raises:
            NotFoundException: If contact information doesn't exist for profile
        """
        # Find contact information for the profile
        results = await self.contact_info_repo.find_by(profile_id=request.profile_id)

        if not results:
            raise NotFoundException("ContactInformation", request.profile_id)

        # Return the first (and only) result
        return ContactInformationResponse.from_entity(results[0])