"""Unit tests for ContactInformationRepository."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.infrastructure.repositories.contact_information_repository import (
    ContactInformationRepository,
)

from .conftest import make_contact_info_doc


@pytest.fixture
def repo(mock_db):
    return ContactInformationRepository(mock_db)


@pytest.fixture
def collection(repo):
    return repo._collection


class TestContactInformationCRUD:
    @pytest.mark.asyncio
    async def test_add(self, repo, collection):
        entity = MagicMock()
        entity.id = "c-1"

        result = await repo.add(entity)

        collection.insert_one.assert_called_once()
        assert result is entity

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, collection):
        doc = make_contact_info_doc()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_id("contact-123")

        assert result is not None
        assert result.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        assert await repo.get_by_id("nope") is None

    @pytest.mark.asyncio
    async def test_update(self, repo, collection):
        entity = MagicMock()
        entity.id = "c-1"

        result = await repo.update(entity)

        collection.replace_one.assert_called_once()
        assert result is entity

    @pytest.mark.asyncio
    async def test_delete_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

        assert await repo.delete("c-1") is True

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))

        assert await repo.delete("nope") is False


class TestContactInformationSpecialMethods:
    @pytest.mark.asyncio
    async def test_get_by_profile_id_found(self, repo, collection):
        doc = make_contact_info_doc()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_profile_id("profile-123")

        collection.find_one.assert_called_once_with({"profile_id": "profile-123"})
        assert result is not None
        assert result.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_by_profile_id_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        result = await repo.get_by_profile_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_count(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=1)

        assert await repo.count() == 1

    @pytest.mark.asyncio
    async def test_exists_true(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=1)

        assert await repo.exists("c-1") is True

    @pytest.mark.asyncio
    async def test_exists_false(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=0)

        assert await repo.exists("nope") is False
