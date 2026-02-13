"""Tests for Language use cases."""

from unittest.mock import AsyncMock

import pytest

from app.application.dto.language_dto import (
    AddLanguageRequest,
    DeleteLanguageRequest,
    EditLanguageRequest,
    ListLanguagesRequest,
)
from app.application.use_cases.language.add_language import AddLanguageUseCase
from app.application.use_cases.language.delete_language import DeleteLanguageUseCase
from app.application.use_cases.language.edit_language import EditLanguageUseCase
from app.application.use_cases.language.list_languages import ListLanguagesUseCase
from app.domain.entities.language import Language
from app.shared.shared_exceptions import NotFoundException

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"


def _make_language(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "name": "English",
        "order_index": 0,
        "proficiency": "c2",
    }
    defaults.update(overrides)
    return Language.create(**defaults)


class TestAddLanguageUseCase:
    async def test_add_language_success(self):
        repo = AsyncMock()
        lang = _make_language()
        repo.add.return_value = lang

        uc = AddLanguageUseCase(repo)
        request = AddLanguageRequest(
            profile_id=PROFILE_ID,
            name="English",
            order_index=0,
            proficiency="c2",
        )
        result = await uc.execute(request)

        assert result.name == "English"
        repo.add.assert_awaited_once()


class TestDeleteLanguageUseCase:
    async def test_delete_language_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteLanguageUseCase(repo)
        result = await uc.execute(DeleteLanguageRequest(language_id="lang-001"))

        assert result.success is True

    async def test_delete_language_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteLanguageUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(DeleteLanguageRequest(language_id="nonexistent"))


class TestEditLanguageUseCase:
    async def test_edit_language_success(self):
        repo = AsyncMock()
        lang = _make_language()
        repo.get_by_id.return_value = lang
        repo.update.return_value = lang

        uc = EditLanguageUseCase(repo)
        request = EditLanguageRequest(
            language_id="lang-001", name="Spanish", proficiency="b2"
        )
        result = await uc.execute(request)

        assert result.name == "Spanish"
        repo.update.assert_awaited_once()

    async def test_edit_language_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditLanguageUseCase(repo)
        request = EditLanguageRequest(language_id="nonexistent", name="Spanish")
        with pytest.raises(NotFoundException):
            await uc.execute(request)


class TestListLanguagesUseCase:
    async def test_list_languages(self):
        repo = AsyncMock()
        langs = [_make_language(), _make_language(name="Spanish", order_index=1)]
        repo.get_all_ordered.return_value = langs

        uc = ListLanguagesUseCase(repo)
        request = ListLanguagesRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 2
        repo.get_all_ordered.assert_awaited_once_with(
            profile_id=PROFILE_ID, ascending=True
        )

    async def test_list_languages_empty(self):
        repo = AsyncMock()
        repo.get_all_ordered.return_value = []

        uc = ListLanguagesUseCase(repo)
        request = ListLanguagesRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 0
        assert result.languages == []
