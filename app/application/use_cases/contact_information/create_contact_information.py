"""
Create ContactInformation Use Case.

Creates contact information for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import (
    ContactInformationResponse,
    CreateContactInformationRequest,
)
from app.domain.entities import ContactInformation
from app.shared.interfaces import ICommandUseCase, IRepository
from app.shared.shared_exceptions import DuplicateException

if TYPE_CHECKING:
    from app.domain.entities import ContactInformation as ContactInformationType


class CreateContactInformationUseCase(
    ICommandUseCase[CreateContactInformationRequest, ContactInformationResponse]
):
    """
    Use case for creating contact information.

    Business Rules:
    - Only one contact information per profile
    - Email is required

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
        self, request: CreateContactInformationRequest
    ) -> ContactInformationResponse:
        """
        Execute the use case.

        Args:
            request: Create contact information request with data

        Returns:
            ContactInformationResponse with created contact information data

        Raises:
            DuplicateException: If contact information already exists for profile
            DomainError: If validation fails
        """
        # Check if contact information already exists for profile
        existing = await self.contact_info_repo.find_by(profile_id=request.profile_id)
        if existing:
            raise DuplicateException(
                "ContactInformation", "profile_id", request.profile_id
            )

        # Create domain entity (validates automatically)
        contact_info = ContactInformation.create(
            profile_id=request.profile_id,
            email=request.email,
            phone=request.phone,
            linkedin=request.linkedin,
            github=request.github,
            website=request.website,
        )

        # Persist the contact information
        created_info = await self.contact_info_repo.add(contact_info)

        # Convert to DTO and return
        return ContactInformationResponse.from_entity(created_info)