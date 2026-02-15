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

# New DTOs
from .additional_training_dto import (
    AddAdditionalTrainingRequest,
    AdditionalTrainingListResponse,
    AdditionalTrainingResponse,
    DeleteAdditionalTrainingRequest,
    EditAdditionalTrainingRequest,
    ListAdditionalTrainingsRequest,
)
from .certification_dto import (
    AddCertificationRequest,
    CertificationListResponse,
    CertificationResponse,
    DeleteCertificationRequest,
    EditCertificationRequest,
    ListCertificationsRequest,
)
from .contact_information_dto import (
    ContactInformationResponse,
    CreateContactInformationRequest,
    DeleteContactInformationRequest,
    GetContactInformationRequest,
    UpdateContactInformationRequest,
)
from .contact_message_dto import (
    ContactMessageListResponse,
    ContactMessageResponse,
    CreateContactMessageRequest,
    DeleteContactMessageRequest,
    ListContactMessagesRequest,
)
from .project_dto import (
    AddProjectRequest,
    DeleteProjectRequest,
    EditProjectRequest,
    ListProjectsRequest,
    ProjectListResponse,
    ProjectResponse,
)
from .social_network_dto import (
    AddSocialNetworkRequest,
    DeleteSocialNetworkRequest,
    EditSocialNetworkRequest,
    ListSocialNetworksRequest,
    SocialNetworkListResponse,
    SocialNetworkResponse,
)
from .tool_dto import (
    AddToolRequest,
    DeleteToolRequest,
    EditToolRequest,
    ListToolsRequest,
    ToolListResponse,
    ToolResponse,
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
    # Project
    "AddProjectRequest",
    "EditProjectRequest",
    "DeleteProjectRequest",
    "ListProjectsRequest",
    "ProjectResponse",
    "ProjectListResponse",
    # Certification
    "AddCertificationRequest",
    "EditCertificationRequest",
    "DeleteCertificationRequest",
    "ListCertificationsRequest",
    "CertificationResponse",
    "CertificationListResponse",
    # AdditionalTraining
    "AddAdditionalTrainingRequest",
    "EditAdditionalTrainingRequest",
    "DeleteAdditionalTrainingRequest",
    "ListAdditionalTrainingsRequest",
    "AdditionalTrainingResponse",
    "AdditionalTrainingListResponse",
    # ContactInformation
    "GetContactInformationRequest",
    "CreateContactInformationRequest",
    "UpdateContactInformationRequest",
    "DeleteContactInformationRequest",
    "ContactInformationResponse",
    # ContactMessage
    "CreateContactMessageRequest",
    "ListContactMessagesRequest",
    "DeleteContactMessageRequest",
    "ContactMessageResponse",
    "ContactMessageListResponse",
    # Tool
    "AddToolRequest",
    "EditToolRequest",
    "DeleteToolRequest",
    "ListToolsRequest",
    "ToolResponse",
    "ToolListResponse",
    # SocialNetwork
    "AddSocialNetworkRequest",
    "EditSocialNetworkRequest",
    "DeleteSocialNetworkRequest",
    "ListSocialNetworksRequest",
    "SocialNetworkResponse",
    "SocialNetworkListResponse",
]
