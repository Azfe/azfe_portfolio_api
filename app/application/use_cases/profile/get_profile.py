"""
Get Profile Use Case.

Retrieves the single profile that exists in the system.
"""

from app.shared.interfaces import IQueryUseCase, IProfileRepository
from app.shared.exceptions import NotFoundException
from app.application.dto import GetProfileRequest, ProfileResponse


class GetProfileUseCase(IQueryUseCase[GetProfileRequest, ProfileResponse]):
    """
    Use case for retrieving the profile.
    
    Business Rules:
    - Only one profile exists in the system
    - Returns NotFoundException if no profile exists
    
    Dependencies:
    - IProfileRepository: For profile data access
    """

    def __init__(self, profile_repository: IProfileRepository):
        """
        Initialize use case with dependencies.
        
        Args:
            profile_repository: Profile repository interface
        """
        self.profile_repo = profile_repository

    async def execute(self, request: GetProfileRequest) -> ProfileResponse:
        """
        Execute the use case.
        
        Args:
            request: Get profile request (empty)
            
        Returns:
            ProfileResponse with profile data
            
        Raises:
            NotFoundException: If no profile exists
        """
        # Get the profile
        profile = await self.profile_repo.get_profile()
        
        # Validate profile exists
        if not profile:
            raise NotFoundException("Profile", "single")
        
        # Convert to DTO and return
        return ProfileResponse.from_entity(profile)