"""Schemas de la API - Contratos de entrada/salida"""

from .common_schema import (
    SuccessResponse,
    ErrorResponse,
    MessageResponse,
    TimestampMixin
)
from .profile_schema import (
    ProfileResponse,
    ProfileCreate,
    ProfileUpdate
)
from .contact_info_schema import (
    ContactInfoResponse,
    ContactInfoCreate,
    ContactInfoUpdate
)
from .social_networks_schema import (
    SocialNetworkResponse,
    SocialNetworkCreate,
    SocialNetworkUpdate,
    SocialNetworkType
)
from .projects_schema import (
    ProjectResponse,
    ProjectCreate,
    ProjectUpdate
)
from .work_experience_schema import (
    ExperienceResponse,
    ExperienceCreate,
    ExperienceUpdate
)
from .skill_schema import (
    SkillResponse,
    SkillCreate,
    SkillUpdate,
    SkillLevel,
    SkillCategory
)
from .tools_schema import (
    ToolResponse,
    ToolCreate,
    ToolUpdate,
    ToolCategory,
    ToolLevel
)
from .education_schema import (
    EducationResponse,
    EducationCreate,
    EducationUpdate
)
from .additional_training_schema import (
    AdditionalTrainingResponse,
    AdditionalTrainingCreate,
    AdditionalTrainingUpdate
)
from .certification_schema import (
    CertificationResponse,
    CertificationCreate,
    CertificationUpdate
)
from .contact_messages_schema import (
    ContactMessageResponse,
    ContactMessageCreate,
    ContactMessageUpdate,
    MessageStatus
)
from .cv_schema import CVCompleteResponse

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
    "ContactInfoResponse",
    "ContactInfoCreate",
    "ContactInfoUpdate",
    # Social Networks
    "SocialNetworkResponse",
    "SocialNetworkCreate",
    "SocialNetworkUpdate",
    "SocialNetworkType",
    # Projects
    "ProjectResponse",
    "ProjectCreate",
    "ProjectUpdate",
    # Work Experience
    "ExperienceResponse",
    "ExperienceCreate",
    "ExperienceUpdate",
    # Skills
    "SkillResponse",
    "SkillCreate",
    "SkillUpdate",
    "SkillLevel",
    "SkillCategory",
    # Tools
    "ToolResponse",
    "ToolCreate",
    "ToolUpdate",
    "ToolCategory",
    "ToolLevel",
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