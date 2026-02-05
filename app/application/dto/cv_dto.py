"""
CV DTOs.

Data Transfer Objects for CV-related use cases.
"""

from dataclasses import dataclass

from .education_dto import EducationResponse
from .profile_dto import ProfileResponse
from .skill_dto import SkillResponse
from .work_experience_dto import WorkExperienceResponse


@dataclass
class GetCompleteCVRequest:
    """Request to get complete CV (no parameters needed)."""

    pass


@dataclass
class CompleteCVResponse:
    """Response containing complete CV data."""

    profile: ProfileResponse
    experiences: list[WorkExperienceResponse]
    skills: list[SkillResponse]
    education: list[EducationResponse]

    @classmethod
    def create(
        cls,
        profile,
        experiences,
        skills,
        education,
    ) -> "CompleteCVResponse":
        """Create complete CV response from entities."""
        return cls(
            profile=ProfileResponse.from_entity(profile),
            experiences=[WorkExperienceResponse.from_entity(e) for e in experiences],
            skills=[SkillResponse.from_entity(s) for s in skills],
            education=[EducationResponse.from_entity(e) for e in education],
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
