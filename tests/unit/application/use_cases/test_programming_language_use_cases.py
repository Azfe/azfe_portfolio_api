"""Tests for ProgrammingLanguage use cases."""

from unittest.mock import AsyncMock

import pytest

from app.application.dto.programming_language_dto import (
    AddProgrammingLanguageRequest,
    DeleteProgrammingLanguageRequest,
    EditProgrammingLanguageRequest,
    ListProgrammingLanguagesRequest,
)
from app.application.use_cases.programming_language.add_programming_language import (
    AddProgrammingLanguageUseCase,
)
from app.application.use_cases.programming_language.delete_programming_language import (
    DeleteProgrammingLanguageUseCase,
)
from app.application.use_cases.programming_language.edit_programming_language import (
    EditProgrammingLanguageUseCase,
)
from app.application.use_cases.programming_language.list_programming_languages import (
    ListProgrammingLanguagesUseCase,
)
from app.domain.entities.programming_language import ProgrammingLanguage
from app.shared.shared_exceptions import NotFoundException

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"


def _make_pl(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "name": "Python",
        "order_index": 0,
        "level": "expert",
    }
    defaults.update(overrides)
    return ProgrammingLanguage.create(**defaults)


class TestAddProgrammingLanguageUseCase:
    async def test_add_success(self):
        repo = AsyncMock()
        pl = _make_pl()
        repo.add.return_value = pl

        uc = AddProgrammingLanguageUseCase(repo)
        request = AddProgrammingLanguageRequest(
            profile_id=PROFILE_ID,
            name="Python",
            order_index=0,
            level="expert",
        )
        result = await uc.execute(request)

        assert result.name == "Python"
        repo.add.assert_awaited_once()


class TestDeleteProgrammingLanguageUseCase:
    async def test_delete_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteProgrammingLanguageUseCase(repo)
        result = await uc.execute(
            DeleteProgrammingLanguageRequest(programming_language_id="pl-001")
        )

        assert result.success is True

    async def test_delete_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteProgrammingLanguageUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(
                DeleteProgrammingLanguageRequest(programming_language_id="nonexistent")
            )


class TestEditProgrammingLanguageUseCase:
    async def test_edit_success(self):
        repo = AsyncMock()
        pl = _make_pl()
        repo.get_by_id.return_value = pl
        repo.update.return_value = pl

        uc = EditProgrammingLanguageUseCase(repo)
        request = EditProgrammingLanguageRequest(
            programming_language_id="pl-001", name="Go", level="intermediate"
        )
        result = await uc.execute(request)

        assert result.name == "Go"
        repo.update.assert_awaited_once()

    async def test_edit_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditProgrammingLanguageUseCase(repo)
        request = EditProgrammingLanguageRequest(
            programming_language_id="nonexistent", name="Go"
        )
        with pytest.raises(NotFoundException):
            await uc.execute(request)


class TestListProgrammingLanguagesUseCase:
    async def test_list_success(self):
        repo = AsyncMock()
        pls = [_make_pl(), _make_pl(name="Go", order_index=1)]
        repo.get_all_ordered.return_value = pls

        uc = ListProgrammingLanguagesUseCase(repo)
        request = ListProgrammingLanguagesRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 2
        repo.get_all_ordered.assert_awaited_once_with(
            profile_id=PROFILE_ID, ascending=True
        )

    async def test_list_empty(self):
        repo = AsyncMock()
        repo.get_all_ordered.return_value = []

        uc = ListProgrammingLanguagesUseCase(repo)
        request = ListProgrammingLanguagesRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 0
