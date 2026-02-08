"""Unit tests for WorkExperienceRepository (ordered repository pattern)."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.infrastructure.repositories.experience_repository import (
    WorkExperienceRepository,
)

from .conftest import make_work_experience_doc


@pytest.fixture
def repo(mock_db):
    return WorkExperienceRepository(mock_db)


@pytest.fixture
def collection(repo):
    return repo._collection


class TestWorkExperienceAdd:
    @pytest.mark.asyncio
    async def test_add_calls_insert_one(self, repo, collection):
        entity = MagicMock()
        entity.id = "exp-1"

        result = await repo.add(entity)

        collection.insert_one.assert_called_once()
        assert result is entity

    @pytest.mark.asyncio
    async def test_add_uses_mapper(self, repo, collection):
        entity = MagicMock()
        entity.id = "exp-1"
        expected_doc = {"_id": "exp-1", "role": "Dev"}

        with patch.object(repo._mapper, "to_persistence", return_value=expected_doc) as mock_mapper:
            await repo.add(entity)
            mock_mapper.assert_called_once_with(entity)
            collection.insert_one.assert_called_once_with(expected_doc)


class TestWorkExperienceGetById:
    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, collection):
        doc = make_work_experience_doc()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_id("exp-123")

        collection.find_one.assert_called_once_with({"_id": "exp-123"})
        assert result is not None
        assert result.role == "Developer"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        result = await repo.get_by_id("nonexistent")

        assert result is None


class TestWorkExperienceUpdate:
    @pytest.mark.asyncio
    async def test_update_calls_replace_one(self, repo, collection):
        entity = MagicMock()
        entity.id = "exp-1"

        result = await repo.update(entity)

        collection.replace_one.assert_called_once()
        assert collection.replace_one.call_args[0][0] == {"_id": "exp-1"}
        assert result is entity


class TestWorkExperienceDelete:
    @pytest.mark.asyncio
    async def test_delete_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

        assert await repo.delete("exp-1") is True

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))

        assert await repo.delete("nonexistent") is False


class TestWorkExperienceListAll:
    @pytest.mark.asyncio
    async def test_list_all_returns_entities(self, repo, collection):
        docs = [make_work_experience_doc(_id="e1"), make_work_experience_doc(_id="e2", role="PM")]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.list_all()

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_list_all_with_sort(self, repo, collection):
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        await repo.list_all(sort_by="start_date", ascending=True)

        cursor.sort.assert_called_once_with("start_date", 1)


class TestWorkExperienceOrderedMethods:
    @pytest.mark.asyncio
    async def test_get_by_order_index_found(self, repo, collection):
        doc = make_work_experience_doc(order_index=2)
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_order_index("profile-123", 2)

        collection.find_one.assert_called_once_with(
            {"profile_id": "profile-123", "order_index": 2}
        )
        assert result is not None
        assert result.order_index == 2

    @pytest.mark.asyncio
    async def test_get_by_order_index_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        result = await repo.get_by_order_index("profile-123", 99)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_ordered_ascending(self, repo, collection):
        docs = [
            make_work_experience_doc(_id="e1", order_index=0),
            make_work_experience_doc(_id="e2", order_index=1),
        ]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.get_all_ordered("profile-123", ascending=True)

        collection.find.assert_called_with({"profile_id": "profile-123"})
        cursor.sort.assert_called_once_with("order_index", 1)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_all_ordered_descending(self, repo, collection):
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        await repo.get_all_ordered("profile-123", ascending=False)

        cursor.sort.assert_called_once_with("order_index", -1)


class TestWorkExperienceReorder:
    @pytest.mark.asyncio
    async def test_reorder_entity_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        await repo.reorder("profile-123", "nonexistent", 3)

        collection.update_many.assert_not_called()
        collection.update_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_reorder_same_index_noop(self, repo, collection):
        doc = make_work_experience_doc(order_index=2)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "exp-123", 2)

        collection.update_many.assert_not_called()
        collection.update_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_reorder_move_down(self, repo, collection):
        """Moving from index 1 to index 3 (down): items 2,3 shift up (-1)."""
        doc = make_work_experience_doc(_id="exp-1", order_index=1)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "exp-1", 3)

        collection.update_many.assert_called_once_with(
            {
                "profile_id": "profile-123",
                "order_index": {"$gt": 1, "$lte": 3},
            },
            {"$inc": {"order_index": -1}},
        )
        collection.update_one.assert_called_once_with(
            {"_id": "exp-1"}, {"$set": {"order_index": 3}}
        )

    @pytest.mark.asyncio
    async def test_reorder_move_up(self, repo, collection):
        """Moving from index 3 to index 1 (up): items 1,2 shift down (+1)."""
        doc = make_work_experience_doc(_id="exp-1", order_index=3)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "exp-1", 1)

        collection.update_many.assert_called_once_with(
            {
                "profile_id": "profile-123",
                "order_index": {"$gte": 1, "$lt": 3},
            },
            {"$inc": {"order_index": 1}},
        )
        collection.update_one.assert_called_once_with(
            {"_id": "exp-1"}, {"$set": {"order_index": 1}}
        )


class TestWorkExperienceCountAndExists:
    @pytest.mark.asyncio
    async def test_count(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=5)

        assert await repo.count() == 5

    @pytest.mark.asyncio
    async def test_exists_true(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=1)

        assert await repo.exists("exp-1") is True

    @pytest.mark.asyncio
    async def test_exists_false(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=0)

        assert await repo.exists("nope") is False
