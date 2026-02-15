"""
Delete SocialNetwork Use Case.

Deletes an existing social network.
"""

from app.application.dto import DeleteSocialNetworkRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, ISocialNetworkRepository
from app.shared.shared_exceptions import NotFoundException


class DeleteSocialNetworkUseCase(
    ICommandUseCase[DeleteSocialNetworkRequest, SuccessResponse]
):
    """
    Use case for deleting a social network.

    Business Rules:
    - Social network must exist
    - Deletion is permanent

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

    async def execute(self, request: DeleteSocialNetworkRequest) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete social network request with social network ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If social network doesn't exist
        """
        # Attempt to delete
        deleted = await self.social_network_repo.delete(request.social_network_id)

        if not deleted:
            raise NotFoundException("SocialNetwork", request.social_network_id)

        return SuccessResponse(message="Social network deleted successfully")