"""
Get Complete CV Use Case.

Aggregates all CV data from multiple sources.
"""

from typing import TYPE_CHECKING

from app.application.dto import CompleteCVResponse, GetCompleteCVRequest
from app.shared.interfaces import (
    IOrderedRepository,
    IProfileRepository,
    IQueryUseCase,
    IRepository,
    ISocialNetworkRepository,
    IUniqueNameRepository,
)
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import (
        AdditionalTraining as AdditionalTrainingType,
        Certification as CertificationType,
        ContactInformation as ContactInformationType,
        Education as EducationType,
        Project as ProjectType,
        Skill as SkillType,
        Tool as ToolType,
        WorkExperience as WorkExperienceType,
    )


class GetCompleteCVUseCase(IQueryUseCase[GetCompleteCVRequest, CompleteCVResponse]):
    """
    Use case for retrieving the complete CV.

    Aggregates data from multiple sources:
    - Profile
    - Contact Information
    - Social Networks
    - Work Experiences
    - Projects
    - Skills
    - Tools
    - Education
    - Additional Training
    - Certifications

    Business Rules:
    - Profile must exist
    - All lists are ordered appropriately
    - Empty lists are returned if no data exists
    - Contact information is optional (None if not set)

    Dependencies:
    - IProfileRepository: For profile data
    - IRepository[ContactInformation]: For contact info
    - ISocialNetworkRepository: For social networks
    - IOrderedRepository[WorkExperience]: For experiences
    - IOrderedRepository[Project]: For projects
    - IUniqueNameRepository[Skill]: For skills
    - IUniqueNameRepository[Tool]: For tools
    - IOrderedRepository[Education]: For education
    - IOrderedRepository[AdditionalTraining]: For additional training
    - IOrderedRepository[Certification]: For certifications
    """

    def __init__(
        self,
        profile_repository: IProfileRepository,
        experience_repository: IOrderedRepository["WorkExperienceType"],
        skill_repository: IUniqueNameRepository["SkillType"],
        education_repository: IOrderedRepository["EducationType"],
        contact_info_repository: IRepository["ContactInformationType"],
        social_network_repository: ISocialNetworkRepository,
        project_repository: IOrderedRepository["ProjectType"],
        tool_repository: IUniqueNameRepository["ToolType"],
        additional_training_repository: IOrderedRepository["AdditionalTrainingType"],
        certification_repository: IOrderedRepository["CertificationType"],
    ):
        self.profile_repo = profile_repository
        self.experience_repo = experience_repository
        self.skill_repo = skill_repository
        self.education_repo = education_repository
        self.contact_info_repo = contact_info_repository
        self.social_network_repo = social_network_repository
        self.project_repo = project_repository
        self.tool_repo = tool_repository
        self.additional_training_repo = additional_training_repository
        self.certification_repo = certification_repository

    async def execute(self, _request: GetCompleteCVRequest) -> CompleteCVResponse:
        """
        Execute the use case.

        Args:
            _request: Get complete CV request (empty)

        Returns:
            CompleteCVResponse with all CV data

        Raises:
            NotFoundException: If profile doesn't exist
        """
        # Get profile (required)
        profile = await self.profile_repo.get_profile()
        if not profile:
            raise NotFoundException("Profile", "single")

        # Get contact information (optional — None if not set)
        contact_info_results = await self.contact_info_repo.find_by(
            profile_id=profile.id
        )
        contact_info = contact_info_results[0] if contact_info_results else None

        # Get social networks (ordered by order_index)
        social_networks = await self.social_network_repo.find_by(profile_id=profile.id)
        social_networks.sort(key=lambda sn: sn.order_index)

        # Get experiences (ordered by order_index, newest first)
        experiences = await self.experience_repo.get_all_ordered(
            profile_id=profile.id, ascending=False
        )

        # Get projects (ordered by order_index, newest first)
        projects = await self.project_repo.get_all_ordered(
            profile_id=profile.id, ascending=False
        )

        # Get skills (find all by profile_id, sorted by order_index)
        skills = await self.skill_repo.find_by(profile_id=profile.id)
        skills.sort(key=lambda s: s.order_index)

        # Get tools (find all by profile_id, sorted by order_index)
        tools = await self.tool_repo.find_by(profile_id=profile.id)
        tools.sort(key=lambda t: t.order_index)

        # Get education (ordered by order_index, newest first)
        education = await self.education_repo.get_all_ordered(
            profile_id=profile.id, ascending=False
        )

        # Get additional training (ordered by order_index, newest first)
        additional_training = await self.additional_training_repo.get_all_ordered(
            profile_id=profile.id, ascending=False
        )

        # Get certifications (ordered by order_index, newest first)
        certifications = await self.certification_repo.get_all_ordered(
            profile_id=profile.id, ascending=False
        )

        return CompleteCVResponse.create(
            profile=profile,
            contact_info=contact_info,
            social_networks=social_networks,
            work_experiences=experiences,
            projects=projects,
            skills=skills,
            tools=tools,
            education=education,
            additional_training=additional_training,
            certifications=certifications,
        )
