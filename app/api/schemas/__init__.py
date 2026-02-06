"""Schemas de la API - Contratos de entrada/salida"""

from .additional_training_schema import (
    AdditionalTrainingCreate,
    AdditionalTrainingResponse,
    AdditionalTrainingUpdate,
)
from .certification_schema import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from .common_schema import (
    ErrorResponse,
    MessageResponse,
    SuccessResponse,
    TimestampMixin,
)
from .contact_info_schema import (
    ContactInformationCreate,
    ContactInformationResponse,
    ContactInformationUpdate,
)
from .contact_messages_schema import (
    ContactMessageCreate,
    ContactMessageResponse,
    ContactMessageUpdate,
    MessageStatus,
)
from .cv_schema import CVCompleteResponse
from .education_schema import EducationCreate, EducationResponse, EducationUpdate
from .profile_schema import ProfileCreate, ProfileResponse, ProfileUpdate
from .projects_schema import ProjectCreate, ProjectResponse, ProjectUpdate
from .skill_schema import (
    SkillCreate,
    SkillLevel,
    SkillResponse,
    SkillUpdate,
)
from .social_networks_schema import (
    SocialNetworkCreate,
    SocialNetworkResponse,
    SocialNetworkUpdate,
)
from .tools_schema import (
    ToolCreate,
    ToolResponse,
    ToolUpdate,
)
from .work_experience_schema import (
    WorkExperienceCreate,
    WorkExperienceResponse,
    WorkExperienceUpdate,
)

__all__ = [
    # Common
    "SuccessResponse",
    "ErrorResponse",
    "MessageResponse",
    "TimestampMixin",
    # Profile
    "ProfileResponse",
    "ProfileCreate",
    "ProfileUpdate",
    # Contact Info
    "ContactInformationResponse",
    "ContactInformationCreate",
    "ContactInformationUpdate",
    # Social Networks
    "SocialNetworkResponse",
    "SocialNetworkCreate",
    "SocialNetworkUpdate",
    # Projects
    "ProjectResponse",
    "ProjectCreate",
    "ProjectUpdate",
    # Work Experience
    "WorkExperienceResponse",
    "WorkExperienceCreate",
    "WorkExperienceUpdate",
    # Skills
    "SkillResponse",
    "SkillCreate",
    "SkillUpdate",
    "SkillLevel",
    # Tools
    "ToolResponse",
    "ToolCreate",
    "ToolUpdate",
    # Education
    "EducationResponse",
    "EducationCreate",
    "EducationUpdate",
    # Additional Training
    "AdditionalTrainingResponse",
    "AdditionalTrainingCreate",
    "AdditionalTrainingUpdate",
    # Certifications
    "CertificationResponse",
    "CertificationCreate",
    "CertificationUpdate",
    # Contact Messages
    "ContactMessageResponse",
    "ContactMessageCreate",
    "ContactMessageUpdate",
    "MessageStatus",
    # CV Complete
    "CVCompleteResponse",
]
