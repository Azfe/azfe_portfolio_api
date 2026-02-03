"""
Create Profile Use Case.

Creates the single profile in the system.
"""

from app.shared.interfaces import ICommandUseCase, IProfileRepository
from app.shared.shared_exceptions import DuplicateException
from app.application.dto import CreateProfileRequest, ProfileResponse
from app.domain.entities import Profile


class CreateProfileUseCase(ICommandUseCase[CreateProfileRequest, ProfileResponse]):
    """
    Use case for creating a profile.
    
    Business Rules:
    - Only ONE profile can exist in the system
    - All required fields must be provided
    - Avatar URL must be valid if provided
    
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

    async def execute(self, request: CreateProfileRequest) -> ProfileResponse:
        """
        Execute the use case.
        
        Args:
            request: Create profile request with profile data
            
        Returns:
            ProfileResponse with created profile data
            
        Raises:
            DuplicateException: If a profile already exists
            DomainError: If validation fails
        """
        # Check if profile already exists
        if await self.profile_repo.profile_exists():
            raise DuplicateException(
                "Profile",
                "single",
                "A profile already exists. Only one profile is allowed."
            )
        
        # Create domain entity (validates automatically)
        profile = Profile.create(
            name=request.name,
            headline=request.headline,
            bio=request.bio,
            location=request.location,
            avatar_url=request.avatar_url,
        )
        
        # Persist the profile
        created_profile = await self.profile_repo.add(profile)
        
        # Convert to DTO and return
        return ProfileResponse.from_entity(created_profile)