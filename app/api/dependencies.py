"""
Centralized dependency injection for FastAPI.

Provides factory functions that wire concrete repositories and use cases
together.  Routers consume these via ``Depends(get_<use_case>_use_case)``.

Architecture flow:
    get_database  →  get_*_repository  →  get_*_use_case  →  Router endpoint
"""

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

# ── Use cases ────────────────────────────────────────────────────────────
from app.application.use_cases import (
    AddEducationUseCase,
    AddExperienceUseCase,
    AddSkillUseCase,
    CreateProfileUseCase,
    DeleteEducationUseCase,
    DeleteExperienceUseCase,
    DeleteSkillUseCase,
    EditEducationUseCase,
    EditExperienceUseCase,
    EditSkillUseCase,
    GenerateCVPDFUseCase,
    GetCompleteCVUseCase,
    GetProfileUseCase,
    ListExperiencesUseCase,
    ListSkillsUseCase,
    UpdateProfileUseCase,
)
from app.application.use_cases.language import (
    AddLanguageUseCase,
    DeleteLanguageUseCase,
    EditLanguageUseCase,
    ListLanguagesUseCase,
)
from app.application.use_cases.programming_language import (
    AddProgrammingLanguageUseCase,
    DeleteProgrammingLanguageUseCase,
    EditProgrammingLanguageUseCase,
    ListProgrammingLanguagesUseCase,
)
from app.infrastructure.database.mongo_client import get_database

# ── Repositories ─────────────────────────────────────────────────────────
from app.infrastructure.repositories import (
    AdditionalTrainingRepository,
    CertificationRepository,
    ContactInformationRepository,
    ContactMessageRepository,
    EducationRepository,
    LanguageRepository,
    ProfileRepository,
    ProgrammingLanguageRepository,
    ProjectRepository,
    SkillRepository,
    WorkExperienceRepository,
)

# =====================================================================
# REPOSITORY PROVIDERS
# =====================================================================


async def get_profile_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ProfileRepository:
    return ProfileRepository(db)


async def get_skill_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> SkillRepository:
    return SkillRepository(db)


async def get_education_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> EducationRepository:
    return EducationRepository(db)


async def get_work_experience_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> WorkExperienceRepository:
    return WorkExperienceRepository(db)


async def get_project_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ProjectRepository:
    return ProjectRepository(db)


async def get_certification_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> CertificationRepository:
    return CertificationRepository(db)


async def get_additional_training_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> AdditionalTrainingRepository:
    return AdditionalTrainingRepository(db)


async def get_contact_information_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ContactInformationRepository:
    return ContactInformationRepository(db)


async def get_contact_message_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ContactMessageRepository:
    return ContactMessageRepository(db)


async def get_programming_language_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ProgrammingLanguageRepository:
    return ProgrammingLanguageRepository(db)


async def get_language_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> LanguageRepository:
    return LanguageRepository(db)


# =====================================================================
# USE CASE PROVIDERS — Profile
# =====================================================================


async def get_get_profile_use_case(
    repo: ProfileRepository = Depends(get_profile_repository),
) -> GetProfileUseCase:
    return GetProfileUseCase(profile_repository=repo)


async def get_create_profile_use_case(
    repo: ProfileRepository = Depends(get_profile_repository),
) -> CreateProfileUseCase:
    return CreateProfileUseCase(profile_repository=repo)


async def get_update_profile_use_case(
    repo: ProfileRepository = Depends(get_profile_repository),
) -> UpdateProfileUseCase:
    return UpdateProfileUseCase(profile_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Skill
# =====================================================================


async def get_add_skill_use_case(
    repo: SkillRepository = Depends(get_skill_repository),
) -> AddSkillUseCase:
    return AddSkillUseCase(skill_repository=repo)


async def get_edit_skill_use_case(
    repo: SkillRepository = Depends(get_skill_repository),
) -> EditSkillUseCase:
    return EditSkillUseCase(skill_repository=repo)


async def get_delete_skill_use_case(
    repo: SkillRepository = Depends(get_skill_repository),
) -> DeleteSkillUseCase:
    return DeleteSkillUseCase(skill_repository=repo)


async def get_list_skills_use_case(
    repo: SkillRepository = Depends(get_skill_repository),
) -> ListSkillsUseCase:
    return ListSkillsUseCase(skill_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Education
# =====================================================================


async def get_add_education_use_case(
    repo: EducationRepository = Depends(get_education_repository),
) -> AddEducationUseCase:
    return AddEducationUseCase(education_repository=repo)


async def get_edit_education_use_case(
    repo: EducationRepository = Depends(get_education_repository),
) -> EditEducationUseCase:
    return EditEducationUseCase(education_repository=repo)


async def get_delete_education_use_case(
    repo: EducationRepository = Depends(get_education_repository),
) -> DeleteEducationUseCase:
    return DeleteEducationUseCase(education_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Work Experience
# =====================================================================


async def get_add_experience_use_case(
    repo: WorkExperienceRepository = Depends(get_work_experience_repository),
) -> AddExperienceUseCase:
    return AddExperienceUseCase(experience_repository=repo)


async def get_edit_experience_use_case(
    repo: WorkExperienceRepository = Depends(get_work_experience_repository),
) -> EditExperienceUseCase:
    return EditExperienceUseCase(experience_repository=repo)


async def get_delete_experience_use_case(
    repo: WorkExperienceRepository = Depends(get_work_experience_repository),
) -> DeleteExperienceUseCase:
    return DeleteExperienceUseCase(experience_repository=repo)


async def get_list_experiences_use_case(
    repo: WorkExperienceRepository = Depends(get_work_experience_repository),
) -> ListExperiencesUseCase:
    return ListExperiencesUseCase(experience_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Language
# =====================================================================


async def get_add_language_use_case(
    repo: LanguageRepository = Depends(get_language_repository),
) -> AddLanguageUseCase:
    return AddLanguageUseCase(language_repository=repo)


async def get_edit_language_use_case(
    repo: LanguageRepository = Depends(get_language_repository),
) -> EditLanguageUseCase:
    return EditLanguageUseCase(language_repository=repo)


async def get_delete_language_use_case(
    repo: LanguageRepository = Depends(get_language_repository),
) -> DeleteLanguageUseCase:
    return DeleteLanguageUseCase(language_repository=repo)


async def get_list_languages_use_case(
    repo: LanguageRepository = Depends(get_language_repository),
) -> ListLanguagesUseCase:
    return ListLanguagesUseCase(language_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Programming Language
# =====================================================================


async def get_add_programming_language_use_case(
    repo: ProgrammingLanguageRepository = Depends(get_programming_language_repository),
) -> AddProgrammingLanguageUseCase:
    return AddProgrammingLanguageUseCase(programming_language_repository=repo)


async def get_edit_programming_language_use_case(
    repo: ProgrammingLanguageRepository = Depends(get_programming_language_repository),
) -> EditProgrammingLanguageUseCase:
    return EditProgrammingLanguageUseCase(programming_language_repository=repo)


async def get_delete_programming_language_use_case(
    repo: ProgrammingLanguageRepository = Depends(get_programming_language_repository),
) -> DeleteProgrammingLanguageUseCase:
    return DeleteProgrammingLanguageUseCase(programming_language_repository=repo)


async def get_list_programming_languages_use_case(
    repo: ProgrammingLanguageRepository = Depends(get_programming_language_repository),
) -> ListProgrammingLanguagesUseCase:
    return ListProgrammingLanguagesUseCase(programming_language_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — CV
# =====================================================================


async def get_get_complete_cv_use_case(
    profile_repo: ProfileRepository = Depends(get_profile_repository),
    experience_repo: WorkExperienceRepository = Depends(get_work_experience_repository),
    skill_repo: SkillRepository = Depends(get_skill_repository),
    education_repo: EducationRepository = Depends(get_education_repository),
) -> GetCompleteCVUseCase:
    return GetCompleteCVUseCase(
        profile_repository=profile_repo,
        experience_repository=experience_repo,
        skill_repository=skill_repo,
        education_repository=education_repo,
    )


async def get_generate_cv_pdf_use_case(
    get_cv_uc: GetCompleteCVUseCase = Depends(get_get_complete_cv_use_case),
) -> GenerateCVPDFUseCase:
    return GenerateCVPDFUseCase(get_cv_use_case=get_cv_uc)
