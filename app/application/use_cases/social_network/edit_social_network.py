"""
Edit SocialNetwork Use Case.

Updates an existing social network.
"""

from typing import TYPE_CHECKING

from app.application.dto import EditSocialNetworkRequest, SocialNetworkResponse
from app.shared.interfaces import ICommandUseCase, ISocialNetworkRepository
from app.shared.shared_exceptions import DuplicateException, NotFoundException

if TYPE_CHECKING:
    pass


class EditSocialNetworkUseCase(
    ICommandUseCase[EditSocialNetworkRequest, SocialNetworkResponse]
):
    """
    Use case for editing a social network.

    Business Rules:
    - Social network must exist
    - Platform must be unique if changed
    - Only provided fields are updated

    Dependencies:
    - ISocialNetworkRepository: For social network data access
    """

    def __init__(self, social_network_repository: ISocialNetworkRepository):
        """
        Initialize use case with dependencies.

        Args:
            social_network_repository: Social network repository interface
        """
        self.social_network_repo = social_network_repository

    async def execute(self, request: EditSocialNetworkRequest) -> SocialNetworkResponse:
        """
        Execute the use case.

        Args:
            request: Edit social network request with fields to update

        Returns:
            SocialNetworkResponse with updated social network data

        Raises:
            NotFoundException: If social network doesn't exist
            DuplicateException: If new platform already exists
            DomainError: If validation fails
        """
        # Get existing social network
        social_network = await self.social_network_repo.get_by_id(
            request.social_network_id
        )

        if not social_network:
            raise NotFoundException("SocialNetwork", request.social_network_id)

        # Check platform uniqueness if changing platform
        if (
            request.platform
            and request.platform != social_network.platform
            and await self.social_network_repo.exists_by_platform(
                social_network.profile_id, request.platform
            )
        ):
            raise DuplicateException("SocialNetwork", "platform", request.platform)

        # Update info (entity validates)
        social_network.update_info(
            platform=request.platform,
            url=request.url,
            username=request.username,
        )

        # Persist changes
        updated = await self.social_network_repo.update(social_network)

        # Convert to DTO and return
        return SocialNetworkResponse.from_entity(updated)
