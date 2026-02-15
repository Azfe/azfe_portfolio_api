"""
Add SocialNetwork Use Case.

Adds a new social network to the profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import AddSocialNetworkRequest, SocialNetworkResponse
from app.domain.entities import SocialNetwork
from app.shared.interfaces import ICommandUseCase, ISocialNetworkRepository
from app.shared.shared_exceptions import DuplicateException

if TYPE_CHECKING:
    pass


class AddSocialNetworkUseCase(
    ICommandUseCase[AddSocialNetworkRequest, SocialNetworkResponse]
):
    """
    Use case for adding a social network.

    Business Rules:
    - Platform must be unique per profile
    - URL is required and must be valid

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

    async def execute(
        self, request: AddSocialNetworkRequest
    ) -> SocialNetworkResponse:
        """
        Execute the use case.

        Args:
            request: Add social network request with data

        Returns:
            SocialNetworkResponse with created social network data

        Raises:
            DuplicateException: If platform already exists for profile
            DomainError: If validation fails
        """
        # Check platform uniqueness
        if await self.social_network_repo.exists_by_platform(
            request.profile_id, request.platform
        ):
            raise DuplicateException("SocialNetwork", "platform", request.platform)

        # Create domain entity (validates automatically)
        social_network = SocialNetwork.create(
            profile_id=request.profile_id,
            platform=request.platform,
            url=request.url,
            order_index=request.order_index,
            username=request.username,
        )

        # Persist the social network
        created = await self.social_network_repo.add(social_network)

        # Convert to DTO and return
        return SocialNetworkResponse.from_entity(created)