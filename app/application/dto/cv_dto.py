"""
CV DTOs.

Data Transfer Objects for CV-related use cases.
"""

from dataclasses import dataclass, field

from .additional_training_dto import AdditionalTrainingResponse
from .certification_dto import CertificationResponse
from .contact_information_dto import ContactInformationResponse
from .education_dto import EducationResponse
from .profile_dto import ProfileResponse
from .project_dto import ProjectResponse
from .skill_dto import SkillResponse
from .social_network_dto import SocialNetworkResponse
from .tool_dto import ToolResponse
from .work_experience_dto import WorkExperienceResponse


@dataclass
class GetCompleteCVRequest:
    """Request to get complete CV (no parameters needed)."""

    pass


@dataclass
class CompleteCVResponse:
    """Response containing complete CV data."""

    profile: ProfileResponse
    work_experiences: list[WorkExperienceResponse]
    skills: list[SkillResponse]
    education: list[EducationResponse]
    contact_info: ContactInformationResponse | None = None
    social_networks: list[SocialNetworkResponse] = field(default_factory=list)
    projects: list[ProjectResponse] = field(default_factory=list)
    tools: list[ToolResponse] = field(default_factory=list)
    additional_training: list[AdditionalTrainingResponse] = field(default_factory=list)
    certifications: list[CertificationResponse] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        profile,
        work_experiences,
        skills,
        education,
        contact_info=None,
        social_networks=None,
        projects=None,
        tools=None,
        additional_training=None,
        certifications=None,
    ) -> "CompleteCVResponse":
        """Create complete CV response from entities."""
        return cls(
            profile=ProfileResponse.from_entity(profile),
            work_experiences=[WorkExperienceResponse.from_entity(e) for e in work_experiences],
            skills=[SkillResponse.from_entity(s) for s in skills],
            education=[EducationResponse.from_entity(e) for e in education],
            contact_info=ContactInformationResponse.from_entity(contact_info) if contact_info else None,
            social_networks=[SocialNetworkResponse.from_entity(sn) for sn in (social_networks or [])],
            projects=[ProjectResponse.from_entity(p) for p in (projects or [])],
            tools=[ToolResponse.from_entity(t) for t in (tools or [])],
            additional_training=[AdditionalTrainingResponse.from_entity(at) for at in (additional_training or [])],
            certifications=[CertificationResponse.from_entity(c) for c in (certifications or [])],
        )


@dataclass
class GenerateCVPDFRequest:
    """Request to generate CV PDF."""

    format: str = "standard"  # standard, compact, detailed
    include_photo: bool = True


@dataclass
class GenerateCVPDFResponse:
    """Response containing PDF generation result."""

    success: bool
    file_path: str
    message: str = "PDF generated successfully"
