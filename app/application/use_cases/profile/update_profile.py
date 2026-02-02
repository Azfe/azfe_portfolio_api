"""
Update Profile Use Case.

Updates the existing profile with new data.
"""

from app.shared.interfaces import ICommandUseCase, IProfileRepository
from app.shared.exceptions import NotFoundException
from app.application.dto import UpdateProfileRequest, ProfileResponse


class UpdateProfileUseCase(ICommandUseCase[UpdateProfileRequest, ProfileResponse]):
    """
    Use case for updating profile information.
    
    Business Rules:
    - Profile must exist
    - Only provided fields are updated (partial update)
    - Validations are performed by the entity
    
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

    async def execute(self, request: UpdateProfileRequest) -> ProfileResponse:
        """
        Execute the use case.
        
        Args:
            request: Update profile request with fields to update
            
        Returns:
            ProfileResponse with updated profile data
            
        Raises:
            NotFoundException: If profile doesn't exist
            DomainError: If validation fails
        """
        # Get existing profile
        profile = await self.profile_repo.get_profile()
        
        if not profile:
            raise NotFoundException("Profile", "single")
        
        # Update basic info (entity validates)
        profile.update_basic_info(
            name=request.name,
            headline=request.headline,
            bio=request.bio,
            location=request.location,
        )
        
        # Update avatar if provided
        if request.avatar_url is not None:
            profile.update_avatar(request.avatar_url)
        
        # Persist changes
        updated_profile = await self.profile_repo.update(profile)
        
        # Convert to DTO and return
        return ProfileResponse.from_entity(updated_profile)