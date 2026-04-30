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


@pytest.mark.unit
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
        assert result.level == "expert"
        assert result.profile_id == PROFILE_ID
        assert result.order_index == 0
        repo.add.assert_awaited_once()

    async def test_add_without_level(self):
        repo = AsyncMock()
        pl = _make_pl(level=None)
        repo.add.return_value = pl

        uc = AddProgrammingLanguageUseCase(repo)
        request = AddProgrammingLanguageRequest(
            profile_id=PROFILE_ID,
            name="Python",
            order_index=0,
        )
        result = await uc.execute(request)

        assert result.name == "Python"
        assert result.level is None
        repo.add.assert_awaited_once()

    async def test_add_returns_response_dto_with_timestamps(self):
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

        assert result.id is not None
        assert result.created_at is not None
        assert result.updated_at is not None


@pytest.mark.unit
class TestDeleteProgrammingLanguageUseCase:
    async def test_delete_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteProgrammingLanguageUseCase(repo)
        result = await uc.execute(
            DeleteProgrammingLanguageRequest(programming_language_id="pl-001")
        )

        assert result.success is True
        repo.delete.assert_awaited_once_with("pl-001")

    async def test_delete_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteProgrammingLanguageUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(
                DeleteProgrammingLanguageRequest(programming_language_id="nonexistent")
            )


@pytest.mark.unit
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

    async def test_edit_partial_update_preserves_level(self):
        repo = AsyncMock()
        pl = _make_pl(name="Python", level="advanced")
        repo.get_by_id.return_value = pl
        repo.update.return_value = pl

        uc = EditProgrammingLanguageUseCase(repo)
        # Only update name — level should remain unchanged
        request = EditProgrammingLanguageRequest(
            programming_language_id="pl-001",
            name="Python 3",
        )
        result = await uc.execute(request)

        assert result.name == "Python 3"
        assert result.level == "advanced"
        repo.update.assert_awaited_once()

    async def test_edit_only_level(self):
        repo = AsyncMock()
        pl = _make_pl(name="Python", level="intermediate")
        repo.get_by_id.return_value = pl
        repo.update.return_value = pl

        uc = EditProgrammingLanguageUseCase(repo)
        request = EditProgrammingLanguageRequest(
            programming_language_id="pl-001",
            level="expert",
        )
        result = await uc.execute(request)

        assert result.level == "expert"
        repo.update.assert_awaited_once()


@pytest.mark.unit
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
        assert result.programming_languages == []

    async def test_list_descending_order(self):
        repo = AsyncMock()
        pls = [
            _make_pl(name="TypeScript", order_index=1),
            _make_pl(name="Python", order_index=0),
        ]
        repo.get_all_ordered.return_value = pls

        uc = ListProgrammingLanguagesUseCase(repo)
        request = ListProgrammingLanguagesRequest(profile_id=PROFILE_ID, ascending=False)
        result = await uc.execute(request)

        assert result.total == 2
        repo.get_all_ordered.assert_awaited_once_with(
            profile_id=PROFILE_ID, ascending=False
        )

    async def test_list_items_have_correct_data(self):
        repo = AsyncMock()
        pls = [_make_pl(name="Python", order_index=0, level="expert")]
        repo.get_all_ordered.return_value = pls

        uc = ListProgrammingLanguagesUseCase(repo)
        request = ListProgrammingLanguagesRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 1
        first = result.programming_languages[0]
        assert first.name == "Python"
        assert first.order_index == 0
        assert first.level == "expert"
        assert first.profile_id == PROFILE_ID
