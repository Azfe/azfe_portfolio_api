"""
List SocialNetworks Use Case.

Retrieves all social networks for a profile.
"""

from app.application.dto import ListSocialNetworksRequest, SocialNetworkListResponse
from app.shared.interfaces import IQueryUseCase, ISocialNetworkRepository


class ListSocialNetworksUseCase(
    IQueryUseCase[ListSocialNetworksRequest, SocialNetworkListResponse]
):
    """
    Use case for listing all social networks.

    Business Rules:
    - Returns all social networks for the profile
    - Ordered by orderIndex (configurable direction)

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
        self, request: ListSocialNetworksRequest
    ) -> SocialNetworkListResponse:
        """
        Execute the use case.

        Args:
            request: List social networks request with profile ID

        Returns:
            SocialNetworkListResponse with list of social networks and metadata
        """
        # Get social networks
        social_networks = await self.social_network_repo.find_by(
            profile_id=request.profile_id
        )

        # Sort by order_index
        social_networks.sort(
            key=lambda sn: sn.order_index, reverse=not request.ascending
        )

        # Convert to DTO and return
        return SocialNetworkListResponse.from_entities(social_networks)
