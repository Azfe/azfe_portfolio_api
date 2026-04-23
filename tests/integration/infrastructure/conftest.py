"""
Fixtures for integration tests of MongoDB repositories.

Each fixture creates a real repository instance connected to the test database.
Entity factory functions create valid domain entities for testing.
"""

from datetime import datetime

import pytest_asyncio

from app.domain.entities import (
    AdditionalTraining,
    Certification,
    ContactInformation,
    ContactMessage,
    Education,
    Language,
    Profile,
    ProgrammingLanguage,
    Project,
    Skill,
    WorkExperience,
)
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

# ==================== CONSTANTS ====================

PROFILE_ID = "test-profile-001"
DT_NOW = datetime(2024, 6, 15, 12, 0, 0)
DT_START = datetime(2024, 1, 1)
DT_END = datetime(2024, 12, 31)


# ==================== REPOSITORY FIXTURES ====================


@pytest_asyncio.fixture
async def profile_repo(test_db):
    return ProfileRepository(test_db)


@pytest_asyncio.fixture
async def skill_repo(test_db):
    return SkillRepository(test_db)


@pytest_asyncio.fixture
async def education_repo(test_db):
    return EducationRepository(test_db)


@pytest_asyncio.fixture
async def experience_repo(test_db):
    return WorkExperienceRepository(test_db)


@pytest_asyncio.fixture
async def project_repo(test_db):
    return ProjectRepository(test_db)


@pytest_asyncio.fixture
async def certification_repo(test_db):
    return CertificationRepository(test_db)


@pytest_asyncio.fixture
async def additional_training_repo(test_db):
    return AdditionalTrainingRepository(test_db)


@pytest_asyncio.fixture
async def language_repo(test_db):
    return LanguageRepository(test_db)


@pytest_asyncio.fixture
async def programming_language_repo(test_db):
    return ProgrammingLanguageRepository(test_db)


@pytest_asyncio.fixture
async def contact_info_repo(test_db):
    return ContactInformationRepository(test_db)


@pytest_asyncio.fixture
async def contact_message_repo(test_db):
    return ContactMessageRepository(test_db)


# ==================== ENTITY FACTORIES ====================


def make_profile(
    id: str = "profile-1",
    name: str = "John Doe",
    headline: str = "Software Developer",
    **overrides,
) -> Profile:
    defaults = {
        "id": id,
        "name": name,
        "headline": headline,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return Profile(**defaults)


def make_skill(
    id: str = "skill-1",
    profile_id: str = PROFILE_ID,
    name: str = "Python",
    category: str = "Backend",
    order_index: int = 0,
    **overrides,
) -> Skill:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "name": name,
        "category": category,
        "order_index": order_index,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return Skill(**defaults)


def make_education(
    id: str = "edu-1",
    profile_id: str = PROFILE_ID,
    institution: str = "MIT",
    degree: str = "BSc",
    field: str = "Computer Science",
    order_index: int = 0,
    **overrides,
) -> Education:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "institution": institution,
        "degree": degree,
        "field": field,
        "start_date": DT_START,
        "order_index": order_index,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return Education(**defaults)


def make_work_experience(
    id: str = "exp-1",
    profile_id: str = PROFILE_ID,
    role: str = "Senior Developer",
    company: str = "Acme Corp",
    order_index: int = 0,
    **overrides,
) -> WorkExperience:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "role": role,
        "company": company,
        "start_date": DT_START,
        "order_index": order_index,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return WorkExperience(**defaults)


def make_project(
    id: str = "proj-1",
    profile_id: str = PROFILE_ID,
    title: str = "Portfolio Website",
    description: str = "A portfolio website built with modern technologies and best practices",
    order_index: int = 0,
    **overrides,
) -> Project:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "title": title,
        "description": description,
        "start_date": DT_START,
        "order_index": order_index,
        "live_url": "https://example.com",
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return Project(**defaults)


def make_certification(
    id: str = "cert-1",
    profile_id: str = PROFILE_ID,
    title: str = "AWS Solutions Architect",
    issuer: str = "Amazon",
    order_index: int = 0,
    **overrides,
) -> Certification:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "title": title,
        "issuer": issuer,
        "issue_date": DT_START,
        "order_index": order_index,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return Certification(**defaults)


def make_additional_training(
    id: str = "train-1",
    profile_id: str = PROFILE_ID,
    title: str = "Docker Fundamentals",
    provider: str = "Udemy",
    order_index: int = 0,
    **overrides,
) -> AdditionalTraining:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "title": title,
        "provider": provider,
        "completion_date": DT_START,
        "order_index": order_index,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return AdditionalTraining(**defaults)


def make_language(
    id: str = "lang-1",
    profile_id: str = PROFILE_ID,
    name: str = "English",
    order_index: int = 0,
    **overrides,
) -> Language:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "name": name,
        "order_index": order_index,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return Language(**defaults)


def make_programming_language(
    id: str = "plang-1",
    profile_id: str = PROFILE_ID,
    name: str = "Python",
    order_index: int = 0,
    **overrides,
) -> ProgrammingLanguage:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "name": name,
        "order_index": order_index,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return ProgrammingLanguage(**defaults)


def make_contact_information(
    id: str = "cinfo-1",
    profile_id: str = PROFILE_ID,
    email: str = "test@example.com",
    **overrides,
) -> ContactInformation:
    defaults = {
        "id": id,
        "profile_id": profile_id,
        "email": email,
        "created_at": DT_NOW,
        "updated_at": DT_NOW,
    }
    defaults.update(overrides)
    return ContactInformation(**defaults)


def make_contact_message(
    id: str = "msg-1",
    name: str = "Jane Doe",
    email: str = "jane@example.com",
    message: str = "Hello, I would like to get in touch with you about a project.",
    **overrides,
) -> ContactMessage:
    defaults = {
        "id": id,
        "name": name,
        "email": email,
        "message": message,
        "created_at": DT_NOW,
    }
    defaults.update(overrides)
    return ContactMessage(**defaults)
