"""
Get Complete CV Use Case.

Aggregates all CV data from multiple sources.
"""

from app.shared.interfaces import (
    IQueryUseCase,
    IProfileRepository,
    IOrderedRepository,
    IUniqueNameRepository
)
from app.shared.shared_exceptions import NotFoundException
from app.application.dto import GetCompleteCVRequest, CompleteCVResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities import (
        WorkExperience as WorkExperienceType,
        Skill as SkillType,
        Education as EducationType,
    )


class GetCompleteCVUseCase(IQueryUseCase[GetCompleteCVRequest, CompleteCVResponse]):
    """
    Use case for retrieving the complete CV.
    
    Aggregates data from multiple sources:
    - Profile
    - Work Experiences
    - Skills
    - Education
    
    Business Rules:
    - Profile must exist
    - All lists are ordered appropriately
    - Empty lists are returned if no data exists
    
    Dependencies:
    - IProfileRepository: For profile data
    - IOrderedRepository[WorkExperience]: For experiences
    - IUniqueNameRepository[Skill]: For skills
    - IOrderedRepository[Education]: For education
    """

    def __init__(
        self,
        profile_repository: IProfileRepository,
        experience_repository: IOrderedRepository['WorkExperienceType'],
        skill_repository: IUniqueNameRepository['SkillType'],
        education_repository: IOrderedRepository['EducationType'],
    ):
        """
        Initialize use case with dependencies.
        
        Args:
            profile_repository: Profile repository interface
            experience_repository: Experience repository interface
            skill_repository: Skill repository interface
            education_repository: Education repository interface
        """
        self.profile_repo = profile_repository
        self.experience_repo = experience_repository
        self.skill_repo = skill_repository
        self.education_repo = education_repository

    async def execute(self, request: GetCompleteCVRequest) -> CompleteCVResponse:
        """
        Execute the use case.
        
        Args:
            request: Get complete CV request (empty)
            
        Returns:
            CompleteCVResponse with all CV data
            
        Raises:
            NotFoundException: If profile doesn't exist
        """
        # Get profile (required)
        profile = await self.profile_repo.get_profile()
        if not profile:
            raise NotFoundException("Profile", "single")
        
        # Get experiences (ordered by orderIndex, newest first)
        experiences = await self.experience_repo.get_all_ordered(
            profile_id=profile.id,
            ascending=False
        )
        
        # Get skills (find all by profile_id)
        skills = await self.skill_repo.find_by(profile_id=profile.id)
        # Sort by order_index
        skills.sort(key=lambda s: s.order_index)
        
        # Get education (ordered by orderIndex, newest first)
        education = await self.education_repo.get_all_ordered(
            profile_id=profile.id,
            ascending=False
        )
        
        # Aggregate and return
        return CompleteCVResponse.create(
            profile=profile,
            experiences=experiences,
            skills=skills,
            education=education,
        )