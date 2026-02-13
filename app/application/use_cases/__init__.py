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
- language/: Language management use cases
- programming_language/: Programming language management use cases
"""

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
from .skill import (
    AddSkillUseCase,
    DeleteSkillUseCase,
    EditSkillUseCase,
    ListSkillsUseCase,
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
]
