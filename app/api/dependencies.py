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
from app.application.use_cases.additional_training import (
    AddAdditionalTrainingUseCase,
    DeleteAdditionalTrainingUseCase,
    EditAdditionalTrainingUseCase,
    ListAdditionalTrainingsUseCase,
)
from app.application.use_cases.certification import (
    AddCertificationUseCase,
    DeleteCertificationUseCase,
    EditCertificationUseCase,
    ListCertificationsUseCase,
)
from app.application.use_cases.contact_information import (
    CreateContactInformationUseCase,
    DeleteContactInformationUseCase,
    GetContactInformationUseCase,
    UpdateContactInformationUseCase,
)
from app.application.use_cases.contact_message import (
    CreateContactMessageUseCase,
    DeleteContactMessageUseCase,
    ListContactMessagesUseCase,
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
from app.application.use_cases.project import (
    AddProjectUseCase,
    DeleteProjectUseCase,
    EditProjectUseCase,
    ListProjectsUseCase,
)
from app.application.use_cases.social_network import (
    AddSocialNetworkUseCase,
    DeleteSocialNetworkUseCase,
    EditSocialNetworkUseCase,
    ListSocialNetworksUseCase,
)
from app.application.use_cases.tool import (
    AddToolUseCase,
    DeleteToolUseCase,
    EditToolUseCase,
    ListToolsUseCase,
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
    SocialNetworkRepository,
    ToolRepository,
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


async def get_tool_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ToolRepository:
    return ToolRepository(db)


async def get_social_network_repository(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> SocialNetworkRepository:
    return SocialNetworkRepository(db)


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
# USE CASE PROVIDERS — Project
# =====================================================================


async def get_add_project_use_case(
    repo: ProjectRepository = Depends(get_project_repository),
) -> AddProjectUseCase:
    return AddProjectUseCase(project_repository=repo)


async def get_edit_project_use_case(
    repo: ProjectRepository = Depends(get_project_repository),
) -> EditProjectUseCase:
    return EditProjectUseCase(project_repository=repo)


async def get_delete_project_use_case(
    repo: ProjectRepository = Depends(get_project_repository),
) -> DeleteProjectUseCase:
    return DeleteProjectUseCase(project_repository=repo)


async def get_list_projects_use_case(
    repo: ProjectRepository = Depends(get_project_repository),
) -> ListProjectsUseCase:
    return ListProjectsUseCase(project_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Certification
# =====================================================================


async def get_add_certification_use_case(
    repo: CertificationRepository = Depends(get_certification_repository),
) -> AddCertificationUseCase:
    return AddCertificationUseCase(certification_repository=repo)


async def get_edit_certification_use_case(
    repo: CertificationRepository = Depends(get_certification_repository),
) -> EditCertificationUseCase:
    return EditCertificationUseCase(certification_repository=repo)


async def get_delete_certification_use_case(
    repo: CertificationRepository = Depends(get_certification_repository),
) -> DeleteCertificationUseCase:
    return DeleteCertificationUseCase(certification_repository=repo)


async def get_list_certifications_use_case(
    repo: CertificationRepository = Depends(get_certification_repository),
) -> ListCertificationsUseCase:
    return ListCertificationsUseCase(certification_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Additional Training
# =====================================================================


async def get_add_additional_training_use_case(
    repo: AdditionalTrainingRepository = Depends(get_additional_training_repository),
) -> AddAdditionalTrainingUseCase:
    return AddAdditionalTrainingUseCase(additional_training_repository=repo)


async def get_edit_additional_training_use_case(
    repo: AdditionalTrainingRepository = Depends(get_additional_training_repository),
) -> EditAdditionalTrainingUseCase:
    return EditAdditionalTrainingUseCase(additional_training_repository=repo)


async def get_delete_additional_training_use_case(
    repo: AdditionalTrainingRepository = Depends(get_additional_training_repository),
) -> DeleteAdditionalTrainingUseCase:
    return DeleteAdditionalTrainingUseCase(additional_training_repository=repo)


async def get_list_additional_trainings_use_case(
    repo: AdditionalTrainingRepository = Depends(get_additional_training_repository),
) -> ListAdditionalTrainingsUseCase:
    return ListAdditionalTrainingsUseCase(additional_training_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Contact Information
# =====================================================================


async def get_get_contact_information_use_case(
    repo: ContactInformationRepository = Depends(get_contact_information_repository),
) -> GetContactInformationUseCase:
    return GetContactInformationUseCase(contact_information_repository=repo)


async def get_create_contact_information_use_case(
    repo: ContactInformationRepository = Depends(get_contact_information_repository),
) -> CreateContactInformationUseCase:
    return CreateContactInformationUseCase(contact_information_repository=repo)


async def get_update_contact_information_use_case(
    repo: ContactInformationRepository = Depends(get_contact_information_repository),
) -> UpdateContactInformationUseCase:
    return UpdateContactInformationUseCase(contact_information_repository=repo)


async def get_delete_contact_information_use_case(
    repo: ContactInformationRepository = Depends(get_contact_information_repository),
) -> DeleteContactInformationUseCase:
    return DeleteContactInformationUseCase(contact_information_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Contact Message
# =====================================================================


async def get_create_contact_message_use_case(
    repo: ContactMessageRepository = Depends(get_contact_message_repository),
) -> CreateContactMessageUseCase:
    return CreateContactMessageUseCase(contact_message_repository=repo)


async def get_list_contact_messages_use_case(
    repo: ContactMessageRepository = Depends(get_contact_message_repository),
) -> ListContactMessagesUseCase:
    return ListContactMessagesUseCase(contact_message_repository=repo)


async def get_delete_contact_message_use_case(
    repo: ContactMessageRepository = Depends(get_contact_message_repository),
) -> DeleteContactMessageUseCase:
    return DeleteContactMessageUseCase(contact_message_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Tool
# =====================================================================


async def get_add_tool_use_case(
    repo: ToolRepository = Depends(get_tool_repository),
) -> AddToolUseCase:
    return AddToolUseCase(tool_repository=repo)


async def get_edit_tool_use_case(
    repo: ToolRepository = Depends(get_tool_repository),
) -> EditToolUseCase:
    return EditToolUseCase(tool_repository=repo)


async def get_delete_tool_use_case(
    repo: ToolRepository = Depends(get_tool_repository),
) -> DeleteToolUseCase:
    return DeleteToolUseCase(tool_repository=repo)


async def get_list_tools_use_case(
    repo: ToolRepository = Depends(get_tool_repository),
) -> ListToolsUseCase:
    return ListToolsUseCase(tool_repository=repo)


# =====================================================================
# USE CASE PROVIDERS — Social Network
# =====================================================================


async def get_add_social_network_use_case(
    repo: SocialNetworkRepository = Depends(get_social_network_repository),
) -> AddSocialNetworkUseCase:
    return AddSocialNetworkUseCase(social_network_repository=repo)


async def get_edit_social_network_use_case(
    repo: SocialNetworkRepository = Depends(get_social_network_repository),
) -> EditSocialNetworkUseCase:
    return EditSocialNetworkUseCase(social_network_repository=repo)


async def get_delete_social_network_use_case(
    repo: SocialNetworkRepository = Depends(get_social_network_repository),
) -> DeleteSocialNetworkUseCase:
    return DeleteSocialNetworkUseCase(social_network_repository=repo)


async def get_list_social_networks_use_case(
    repo: SocialNetworkRepository = Depends(get_social_network_repository),
) -> ListSocialNetworksUseCase:
    return ListSocialNetworksUseCase(social_network_repository=repo)


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