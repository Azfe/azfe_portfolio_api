"""
DTOs (Data Transfer Objects) Module.

Contains all request and response DTOs for application use cases.
DTOs are simple data containers without business logic.
"""

from .base_dto import DateRangeDTO, ErrorResponse, PaginationRequest, SuccessResponse
from .cv_dto import (
    CompleteCVResponse,
    GenerateCVPDFRequest,
    GenerateCVPDFResponse,
    GetCompleteCVRequest,
)
from .education_dto import (
    AddEducationRequest,
    DeleteEducationRequest,
    EditEducationRequest,
    EducationListResponse,
    EducationResponse,
    ListEducationRequest,
)
from .language_dto import (
    AddLanguageRequest,
    DeleteLanguageRequest,
    EditLanguageRequest,
    LanguageListResponse,
    LanguageResponse,
    ListLanguagesRequest,
)
from .profile_dto import (
    CreateProfileRequest,
    GetProfileRequest,
    ProfileResponse,
    UpdateProfileRequest,
)
from .programming_language_dto import (
    AddProgrammingLanguageRequest,
    DeleteProgrammingLanguageRequest,
    EditProgrammingLanguageRequest,
    ListProgrammingLanguagesRequest,
    ProgrammingLanguageListResponse,
    ProgrammingLanguageResponse,
)
from .skill_dto import (
    AddSkillRequest,
    DeleteSkillRequest,
    EditSkillRequest,
    ListSkillsRequest,
    SkillListResponse,
    SkillResponse,
)
from .work_experience_dto import (
    AddExperienceRequest,
    DeleteExperienceRequest,
    EditExperienceRequest,
    ListExperiencesRequest,
    WorkExperienceListResponse,
    WorkExperienceResponse,
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
    # ProgrammingLanguage
    "AddProgrammingLanguageRequest",
    "EditProgrammingLanguageRequest",
    "DeleteProgrammingLanguageRequest",
    "ListProgrammingLanguagesRequest",
    "ProgrammingLanguageResponse",
    "ProgrammingLanguageListResponse",
    # Language
    "AddLanguageRequest",
    "EditLanguageRequest",
    "DeleteLanguageRequest",
    "ListLanguagesRequest",
    "LanguageResponse",
    "LanguageListResponse",
    # CV
    "GetCompleteCVRequest",
    "CompleteCVResponse",
    "GenerateCVPDFRequest",
    "GenerateCVPDFResponse",
]
