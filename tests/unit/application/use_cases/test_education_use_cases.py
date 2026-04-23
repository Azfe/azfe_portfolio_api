"""Tests for Education use cases."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    AddEducationRequest,
    DeleteEducationRequest,
    EditEducationRequest,
)
from app.application.use_cases.education.add_education import AddEducationUseCase
from app.application.use_cases.education.delete_education import DeleteEducationUseCase
from app.application.use_cases.education.edit_education import EditEducationUseCase
from app.domain.entities.education import Education
from app.shared.shared_exceptions import (
    BusinessRuleViolationException,
    NotFoundException,
)

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"


def _make_education(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "institution": "MIT",
        "degree": "BSc",
        "field": "Computer Science",
        "start_date": datetime(2018, 9, 1),
        "order_index": 0,
    }
    defaults.update(overrides)
    return Education.create(**defaults)


class TestAddEducationUseCase:
    async def test_add_education_success(self):
        repo = AsyncMock()
        education = _make_education()
        repo.get_by_order_index.return_value = None
        repo.add.return_value = education

        uc = AddEducationUseCase(repo)
        request = AddEducationRequest(
            profile_id=PROFILE_ID,
            institution="MIT",
            degree="BSc",
            field="Computer Science",
            start_date=datetime(2018, 9, 1),
            order_index=0,
        )
        result = await uc.execute(request)

        assert result.institution == "MIT"
        repo.get_by_order_index.assert_awaited_once_with(PROFILE_ID, 0)
        repo.add.assert_awaited_once()

    async def test_add_education_duplicate_order_raises(self):
        repo = AsyncMock()
        repo.get_by_order_index.return_value = _make_education()

        uc = AddEducationUseCase(repo)
        request = AddEducationRequest(
            profile_id=PROFILE_ID,
            institution="MIT",
            degree="BSc",
            field="CS",
            start_date=datetime(2018, 9, 1),
            order_index=0,
        )
        with pytest.raises(BusinessRuleViolationException):
            await uc.execute(request)

        repo.add.assert_not_awaited()


class TestDeleteEducationUseCase:
    async def test_delete_education_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteEducationUseCase(repo)
        result = await uc.execute(DeleteEducationRequest(education_id="edu-001"))

        assert result.success is True
        repo.delete.assert_awaited_once_with("edu-001")

    async def test_delete_education_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteEducationUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(DeleteEducationRequest(education_id="nonexistent"))


class TestEditEducationUseCase:
    async def test_edit_education_success(self):
        repo = AsyncMock()
        education = _make_education()
        repo.get_by_id.return_value = education
        repo.update.return_value = education

        uc = EditEducationUseCase(repo)
        request = EditEducationRequest(education_id="edu-001", institution="Stanford")
        result = await uc.execute(request)

        assert result.institution == "Stanford"
        repo.update.assert_awaited_once()

    async def test_edit_education_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditEducationUseCase(repo)
        request = EditEducationRequest(
            education_id="nonexistent", institution="Stanford"
        )
        with pytest.raises(NotFoundException):
            await uc.execute(request)
