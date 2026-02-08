"""Unit tests for ProfileRepository."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.infrastructure.repositories.profile_repository import ProfileRepository

from .conftest import make_profile_doc


@pytest.fixture
def repo(mock_db):
    return ProfileRepository(mock_db)


@pytest.fixture
def collection(repo):
    return repo._collection


class TestProfileRepositoryAdd:
    @pytest.mark.asyncio
    async def test_add_calls_insert_one(self, repo, collection):
        entity = MagicMock()
        entity.id = "p-1"

        result = await repo.add(entity)

        collection.insert_one.assert_called_once()
        assert result is entity

    @pytest.mark.asyncio
    async def test_add_uses_mapper_to_persistence(self, repo, collection):
        entity = MagicMock()
        entity.id = "p-1"

        with patch.object(repo._mapper, "to_persistence", return_value={"_id": "p-1"}) as mock_mapper:
            await repo.add(entity)
            mock_mapper.assert_called_once_with(entity)
            collection.insert_one.assert_called_once_with({"_id": "p-1"})


class TestProfileRepositoryGetById:
    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, collection):
        doc = make_profile_doc()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_id("profile-123")

        collection.find_one.assert_called_once_with({"_id": "profile-123"})
        assert result is not None
        assert result.id == "profile-123"
        assert result.name == "John Doe"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        result = await repo.get_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_with_optional_fields(self, repo, collection):
        doc = make_profile_doc(bio="A bio", location="NYC", avatar_url="https://img.com/a.jpg")
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_id("profile-123")

        assert result.bio == "A bio"
        assert result.location == "NYC"
        assert result.avatar_url == "https://img.com/a.jpg"


class TestProfileRepositoryUpdate:
    @pytest.mark.asyncio
    async def test_update_calls_replace_one(self, repo, collection):
        entity = MagicMock()
        entity.id = "p-1"

        result = await repo.update(entity)

        collection.replace_one.assert_called_once()
        call_args = collection.replace_one.call_args
        assert call_args[0][0] == {"_id": "p-1"}
        assert result is entity


class TestProfileRepositoryDelete:
    @pytest.mark.asyncio
    async def test_delete_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

        result = await repo.delete("p-1")

        collection.delete_one.assert_called_once_with({"_id": "p-1"})
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))

        result = await repo.delete("nonexistent")

        assert result is False


class TestProfileRepositoryListAll:
    @pytest.mark.asyncio
    async def test_list_all_empty(self, repo, collection):
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        result = await repo.list_all()

        assert result == []

    @pytest.mark.asyncio
    async def test_list_all_with_docs(self, repo, collection):
        docs = [make_profile_doc(_id="p-1"), make_profile_doc(_id="p-2", name="Jane")]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.list_all()

        assert len(result) == 2
        assert result[0].id == "p-1"
        assert result[1].name == "Jane"

    @pytest.mark.asyncio
    async def test_list_all_with_sort(self, repo, collection):
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        await repo.list_all(sort_by="name", ascending=False)

        cursor.sort.assert_called_once_with("name", -1)

    @pytest.mark.asyncio
    async def test_list_all_with_pagination(self, repo, collection):
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        await repo.list_all(skip=10, limit=5)

        cursor.skip.assert_called_once_with(10)
        cursor.limit.assert_called_once_with(5)


class TestProfileRepositoryCount:
    @pytest.mark.asyncio
    async def test_count_no_filters(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=3)

        result = await repo.count()

        collection.count_documents.assert_called_once_with({})
        assert result == 3

    @pytest.mark.asyncio
    async def test_count_with_filters(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=1)

        result = await repo.count({"name": "John"})

        collection.count_documents.assert_called_once_with({"name": "John"})
        assert result == 1


class TestProfileRepositoryExists:
    @pytest.mark.asyncio
    async def test_exists_true(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=1)

        result = await repo.exists("p-1")

        collection.count_documents.assert_called_once_with({"_id": "p-1"})
        assert result is True

    @pytest.mark.asyncio
    async def test_exists_false(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=0)

        result = await repo.exists("nonexistent")

        assert result is False


class TestProfileRepositoryFindBy:
    @pytest.mark.asyncio
    async def test_find_by_filters(self, repo, collection):
        docs = [make_profile_doc()]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.find_by(name="John Doe")

        collection.find.assert_called_with({"name": "John Doe"})
        assert len(result) == 1


class TestProfileRepositorySpecialMethods:
    @pytest.mark.asyncio
    async def test_get_profile_found(self, repo, collection):
        doc = make_profile_doc()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_profile()

        collection.find_one.assert_called_once_with()
        assert result is not None
        assert result.name == "John Doe"

    @pytest.mark.asyncio
    async def test_get_profile_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        result = await repo.get_profile()

        assert result is None

    @pytest.mark.asyncio
    async def test_profile_exists_true(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=1)

        result = await repo.profile_exists()

        collection.count_documents.assert_called_once_with({})
        assert result is True

    @pytest.mark.asyncio
    async def test_profile_exists_false(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=0)

        result = await repo.profile_exists()

        assert result is False
