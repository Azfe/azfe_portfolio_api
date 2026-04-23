"""Tests for CV use cases."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.application.dto import GenerateCVPDFRequest, GetCompleteCVRequest
from app.application.use_cases.cv.generate_cv_pdf import GenerateCVPDFUseCase
from app.application.use_cases.cv.get_complete_cv import GetCompleteCVUseCase
from app.domain.entities.education import Education
from app.domain.entities.profile import Profile
from app.domain.entities.skill import Skill
from app.domain.entities.work_experience import WorkExperience
from app.shared.shared_exceptions import NotFoundException

pytestmark = pytest.mark.asyncio


def _make_profile():
    return Profile.create(name="Alex", headline="Developer")


def _make_skill(profile_id):
    return Skill.create(
        profile_id=profile_id,
        name="Python",
        category="backend",
        order_index=0,
    )


def _make_experience(profile_id):
    return WorkExperience.create(
        profile_id=profile_id,
        role="Dev",
        company="Acme",
        start_date=datetime(2022, 1, 1),
        order_index=0,
    )


def _make_education(profile_id):
    return Education.create(
        profile_id=profile_id,
        institution="MIT",
        degree="BSc",
        field="CS",
        start_date=datetime(2018, 9, 1),
        order_index=0,
    )


def _make_all_repos(profile, *, contact_info=None):
    """Build the full set of mocked repos needed by GetCompleteCVUseCase."""
    profile_repo = AsyncMock()
    profile_repo.get_profile.return_value = profile

    exp_repo = AsyncMock()
    exp_repo.get_all_ordered.return_value = []

    skill_repo = AsyncMock()
    skill_repo.find_by.return_value = []

    edu_repo = AsyncMock()
    edu_repo.get_all_ordered.return_value = []

    contact_info_repo = AsyncMock()
    contact_info_repo.find_by.return_value = [contact_info] if contact_info else []

    social_network_repo = AsyncMock()
    social_network_repo.find_by.return_value = []

    project_repo = AsyncMock()
    project_repo.get_all_ordered.return_value = []

    tool_repo = AsyncMock()
    tool_repo.find_by.return_value = []

    additional_training_repo = AsyncMock()
    additional_training_repo.get_all_ordered.return_value = []

    certification_repo = AsyncMock()
    certification_repo.get_all_ordered.return_value = []

    return (
        profile_repo,
        exp_repo,
        skill_repo,
        edu_repo,
        contact_info_repo,
        social_network_repo,
        project_repo,
        tool_repo,
        additional_training_repo,
        certification_repo,
    )


def _make_use_case(profile, **repo_overrides):
    repos = _make_all_repos(profile)
    (
        profile_repo,
        exp_repo,
        skill_repo,
        edu_repo,
        contact_info_repo,
        social_network_repo,
        project_repo,
        tool_repo,
        additional_training_repo,
        certification_repo,
    ) = repos
    return GetCompleteCVUseCase(
        profile_repository=profile_repo,
        experience_repository=exp_repo,
        skill_repository=skill_repo,
        education_repository=edu_repo,
        contact_info_repository=contact_info_repo,
        social_network_repository=social_network_repo,
        project_repository=project_repo,
        tool_repository=tool_repo,
        additional_training_repository=additional_training_repo,
        certification_repository=certification_repo,
    )


class TestGetCompleteCVUseCase:
    async def test_get_cv_success(self):
        profile = _make_profile()
        (
            profile_repo,
            exp_repo,
            skill_repo,
            edu_repo,
            contact_info_repo,
            social_network_repo,
            project_repo,
            tool_repo,
            additional_training_repo,
            certification_repo,
        ) = _make_all_repos(profile)

        exp_repo.get_all_ordered.return_value = [_make_experience(profile.id)]
        skill_repo.find_by.return_value = [_make_skill(profile.id)]
        edu_repo.get_all_ordered.return_value = [_make_education(profile.id)]

        uc = GetCompleteCVUseCase(
            profile_repository=profile_repo,
            experience_repository=exp_repo,
            skill_repository=skill_repo,
            education_repository=edu_repo,
            contact_info_repository=contact_info_repo,
            social_network_repository=social_network_repo,
            project_repository=project_repo,
            tool_repository=tool_repo,
            additional_training_repository=additional_training_repo,
            certification_repository=certification_repo,
        )
        result = await uc.execute(GetCompleteCVRequest())

        assert result.profile.name == "Alex"
        assert len(result.work_experiences) == 1
        assert len(result.skills) == 1
        assert len(result.education) == 1
        assert result.contact_info is None
        assert result.social_networks == []
        assert result.projects == []
        assert result.tools == []
        assert result.additional_training == []
        assert result.certifications == []

    async def test_get_cv_no_profile_raises(self):
        profile_repo = AsyncMock()
        profile_repo.get_profile.return_value = None

        uc = GetCompleteCVUseCase(
            profile_repository=profile_repo,
            experience_repository=AsyncMock(),
            skill_repository=AsyncMock(),
            education_repository=AsyncMock(),
            contact_info_repository=AsyncMock(),
            social_network_repository=AsyncMock(),
            project_repository=AsyncMock(),
            tool_repository=AsyncMock(),
            additional_training_repository=AsyncMock(),
            certification_repository=AsyncMock(),
        )
        with pytest.raises(NotFoundException):
            await uc.execute(GetCompleteCVRequest())

    async def test_get_cv_empty_lists(self):
        profile = _make_profile()
        uc = _make_use_case(profile)
        result = await uc.execute(GetCompleteCVRequest())

        assert result.profile.name == "Alex"
        assert result.work_experiences == []
        assert result.skills == []
        assert result.education == []
        assert result.contact_info is None
        assert result.social_networks == []
        assert result.projects == []
        assert result.tools == []
        assert result.additional_training == []
        assert result.certifications == []


class TestGenerateCVPDFUseCase:
    async def test_generate_pdf_placeholder(self):
        profile = _make_profile()
        uc = _make_use_case(profile)
        pdf_uc = GenerateCVPDFUseCase(uc)

        result = await pdf_uc.execute(GenerateCVPDFRequest())

        assert result.success is True
        assert profile.id in result.file_path
        assert "standard" in result.file_path
