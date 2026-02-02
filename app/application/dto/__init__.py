"""
DTOs (Data Transfer Objects) Module.

Contains all request and response DTOs for application use cases.
DTOs are simple data containers without business logic.
"""

from .base_dto import (
    SuccessResponse,
    ErrorResponse,
    PaginationRequest,
    DateRangeDTO,
)

from .profile_dto import (
    CreateProfileRequest,
    UpdateProfileRequest,
    GetProfileRequest,
    ProfileResponse,
)

from .work_experience_dto import (
    AddExperienceRequest,
    EditExperienceRequest,
    DeleteExperienceRequest,
    ListExperiencesRequest,
    WorkExperienceResponse,
    WorkExperienceListResponse,
)

from .skill_dto import (
    AddSkillRequest,
    EditSkillRequest,
    DeleteSkillRequest,
    ListSkillsRequest,
    SkillResponse,
    SkillListResponse,
)

from .education_dto import (
    AddEducationRequest,
    EditEducationRequest,
    DeleteEducationRequest,
    ListEducationRequest,
    EducationResponse,
    EducationListResponse,
)

from .cv_dto import (
    GetCompleteCVRequest,
    CompleteCVResponse,
    GenerateCVPDFRequest,
    GenerateCVPDFResponse,
)

__all__ = [
    # Base
    "SuccessResponse",
    "ErrorResponse",
    "PaginationRequest",
    "DateRangeDTO",
    # Profile
    "CreateProfileRequest",
    "UpdateProfileRequest",
    "GetProfileRequest",
    "ProfileResponse",
    # Experience
    "AddExperienceRequest",
    "EditExperienceRequest",
    "DeleteExperienceRequest",
    "ListExperiencesRequest",
    "WorkExperienceResponse",
    "WorkExperienceListResponse",
    # Skill
    "AddSkillRequest",
    "EditSkillRequest",
    "DeleteSkillRequest",
    "ListSkillsRequest",
    "SkillResponse",
    "SkillListResponse",
    # Education
    "AddEducationRequest",
    "EditEducationRequest",
    "DeleteEducationRequest",
    "ListEducationRequest",
    "EducationResponse",
    "EducationListResponse",
    # CV
    "GetCompleteCVRequest",
    "CompleteCVResponse",
    "GenerateCVPDFRequest",
    "GenerateCVPDFResponse",
]