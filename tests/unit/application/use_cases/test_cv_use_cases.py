"""Tests for CV use cases."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    GenerateCVPDFRequest,
    GetCompleteCVRequest,
)
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


class TestGetCompleteCVUseCase:
    async def test_get_cv_success(self):
        profile = _make_profile()
        profile_repo = AsyncMock()
        profile_repo.get_profile.return_value = profile

        exp_repo = AsyncMock()
        exp_repo.get_all_ordered.return_value = [_make_experience(profile.id)]

        skill_repo = AsyncMock()
        skill_repo.find_by.return_value = [_make_skill(profile.id)]

        edu_repo = AsyncMock()
        edu_repo.get_all_ordered.return_value = [_make_education(profile.id)]

        uc = GetCompleteCVUseCase(profile_repo, exp_repo, skill_repo, edu_repo)
        result = await uc.execute(GetCompleteCVRequest())

        assert result.profile.name == "Alex"
        assert len(result.experiences) == 1
        assert len(result.skills) == 1
        assert len(result.education) == 1

    async def test_get_cv_no_profile_raises(self):
        profile_repo = AsyncMock()
        profile_repo.get_profile.return_value = None
        exp_repo = AsyncMock()
        skill_repo = AsyncMock()
        edu_repo = AsyncMock()

        uc = GetCompleteCVUseCase(profile_repo, exp_repo, skill_repo, edu_repo)
        with pytest.raises(NotFoundException):
            await uc.execute(GetCompleteCVRequest())

    async def test_get_cv_empty_lists(self):
        profile = _make_profile()
        profile_repo = AsyncMock()
        profile_repo.get_profile.return_value = profile

        exp_repo = AsyncMock()
        exp_repo.get_all_ordered.return_value = []

        skill_repo = AsyncMock()
        skill_repo.find_by.return_value = []

        edu_repo = AsyncMock()
        edu_repo.get_all_ordered.return_value = []

        uc = GetCompleteCVUseCase(profile_repo, exp_repo, skill_repo, edu_repo)
        result = await uc.execute(GetCompleteCVRequest())

        assert result.profile.name == "Alex"
        assert result.experiences == []
        assert result.skills == []
        assert result.education == []


class TestGenerateCVPDFUseCase:
    async def test_generate_pdf_placeholder(self):
        profile = _make_profile()
        profile_repo = AsyncMock()
        profile_repo.get_profile.return_value = profile

        exp_repo = AsyncMock()
        exp_repo.get_all_ordered.return_value = []
        skill_repo = AsyncMock()
        skill_repo.find_by.return_value = []
        edu_repo = AsyncMock()
        edu_repo.get_all_ordered.return_value = []

        get_cv_uc = GetCompleteCVUseCase(
            profile_repo, exp_repo, skill_repo, edu_repo
        )
        uc = GenerateCVPDFUseCase(get_cv_uc)

        result = await uc.execute(GenerateCVPDFRequest())

        assert result.success is True
        assert profile.id in result.file_path
        assert "standard" in result.file_path
