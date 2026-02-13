"""Tests for WorkExperience use cases."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    AddExperienceRequest,
    DeleteExperienceRequest,
    EditExperienceRequest,
    ListExperiencesRequest,
)
from app.application.use_cases.work_experience.add_experience import (
    AddExperienceUseCase,
)
from app.application.use_cases.work_experience.delete_experience import (
    DeleteExperienceUseCase,
)
from app.application.use_cases.work_experience.edit_experience import (
    EditExperienceUseCase,
)
from app.application.use_cases.work_experience.list_experiences import (
    ListExperiencesUseCase,
)
from app.domain.entities.work_experience import WorkExperience
from app.shared.shared_exceptions import (
    BusinessRuleViolationException,
    NotFoundException,
)

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"


def _make_experience(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "role": "Backend Dev",
        "company": "Acme",
        "start_date": datetime(2022, 1, 1),
        "order_index": 0,
    }
    defaults.update(overrides)
    return WorkExperience.create(**defaults)


class TestAddExperienceUseCase:
    async def test_add_experience_success(self):
        repo = AsyncMock()
        exp = _make_experience()
        repo.get_by_order_index.return_value = None
        repo.add.return_value = exp

        uc = AddExperienceUseCase(repo)
        request = AddExperienceRequest(
            profile_id=PROFILE_ID,
            role="Backend Dev",
            company="Acme",
            start_date=datetime(2022, 1, 1),
            order_index=0,
        )
        result = await uc.execute(request)

        assert result.role == "Backend Dev"
        assert result.company == "Acme"
        repo.add.assert_awaited_once()

    async def test_add_experience_duplicate_order_raises(self):
        repo = AsyncMock()
        repo.get_by_order_index.return_value = _make_experience()

        uc = AddExperienceUseCase(repo)
        request = AddExperienceRequest(
            profile_id=PROFILE_ID,
            role="Dev",
            company="Co",
            start_date=datetime(2022, 1, 1),
            order_index=0,
        )
        with pytest.raises(BusinessRuleViolationException):
            await uc.execute(request)

        repo.add.assert_not_awaited()


class TestDeleteExperienceUseCase:
    async def test_delete_experience_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteExperienceUseCase(repo)
        result = await uc.execute(DeleteExperienceRequest(experience_id="exp-001"))

        assert result.success is True

    async def test_delete_experience_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteExperienceUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(
                DeleteExperienceRequest(experience_id="nonexistent")
            )


class TestEditExperienceUseCase:
    async def test_edit_experience_success(self):
        repo = AsyncMock()
        exp = _make_experience()
        repo.get_by_id.return_value = exp
        repo.update.return_value = exp

        uc = EditExperienceUseCase(repo)
        request = EditExperienceRequest(
            experience_id="exp-001", role="Senior Dev"
        )
        result = await uc.execute(request)

        assert result.role == "Senior Dev"
        repo.update.assert_awaited_once()

    async def test_edit_experience_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditExperienceUseCase(repo)
        request = EditExperienceRequest(
            experience_id="nonexistent", role="Dev"
        )
        with pytest.raises(NotFoundException):
            await uc.execute(request)

    async def test_edit_experience_with_responsibilities(self):
        repo = AsyncMock()
        exp = _make_experience()
        repo.get_by_id.return_value = exp
        repo.update.return_value = exp

        uc = EditExperienceUseCase(repo)
        request = EditExperienceRequest(
            experience_id="exp-001",
            responsibilities=["Code review", "Architecture"],
        )
        await uc.execute(request)

        repo.update.assert_awaited_once()


class TestListExperiencesUseCase:
    async def test_list_experiences(self):
        repo = AsyncMock()
        exps = [_make_experience(order_index=0), _make_experience(order_index=1)]
        repo.get_all_ordered.return_value = exps

        uc = ListExperiencesUseCase(repo)
        request = ListExperiencesRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 2
        assert len(result.experiences) == 2
        repo.get_all_ordered.assert_awaited_once_with(
            profile_id=PROFILE_ID, ascending=False
        )

    async def test_list_experiences_ascending(self):
        repo = AsyncMock()
        repo.get_all_ordered.return_value = []

        uc = ListExperiencesUseCase(repo)
        request = ListExperiencesRequest(profile_id=PROFILE_ID, ascending=True)
        result = await uc.execute(request)

        assert result.total == 0
        repo.get_all_ordered.assert_awaited_once_with(
            profile_id=PROFILE_ID, ascending=True
        )
