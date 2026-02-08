"""Unit tests for SkillRepository (unique name + ordered repository)."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.infrastructure.repositories.skill_repository import SkillRepository

from .conftest import make_skill_doc


@pytest.fixture
def repo(mock_db):
    return SkillRepository(mock_db)


@pytest.fixture
def collection(repo):
    return repo._collection


class TestSkillRepositoryCRUD:
    @pytest.mark.asyncio
    async def test_add(self, repo, collection):
        entity = MagicMock()
        entity.id = "s-1"

        result = await repo.add(entity)

        collection.insert_one.assert_called_once()
        assert result is entity

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, collection):
        doc = make_skill_doc()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_id("skill-123")

        assert result is not None
        assert result.name == "Python"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        assert await repo.get_by_id("nope") is None

    @pytest.mark.asyncio
    async def test_update(self, repo, collection):
        entity = MagicMock()
        entity.id = "s-1"

        result = await repo.update(entity)

        collection.replace_one.assert_called_once()
        assert result is entity

    @pytest.mark.asyncio
    async def test_delete_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

        assert await repo.delete("s-1") is True

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))

        assert await repo.delete("nope") is False


class TestSkillRepositoryUniqueNameMethods:
    @pytest.mark.asyncio
    async def test_exists_by_name_true(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=1)

        result = await repo.exists_by_name("profile-123", "Python")

        collection.count_documents.assert_called_once_with(
            {"profile_id": "profile-123", "name": "Python"}
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_exists_by_name_false(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=0)

        result = await repo.exists_by_name("profile-123", "Rust")

        assert result is False

    @pytest.mark.asyncio
    async def test_get_by_name_found(self, repo, collection):
        doc = make_skill_doc(name="FastAPI")
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_name("profile-123", "FastAPI")

        collection.find_one.assert_called_once_with(
            {"profile_id": "profile-123", "name": "FastAPI"}
        )
        assert result is not None
        assert result.name == "FastAPI"

    @pytest.mark.asyncio
    async def test_get_by_name_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        result = await repo.get_by_name("profile-123", "Rust")

        assert result is None


class TestSkillRepositoryOrderedMethods:
    @pytest.mark.asyncio
    async def test_get_by_order_index(self, repo, collection):
        doc = make_skill_doc(order_index=0)
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_order_index("profile-123", 0)

        collection.find_one.assert_called_once_with(
            {"profile_id": "profile-123", "order_index": 0}
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_get_all_ordered(self, repo, collection):
        docs = [make_skill_doc(_id="s1", order_index=0), make_skill_doc(_id="s2", order_index=1)]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.get_all_ordered("profile-123")

        collection.find.assert_called_with({"profile_id": "profile-123"})
        cursor.sort.assert_called_once_with("order_index", 1)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_reorder_move_down(self, repo, collection):
        doc = make_skill_doc(_id="s-1", order_index=0)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "s-1", 2)

        collection.update_many.assert_called_once()
        collection.update_one.assert_called_once_with(
            {"_id": "s-1"}, {"$set": {"order_index": 2}}
        )

    @pytest.mark.asyncio
    async def test_reorder_same_index_noop(self, repo, collection):
        doc = make_skill_doc(_id="s-1", order_index=5)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "s-1", 5)

        collection.update_many.assert_not_called()
        collection.update_one.assert_not_called()


class TestSkillRepositoryMapperValidation:
    @pytest.mark.asyncio
    async def test_add_calls_mapper_to_persistence(self, repo, collection):
        entity = MagicMock()
        entity.id = "s-1"

        with patch.object(repo._mapper, "to_persistence", return_value={"_id": "s-1"}) as mock_mapper:
            await repo.add(entity)
            mock_mapper.assert_called_once_with(entity)

    @pytest.mark.asyncio
    async def test_get_by_id_calls_mapper_to_domain(self, repo, collection):
        doc = make_skill_doc()
        collection.find_one = AsyncMock(return_value=doc)

        with patch.object(repo._mapper, "to_domain") as mock_mapper:
            mock_mapper.return_value = MagicMock()
            await repo.get_by_id("skill-123")
            mock_mapper.assert_called_once_with(doc)
