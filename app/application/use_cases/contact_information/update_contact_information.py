"""
Update ContactInformation Use Case.

Updates existing contact information for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import (
    ContactInformationResponse,
    UpdateContactInformationRequest,
)
from app.shared.interfaces import ICommandUseCase, IRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import ContactInformation as ContactInformationType


class UpdateContactInformationUseCase(
    ICommandUseCase[UpdateContactInformationRequest, ContactInformationResponse]
):
    """
    Use case for updating contact information.

    Business Rules:
    - Contact information must exist for the profile
    - Only provided fields are updated

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
        self, request: UpdateContactInformationRequest
    ) -> ContactInformationResponse:
        """
        Execute the use case.

        Args:
            request: Update contact information request with fields to update

        Returns:
            ContactInformationResponse with updated contact information data

        Raises:
            NotFoundException: If contact information doesn't exist for profile
            DomainError: If validation fails
        """
        # Find existing contact information
        results = await self.contact_info_repo.find_by(profile_id=request.profile_id)

        if not results:
            raise NotFoundException("ContactInformation", request.profile_id)

        contact_info = results[0]

        # Update email if provided
        if request.email is not None:
            contact_info.update_email(request.email)

        # Update phone if provided
        if request.phone is not None:
            contact_info.update_phone(request.phone)

        # Update social links if any provided
        if any(
            v is not None for v in [request.linkedin, request.github, request.website]
        ):
            contact_info.update_social_links(
                linkedin=request.linkedin,
                github=request.github,
                website=request.website,
            )

        # Persist changes
        updated_info = await self.contact_info_repo.update(contact_info)

        # Convert to DTO and return
        return ContactInformationResponse.from_entity(updated_info)
