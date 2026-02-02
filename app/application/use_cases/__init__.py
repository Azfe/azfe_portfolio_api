"""
Use Cases Module.

Contains all application use cases following Clean Architecture.

Use cases represent the business logic of the application and orchestrate
the flow between entities, repositories, and external services.

Organization:
- profile/: Profile management use cases
- experience/: Work experience use cases
- skill/: Skill management use cases
- education/: Education management use cases
- cv/: CV aggregation and generation use cases
"""

from .profile import (
    GetProfileUseCase,
    CreateProfileUseCase,
    UpdateProfileUseCase,
)

from .work_experience import (
    AddExperienceUseCase,
    EditExperienceUseCase,
    DeleteExperienceUseCase,
    ListExperiencesUseCase,
)

from .skill import (
    AddSkillUseCase,
    EditSkillUseCase,
    DeleteSkillUseCase,
    ListSkillsUseCase,
)

from .education import (
    AddEducationUseCase,
    EditEducationUseCase,
    DeleteEducationUseCase,
)

from .cv import (
    GetCompleteCVUseCase,
    GenerateCVPDFUseCase,
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
    # CV
    "GetCompleteCVUseCase",
    "GenerateCVPDFUseCase",
]