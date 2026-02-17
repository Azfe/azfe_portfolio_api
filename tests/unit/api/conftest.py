"""
Conftest for unit API tests.

Provides dependency overrides that replace real use cases and repositories
with mock implementations returning fake data. This allows unit tests to run
without MongoDB.

IMPORTANT: These overrides only affect the test execution. The production
wiring (routers -> use cases -> repositories -> MongoDB) is NOT modified.
"""

from collections.abc import AsyncGenerator
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from httpx import ASGITransport, AsyncClient
import pytest_asyncio

from app.api.dependencies import (
    get_additional_training_repository,
    get_add_additional_training_use_case,
    get_add_certification_use_case,
    get_add_education_use_case,
    get_add_experience_use_case,
    get_add_language_use_case,
    get_add_programming_language_use_case,
    get_add_project_use_case,
    get_add_skill_use_case,
    get_add_social_network_use_case,
    get_add_tool_use_case,
    get_certification_repository,
    get_contact_message_repository,
    get_create_contact_information_use_case,
    get_create_contact_message_use_case,
    get_create_profile_use_case,
    get_delete_additional_training_use_case,
    get_delete_certification_use_case,
    get_delete_contact_information_use_case,
    get_delete_contact_message_use_case,
    get_delete_education_use_case,
    get_delete_experience_use_case,
    get_delete_language_use_case,
    get_delete_programming_language_use_case,
    get_delete_project_use_case,
    get_delete_skill_use_case,
    get_delete_social_network_use_case,
    get_delete_tool_use_case,
    get_edit_additional_training_use_case,
    get_edit_certification_use_case,
    get_edit_education_use_case,
    get_edit_experience_use_case,
    get_edit_language_use_case,
    get_edit_programming_language_use_case,
    get_edit_project_use_case,
    get_edit_skill_use_case,
    get_edit_social_network_use_case,
    get_edit_tool_use_case,
    get_education_repository,
    get_generate_cv_pdf_use_case,
    get_get_complete_cv_use_case,
    get_get_contact_information_use_case,
    get_get_profile_use_case,
    get_language_repository,
    get_list_additional_trainings_use_case,
    get_list_certifications_use_case,
    get_list_contact_messages_use_case,
    get_list_experiences_use_case,
    get_list_languages_use_case,
    get_list_programming_languages_use_case,
    get_list_projects_use_case,
    get_list_skills_use_case,
    get_list_social_networks_use_case,
    get_list_tools_use_case,
    get_programming_language_repository,
    get_project_repository,
    get_skill_repository,
    get_social_network_repository,
    get_tool_repository,
    get_update_contact_information_use_case,
    get_update_profile_use_case,
    get_work_experience_repository,
)
from app.application.dto import (
    AdditionalTrainingResponse as AdditionalTrainingDTO,
    CertificationResponse as CertificationDTO,
    CompleteCVResponse,
    ContactInformationResponse as ContactInfoDTO,
    ContactMessageResponse as ContactMessageDTO,
    EducationResponse as EducationDTO,
    GenerateCVPDFResponse,
    LanguageResponse as LanguageDTO,
    ProfileResponse as ProfileDTO,
    ProgrammingLanguageResponse as ProgrammingLanguageDTO,
    ProjectResponse as ProjectDTO,
    SkillResponse as SkillDTO,
    SocialNetworkResponse as SocialNetworkDTO,
    ToolResponse as ToolDTO,
    WorkExperienceResponse as WorkExperienceDTO,
)
from app.application.dto.additional_training_dto import AdditionalTrainingListResponse
from app.application.dto.certification_dto import CertificationListResponse
from app.application.dto.contact_message_dto import ContactMessageListResponse
from app.application.dto.language_dto import LanguageListResponse
from app.application.dto.programming_language_dto import ProgrammingLanguageListResponse
from app.application.dto.project_dto import ProjectListResponse
from app.application.dto.skill_dto import SkillListResponse
from app.application.dto.social_network_dto import SocialNetworkListResponse
from app.application.dto.tool_dto import ToolListResponse
from app.application.dto.work_experience_dto import WorkExperienceListResponse
from app.main import app
from app.shared.shared_exceptions import NotFoundException

# =====================================================================
# MOCK DATA
# =====================================================================

NOW = datetime.now()
YESTERDAY = NOW - timedelta(days=1)
LAST_WEEK = NOW - timedelta(days=7)
PROFILE_ID = "default_profile"

# -- Profile --
MOCK_PROFILE = ProfileDTO(
    id="profile_001",
    name="Alex Zapata",
    headline="Full Stack Developer",
    bio="Passionate developer",
    location="Madrid, Spain",
    avatar_url=None,
    created_at=NOW,
    updated_at=NOW,
)

# -- Skills --
MOCK_SKILLS = [
    SkillDTO(
        id="skill_001", profile_id=PROFILE_ID, name="Python",
        category="backend", order_index=0, level="expert",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
    SkillDTO(
        id="skill_002", profile_id=PROFILE_ID, name="React",
        category="frontend", order_index=1, level="advanced",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
    SkillDTO(
        id="skill_003", profile_id=PROFILE_ID, name="PostgreSQL",
        category="database", order_index=2, level="intermediate",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
    SkillDTO(
        id="skill_004", profile_id=PROFILE_ID, name="FastAPI",
        category="backend", order_index=3, level="expert",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
]

# -- Education --
MOCK_EDUCATION = [
    EducationDTO(
        id="edu_001", profile_id=PROFILE_ID,
        institution="Universidad Complutense", degree="BSc Computer Science",
        field="Computer Science", start_date=datetime(2018, 9, 1),
        end_date=datetime(2022, 6, 30), description=None, order_index=0,
        created_at=NOW, updated_at=NOW, is_ongoing=False,
    ),
    EducationDTO(
        id="edu_002", profile_id=PROFILE_ID,
        institution="Coursera", degree="Machine Learning Specialization",
        field="AI", start_date=datetime(2023, 1, 1),
        end_date=None, description=None, order_index=1,
        created_at=NOW, updated_at=NOW, is_ongoing=True,
    ),
]

# -- Work Experiences --
MOCK_EXPERIENCES = [
    WorkExperienceDTO(
        id="exp_001", profile_id=PROFILE_ID, role="Senior Developer",
        company="Tech Corp", start_date=datetime(2022, 1, 1), end_date=None,
        description="Leading backend development",
        responsibilities=["Architecture", "Code review"], order_index=0,
        created_at=NOW, updated_at=NOW, is_current=True,
    ),
    WorkExperienceDTO(
        id="exp_002", profile_id=PROFILE_ID, role="Junior Developer",
        company="StartUp Inc", start_date=datetime(2020, 6, 1),
        end_date=datetime(2021, 12, 31), description="Full stack development",
        responsibilities=["Frontend", "Backend"], order_index=1,
        created_at=NOW, updated_at=NOW, is_current=False,
    ),
]

# -- Projects --
MOCK_PROJECTS = [
    ProjectDTO(
        id="proj_001", profile_id=PROFILE_ID, title="Portfolio Website",
        description="Personal portfolio built with FastAPI and React",
        start_date=datetime(2024, 1, 1), order_index=0, end_date=None,
        live_url="https://example.com",
        repo_url="https://github.com/example/portfolio",
        technologies=["Python", "FastAPI", "React"],
        created_at=NOW, updated_at=NOW, is_ongoing=True,
    ),
    ProjectDTO(
        id="proj_002", profile_id=PROFILE_ID, title="E-Commerce API",
        description="REST API for e-commerce platform",
        start_date=datetime(2023, 6, 1), order_index=1,
        end_date=datetime(2023, 12, 31), live_url=None, repo_url=None,
        technologies=["Python", "Django"],
        created_at=NOW, updated_at=NOW, is_ongoing=False,
    ),
]

# -- Certifications --
MOCK_CERTIFICATIONS = [
    CertificationDTO(
        id="cert_001", profile_id=PROFILE_ID, title="AWS Solutions Architect",
        issuer="Amazon", issue_date=datetime(2024, 1, 15), order_index=0,
        expiry_date=datetime(2027, 1, 15), credential_id="AWS-001",
        credential_url="https://aws.amazon.com/verify/001",
        created_at=NOW, updated_at=NOW, is_expired=False,
    ),
    CertificationDTO(
        id="cert_002", profile_id=PROFILE_ID, title="Python PCEP",
        issuer="Python Institute", issue_date=datetime(2023, 6, 1),
        order_index=1, expiry_date=None, credential_id=None,
        credential_url=None, created_at=NOW, updated_at=NOW, is_expired=False,
    ),
    CertificationDTO(
        id="cert_003", profile_id=PROFILE_ID, title="Scrum Master PSM I",
        issuer="Scrum.org", issue_date=datetime(2023, 3, 1), order_index=2,
        expiry_date=None, credential_id=None, credential_url=None,
        created_at=NOW, updated_at=NOW, is_expired=False,
    ),
    CertificationDTO(
        id="cert_004", profile_id=PROFILE_ID, title="MongoDB Developer",
        issuer="MongoDB Inc", issue_date=datetime(2023, 9, 1), order_index=3,
        expiry_date=None, credential_id=None, credential_url=None,
        created_at=NOW, updated_at=NOW, is_expired=False,
    ),
    CertificationDTO(
        id="cert_005", profile_id=PROFILE_ID, title="Docker DCA",
        issuer="Docker", issue_date=datetime(2022, 9, 12), order_index=4,
        expiry_date=datetime(2023, 9, 12), credential_id=None,
        credential_url=None, created_at=NOW, updated_at=NOW, is_expired=True,
    ),
]

# -- Additional Training --
MOCK_TRAININGS = [
    AdditionalTrainingDTO(
        id="train_001", profile_id=PROFILE_ID, title="Advanced Python Patterns",
        provider="Udemy", completion_date=datetime(2024, 1, 15), order_index=0,
        duration="40h", certificate_url=None, description=None,
        created_at=NOW, updated_at=NOW,
    ),
    AdditionalTrainingDTO(
        id="train_002", profile_id=PROFILE_ID, title="Docker Mastery",
        provider="Udemy", completion_date=datetime(2023, 8, 1), order_index=1,
        duration="20h", certificate_url=None, description=None,
        created_at=NOW, updated_at=NOW,
    ),
]

# -- Contact Information --
MOCK_CONTACT_INFO = ContactInfoDTO(
    id="contact_001", profile_id=PROFILE_ID, email="alex@example.com",
    phone="+34 600 000 000", linkedin="https://linkedin.com/in/alexzapata",
    github="https://github.com/alexzapata",
    website="https://alexzapata.dev", created_at=NOW, updated_at=NOW,
)

# -- Contact Messages --
MOCK_MESSAGES = [
    ContactMessageDTO(
        id="msg_001", name="John Doe", email="john@example.com",
        message="Great portfolio! Let's connect.", status="unread",
        created_at=NOW, read_at=None, replied_at=None,
    ),
    ContactMessageDTO(
        id="msg_002", name="Jane Smith", email="jane@example.com",
        message="Interested in working together.", status="unread",
        created_at=YESTERDAY, read_at=None, replied_at=None,
    ),
    ContactMessageDTO(
        id="msg_003", name="Bob Wilson", email="bob@example.com",
        message="Nice projects! Would love to discuss.", status="read",
        created_at=LAST_WEEK, read_at=LAST_WEEK, replied_at=None,
    ),
]

# -- Tools --
MOCK_TOOLS = [
    ToolDTO(
        id="tool_001", profile_id=PROFILE_ID, name="VS Code",
        category="ide", order_index=0, icon_url=None,
        created_at=NOW, updated_at=NOW,
    ),
    ToolDTO(
        id="tool_002", profile_id=PROFILE_ID, name="Git",
        category="version_control", order_index=1, icon_url=None,
        created_at=NOW, updated_at=NOW,
    ),
    ToolDTO(
        id="tool_003", profile_id=PROFILE_ID, name="Docker",
        category="devops", order_index=2, icon_url=None,
        created_at=NOW, updated_at=NOW,
    ),
    ToolDTO(
        id="tool_004", profile_id=PROFILE_ID, name="PyCharm",
        category="ide", order_index=3, icon_url=None,
        created_at=NOW, updated_at=NOW,
    ),
]

# -- Social Networks --
MOCK_SOCIAL_NETWORKS = [
    SocialNetworkDTO(
        id="social_001", profile_id=PROFILE_ID, platform="github",
        url="https://github.com/alexzapata", order_index=0,
        username="alexzapata", created_at=NOW, updated_at=NOW,
    ),
    SocialNetworkDTO(
        id="social_002", profile_id=PROFILE_ID, platform="linkedin",
        url="https://linkedin.com/in/alexzapata", order_index=1,
        username="alexzapata", created_at=NOW, updated_at=NOW,
    ),
    SocialNetworkDTO(
        id="social_003", profile_id=PROFILE_ID, platform="twitter",
        url="https://twitter.com/alexzapata", order_index=2,
        username="alexzapata", created_at=NOW, updated_at=NOW,
    ),
]

# -- Languages --
MOCK_LANGUAGES = [
    LanguageDTO(
        id="lang_001", profile_id=PROFILE_ID, name="Español",
        order_index=0, proficiency="c2",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
    LanguageDTO(
        id="lang_002", profile_id=PROFILE_ID, name="English",
        order_index=1, proficiency="b2",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
    LanguageDTO(
        id="lang_003", profile_id=PROFILE_ID, name="Français",
        order_index=2, proficiency="a2",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
]

# -- Programming Languages --
MOCK_PROGRAMMING_LANGUAGES = [
    ProgrammingLanguageDTO(
        id="pl_001", profile_id=PROFILE_ID, name="Python",
        order_index=0, level="expert",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
    ProgrammingLanguageDTO(
        id="pl_002", profile_id=PROFILE_ID, name="JavaScript",
        order_index=1, level="advanced",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
    ProgrammingLanguageDTO(
        id="pl_003", profile_id=PROFILE_ID, name="TypeScript",
        order_index=2, level="intermediate",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
    ProgrammingLanguageDTO(
        id="pl_004", profile_id=PROFILE_ID, name="Go",
        order_index=3, level="basic",
        created_at=NOW.isoformat(), updated_at=NOW.isoformat(),
    ),
]


# =====================================================================
# HELPER FUNCTIONS
# =====================================================================


def _find_by_id(items, item_id):
    for item in items:
        if item.id == item_id:
            return item
    return None


def _make_entity_from_dto(dto):
    """Create a MagicMock entity from a DTO dataclass.

    For fields that are str-ified datetimes (isoformat), convert back to datetime
    so that entity.created_at.isoformat() works in from_entity() calls.
    """
    entity = MagicMock()
    for field_name in dto.__dataclass_fields__:
        val = getattr(dto, field_name)
        # If the DTO stores created_at/updated_at as str, the entity needs datetime
        if field_name in ("created_at", "updated_at") and isinstance(val, str):
            val = datetime.fromisoformat(val)
        setattr(entity, field_name, val)

    # Add domain methods based on DTO fields
    if hasattr(dto, "is_current"):
        entity.is_current_position = MagicMock(return_value=dto.is_current)
    if hasattr(dto, "is_ongoing"):
        entity.is_ongoing = MagicMock(return_value=dto.is_ongoing)
    if hasattr(dto, "is_expired"):
        entity.is_expired = MagicMock(return_value=dto.is_expired)
    # For WorkExperienceDTO with responsibilities list
    if hasattr(dto, "responsibilities") and isinstance(dto.responsibilities, list):
        entity.responsibilities = dto.responsibilities.copy()

    return entity


def _mock_repo(items):
    """Create a mock repository with get_by_id, find_by, and delete."""
    repo = AsyncMock()

    async def mock_get_by_id(item_id):
        dto = _find_by_id(items, item_id)
        if dto is None:
            return None
        return _make_entity_from_dto(dto)

    repo.get_by_id = AsyncMock(side_effect=mock_get_by_id)

    async def mock_find_by(**kwargs):
        return [_make_entity_from_dto(dto) for dto in items]

    repo.find_by = AsyncMock(side_effect=mock_find_by)
    repo.delete = AsyncMock(return_value=True)

    return repo


def _mock_list_uc(list_response):
    """Create a mock use case that returns a list response."""
    uc = AsyncMock()
    uc.execute = AsyncMock(return_value=list_response)
    return uc


def _mock_command_uc(return_value=None):
    """Create a mock use case for create/update/delete."""
    uc = AsyncMock()
    uc.execute = AsyncMock(return_value=return_value)
    return uc


def _mock_edit_uc(items, id_field, return_item):
    """Create a mock edit use case that raises NotFoundException for unknown IDs."""
    uc = AsyncMock()

    async def execute(request):
        item_id = getattr(request, id_field)
        found = _find_by_id(items, item_id)
        if found is None:
            raise NotFoundException(type(request).__name__, item_id)
        return return_item

    uc.execute = AsyncMock(side_effect=execute)
    return uc


def _mock_skill_list_uc():
    """Skill list UC that respects category filter."""
    uc = AsyncMock()

    async def execute(request):
        skills = MOCK_SKILLS
        if request.category:
            skills = [s for s in skills if s.category == request.category]
        return SkillListResponse(skills=skills, total=len(skills))

    uc.execute = AsyncMock(side_effect=execute)
    return uc


def _mock_tool_list_uc():
    """Tool list UC that respects category filter."""
    uc = AsyncMock()

    async def execute(request):
        tools = MOCK_TOOLS
        if request.category:
            tools = [t for t in tools if t.category == request.category]
        return ToolListResponse(tools=tools, total=len(tools))

    uc.execute = AsyncMock(side_effect=execute)
    return uc


# =====================================================================
# APPLY OVERRIDES
# =====================================================================


@pytest_asyncio.fixture(autouse=True)
async def _apply_dependency_overrides():
    """
    Apply all dependency overrides before each test, clear after.
    This fixture is autouse so it applies to every test in tests/unit/api/.
    """

    # -- Profile --
    app.dependency_overrides[get_get_profile_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_PROFILE
    )
    app.dependency_overrides[get_create_profile_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_PROFILE
    )
    app.dependency_overrides[get_update_profile_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_PROFILE
    )

    # -- Skills --
    app.dependency_overrides[get_list_skills_use_case] = _mock_skill_list_uc
    app.dependency_overrides[get_add_skill_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_SKILLS[0]
    )
    app.dependency_overrides[get_edit_skill_use_case] = lambda: _mock_edit_uc(
        MOCK_SKILLS, "skill_id", MOCK_SKILLS[0]
    )
    app.dependency_overrides[get_delete_skill_use_case] = lambda: _mock_command_uc()
    app.dependency_overrides[get_skill_repository] = lambda: _mock_repo(MOCK_SKILLS)

    # -- Education --
    app.dependency_overrides[get_add_education_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_EDUCATION[0]
    )
    app.dependency_overrides[get_edit_education_use_case] = lambda: _mock_edit_uc(
        MOCK_EDUCATION, "education_id", MOCK_EDUCATION[0]
    )
    app.dependency_overrides[get_delete_education_use_case] = lambda: _mock_command_uc()
    app.dependency_overrides[get_education_repository] = lambda: _mock_repo(
        MOCK_EDUCATION
    )

    # -- Work Experience --
    exp_list_response = WorkExperienceListResponse(
        experiences=MOCK_EXPERIENCES, total=len(MOCK_EXPERIENCES)
    )
    app.dependency_overrides[get_list_experiences_use_case] = lambda: _mock_list_uc(
        exp_list_response
    )
    app.dependency_overrides[get_add_experience_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_EXPERIENCES[0]
    )
    app.dependency_overrides[get_edit_experience_use_case] = lambda: _mock_edit_uc(
        MOCK_EXPERIENCES, "experience_id", MOCK_EXPERIENCES[0]
    )
    app.dependency_overrides[get_delete_experience_use_case] = (
        lambda: _mock_command_uc()
    )
    app.dependency_overrides[get_work_experience_repository] = lambda: _mock_repo(
        MOCK_EXPERIENCES
    )

    # -- Projects --
    proj_list_response = ProjectListResponse(
        projects=MOCK_PROJECTS, total=len(MOCK_PROJECTS)
    )
    app.dependency_overrides[get_list_projects_use_case] = lambda: _mock_list_uc(
        proj_list_response
    )
    app.dependency_overrides[get_add_project_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_PROJECTS[0]
    )
    app.dependency_overrides[get_edit_project_use_case] = lambda: _mock_edit_uc(
        MOCK_PROJECTS, "project_id", MOCK_PROJECTS[0]
    )
    app.dependency_overrides[get_delete_project_use_case] = lambda: _mock_command_uc()
    app.dependency_overrides[get_project_repository] = lambda: _mock_repo(MOCK_PROJECTS)

    # -- Certifications --
    cert_list_response = CertificationListResponse(
        certifications=MOCK_CERTIFICATIONS, total=len(MOCK_CERTIFICATIONS)
    )
    app.dependency_overrides[get_list_certifications_use_case] = lambda: _mock_list_uc(
        cert_list_response
    )
    app.dependency_overrides[get_add_certification_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_CERTIFICATIONS[0]
    )
    app.dependency_overrides[get_edit_certification_use_case] = lambda: _mock_edit_uc(
        MOCK_CERTIFICATIONS, "certification_id", MOCK_CERTIFICATIONS[0]
    )
    app.dependency_overrides[get_delete_certification_use_case] = (
        lambda: _mock_command_uc()
    )
    app.dependency_overrides[get_certification_repository] = lambda: _mock_repo(
        MOCK_CERTIFICATIONS
    )

    # -- Additional Training --
    train_list_response = AdditionalTrainingListResponse(
        trainings=MOCK_TRAININGS, total=len(MOCK_TRAININGS)
    )
    app.dependency_overrides[get_list_additional_trainings_use_case] = (
        lambda: _mock_list_uc(train_list_response)
    )
    app.dependency_overrides[get_add_additional_training_use_case] = (
        lambda: _mock_command_uc(return_value=MOCK_TRAININGS[0])
    )
    app.dependency_overrides[get_edit_additional_training_use_case] = (
        lambda: _mock_edit_uc(MOCK_TRAININGS, "training_id", MOCK_TRAININGS[0])
    )
    app.dependency_overrides[get_delete_additional_training_use_case] = (
        lambda: _mock_command_uc()
    )
    app.dependency_overrides[get_additional_training_repository] = lambda: _mock_repo(
        MOCK_TRAININGS
    )

    # -- Contact Information --
    app.dependency_overrides[get_get_contact_information_use_case] = (
        lambda: _mock_command_uc(return_value=MOCK_CONTACT_INFO)
    )
    app.dependency_overrides[get_create_contact_information_use_case] = (
        lambda: _mock_command_uc(return_value=MOCK_CONTACT_INFO)
    )
    app.dependency_overrides[get_update_contact_information_use_case] = (
        lambda: _mock_command_uc(return_value=MOCK_CONTACT_INFO)
    )
    app.dependency_overrides[get_delete_contact_information_use_case] = (
        lambda: _mock_command_uc()
    )

    # -- Contact Messages --
    msg_list_response = ContactMessageListResponse(
        messages=MOCK_MESSAGES, total=len(MOCK_MESSAGES)
    )
    app.dependency_overrides[get_list_contact_messages_use_case] = (
        lambda: _mock_list_uc(msg_list_response)
    )
    app.dependency_overrides[get_create_contact_message_use_case] = (
        lambda: _mock_command_uc(return_value=MOCK_MESSAGES[0])
    )
    app.dependency_overrides[get_delete_contact_message_use_case] = (
        lambda: _mock_command_uc()
    )
    app.dependency_overrides[get_contact_message_repository] = lambda: _mock_repo(
        MOCK_MESSAGES
    )

    # -- Tools --
    app.dependency_overrides[get_list_tools_use_case] = _mock_tool_list_uc
    app.dependency_overrides[get_add_tool_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_TOOLS[0]
    )
    app.dependency_overrides[get_edit_tool_use_case] = lambda: _mock_edit_uc(
        MOCK_TOOLS, "tool_id", MOCK_TOOLS[0]
    )
    app.dependency_overrides[get_delete_tool_use_case] = lambda: _mock_command_uc()
    app.dependency_overrides[get_tool_repository] = lambda: _mock_repo(MOCK_TOOLS)

    # -- Social Networks --
    social_list_response = SocialNetworkListResponse(
        social_networks=MOCK_SOCIAL_NETWORKS, total=len(MOCK_SOCIAL_NETWORKS)
    )
    app.dependency_overrides[get_list_social_networks_use_case] = (
        lambda: _mock_list_uc(social_list_response)
    )
    app.dependency_overrides[get_add_social_network_use_case] = (
        lambda: _mock_command_uc(return_value=MOCK_SOCIAL_NETWORKS[0])
    )
    app.dependency_overrides[get_edit_social_network_use_case] = (
        lambda: _mock_edit_uc(
            MOCK_SOCIAL_NETWORKS, "social_network_id", MOCK_SOCIAL_NETWORKS[0]
        )
    )
    app.dependency_overrides[get_delete_social_network_use_case] = (
        lambda: _mock_command_uc()
    )
    app.dependency_overrides[get_social_network_repository] = lambda: _mock_repo(
        MOCK_SOCIAL_NETWORKS
    )

    # -- Languages --
    lang_list_response = LanguageListResponse(
        languages=MOCK_LANGUAGES, total=len(MOCK_LANGUAGES)
    )
    app.dependency_overrides[get_list_languages_use_case] = lambda: _mock_list_uc(
        lang_list_response
    )
    app.dependency_overrides[get_add_language_use_case] = lambda: _mock_command_uc(
        return_value=MOCK_LANGUAGES[0]
    )
    app.dependency_overrides[get_edit_language_use_case] = lambda: _mock_edit_uc(
        MOCK_LANGUAGES, "language_id", MOCK_LANGUAGES[0]
    )

    # Language delete: raises NotFoundException for unknown IDs
    async def lang_delete_execute(request):
        if _find_by_id(MOCK_LANGUAGES, request.language_id) is None:
            raise NotFoundException("Language", request.language_id)

    lang_delete_uc = AsyncMock()
    lang_delete_uc.execute = AsyncMock(side_effect=lang_delete_execute)
    app.dependency_overrides[get_delete_language_use_case] = lambda: lang_delete_uc
    app.dependency_overrides[get_language_repository] = lambda: _mock_repo(
        MOCK_LANGUAGES
    )

    # -- Programming Languages --
    pl_list_response = ProgrammingLanguageListResponse(
        programming_languages=MOCK_PROGRAMMING_LANGUAGES,
        total=len(MOCK_PROGRAMMING_LANGUAGES),
    )
    app.dependency_overrides[get_list_programming_languages_use_case] = (
        lambda: _mock_list_uc(pl_list_response)
    )
    app.dependency_overrides[get_add_programming_language_use_case] = (
        lambda: _mock_command_uc(return_value=MOCK_PROGRAMMING_LANGUAGES[0])
    )
    app.dependency_overrides[get_edit_programming_language_use_case] = (
        lambda: _mock_edit_uc(
            MOCK_PROGRAMMING_LANGUAGES,
            "programming_language_id",
            MOCK_PROGRAMMING_LANGUAGES[0],
        )
    )

    # PL delete: raises NotFoundException for unknown IDs
    async def pl_delete_execute(request):
        if (
            _find_by_id(
                MOCK_PROGRAMMING_LANGUAGES, request.programming_language_id
            )
            is None
        ):
            raise NotFoundException(
                "ProgrammingLanguage", request.programming_language_id
            )

    pl_delete_uc = AsyncMock()
    pl_delete_uc.execute = AsyncMock(side_effect=pl_delete_execute)
    app.dependency_overrides[get_delete_programming_language_use_case] = (
        lambda: pl_delete_uc
    )
    app.dependency_overrides[get_programming_language_repository] = lambda: _mock_repo(
        MOCK_PROGRAMMING_LANGUAGES
    )

    # -- CV --
    cv_response = CompleteCVResponse(
        profile=MOCK_PROFILE,
        experiences=MOCK_EXPERIENCES,
        skills=MOCK_SKILLS,
        education=MOCK_EDUCATION,
    )
    app.dependency_overrides[get_get_complete_cv_use_case] = lambda: _mock_command_uc(
        return_value=cv_response
    )

    pdf_response = GenerateCVPDFResponse(
        success=True,
        file_path="/tmp/cv.pdf",
        message="Generación de PDF no implementada aún",
    )
    app.dependency_overrides[get_generate_cv_pdf_use_case] = lambda: _mock_command_uc(
        return_value=pdf_response
    )

    yield

    app.dependency_overrides.clear()
