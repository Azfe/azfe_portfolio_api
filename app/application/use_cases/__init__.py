"""
Use Cases Module.

Contains all application use cases following Clean Architecture.
"""

from .additional_training import (
    AddAdditionalTrainingUseCase,
    DeleteAdditionalTrainingUseCase,
    EditAdditionalTrainingUseCase,
    ListAdditionalTrainingsUseCase,
)
from .certification import (
    AddCertificationUseCase,
    DeleteCertificationUseCase,
    EditCertificationUseCase,
    ListCertificationsUseCase,
)
from .contact_information import (
    CreateContactInformationUseCase,
    DeleteContactInformationUseCase,
    GetContactInformationUseCase,
    UpdateContactInformationUseCase,
)
from .contact_message import (
    CreateContactMessageUseCase,
    DeleteContactMessageUseCase,
    ListContactMessagesUseCase,
)
from .cv import GenerateCVPDFUseCase, GetCompleteCVUseCase
from .education import AddEducationUseCase, DeleteEducationUseCase, EditEducationUseCase
from .language import (
    AddLanguageUseCase,
    DeleteLanguageUseCase,
    EditLanguageUseCase,
    ListLanguagesUseCase,
)
from .profile import CreateProfileUseCase, GetProfileUseCase, UpdateProfileUseCase
from .programming_language import (
    AddProgrammingLanguageUseCase,
    DeleteProgrammingLanguageUseCase,
    EditProgrammingLanguageUseCase,
    ListProgrammingLanguagesUseCase,
)
from .project import (
    AddProjectUseCase,
    DeleteProjectUseCase,
    EditProjectUseCase,
    ListProjectsUseCase,
)
from .skill import (
    AddSkillUseCase,
    DeleteSkillUseCase,
    EditSkillUseCase,
    ListSkillsUseCase,
)
from .social_network import (
    AddSocialNetworkUseCase,
    DeleteSocialNetworkUseCase,
    EditSocialNetworkUseCase,
    ListSocialNetworksUseCase,
)
from .tool import (
    AddToolUseCase,
    DeleteToolUseCase,
    EditToolUseCase,
    ListToolsUseCase,
)
from .work_experience import (
    AddExperienceUseCase,
    DeleteExperienceUseCase,
    EditExperienceUseCase,
    ListExperiencesUseCase,
)

__all__ = [
    # Profile
    "GetProfileUseCase",
    "CreateProfileUseCase",
    "UpdateProfileUseCase",
    # Experience
    "AddExperienceUseCase",
    "EditExperienceUseCase",
    "DeleteExperienceUseCase",
    "ListExperiencesUseCase",
    # Skill
    "AddSkillUseCase",
    "EditSkillUseCase",
    "DeleteSkillUseCase",
    "ListSkillsUseCase",
    # Education
    "AddEducationUseCase",
    "EditEducationUseCase",
    "DeleteEducationUseCase",
    # Language
    "AddLanguageUseCase",
    "EditLanguageUseCase",
    "DeleteLanguageUseCase",
    "ListLanguagesUseCase",
    # Programming Language
    "AddProgrammingLanguageUseCase",
    "EditProgrammingLanguageUseCase",
    "DeleteProgrammingLanguageUseCase",
    "ListProgrammingLanguagesUseCase",
    # CV
    "GetCompleteCVUseCase",
    "GenerateCVPDFUseCase",
    # Project
    "AddProjectUseCase",
    "EditProjectUseCase",
    "DeleteProjectUseCase",
    "ListProjectsUseCase",
    # Certification
    "AddCertificationUseCase",
    "EditCertificationUseCase",
    "DeleteCertificationUseCase",
    "ListCertificationsUseCase",
    # AdditionalTraining
    "AddAdditionalTrainingUseCase",
    "EditAdditionalTrainingUseCase",
    "DeleteAdditionalTrainingUseCase",
    "ListAdditionalTrainingsUseCase",
    # ContactInformation
    "GetContactInformationUseCase",
    "CreateContactInformationUseCase",
    "UpdateContactInformationUseCase",
    "DeleteContactInformationUseCase",
    # ContactMessage
    "CreateContactMessageUseCase",
    "ListContactMessagesUseCase",
    "DeleteContactMessageUseCase",
    # Tool
    "AddToolUseCase",
    "EditToolUseCase",
    "DeleteToolUseCase",
    "ListToolsUseCase",
    # SocialNetwork
    "AddSocialNetworkUseCase",
    "EditSocialNetworkUseCase",
    "DeleteSocialNetworkUseCase",
    "ListSocialNetworksUseCase",
]
