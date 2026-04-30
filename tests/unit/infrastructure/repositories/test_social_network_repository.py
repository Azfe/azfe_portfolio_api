"""Unit tests for SocialNetworkRepository.

Covers the platform-specific methods (exists_by_platform, get_by_platform)
and the ordered-repository behaviour (get_all_ordered, reorder).
Generic CRUD, count/exists and find_by are already exercised by
test_ordered_repositories.py for every IOrderedRepository implementation;
they are repeated here only where the assertions are specific to SocialNetwork.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.infrastructure.repositories.social_network_repository import (
    SocialNetworkRepository,
)

from .conftest import make_social_network_doc


@pytest.fixture
def repo(mock_db):
    return SocialNetworkRepository(mock_db)


@pytest.fixture
def collection(repo):
    return repo._collection


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------


class TestSocialNetworkRepositoryCRUD:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_add_returns_entity(self, repo, collection):
        entity = MagicMock()
        entity.id = "sn-1"

        result = await repo.add(entity)

        collection.insert_one.assert_called_once()
        assert result is entity

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, collection):
        doc = make_social_network_doc()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_id("sn-123")

        assert result is not None
        assert result.platform == "LinkedIn"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        assert await repo.get_by_id("nope") is None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_update_returns_entity(self, repo, collection):
        entity = MagicMock()
        entity.id = "sn-1"

        result = await repo.update(entity)

        collection.replace_one.assert_called_once()
        assert result is entity

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_delete_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

        assert await repo.delete("sn-1") is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))

        assert await repo.delete("nope") is False


# ---------------------------------------------------------------------------
# Platform-specific methods
# ---------------------------------------------------------------------------


class TestSocialNetworkRepositoryPlatformMethods:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_exists_by_platform_true(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=1)

        result = await repo.exists_by_platform("profile-123", "LinkedIn")

        collection.count_documents.assert_called_once_with(
            {"profile_id": "profile-123", "platform": "LinkedIn"}
        )
        assert result is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_exists_by_platform_false(self, repo, collection):
        collection.count_documents = AsyncMock(return_value=0)

        result = await repo.exists_by_platform("profile-123", "Twitter")

        assert result is False

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_by_platform_found(self, repo, collection):
        doc = make_social_network_doc(platform="GitHub", url="https://github.com/azfe")
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_platform("profile-123", "GitHub")

        collection.find_one.assert_called_once_with(
            {"profile_id": "profile-123", "platform": "GitHub"}
        )
        assert result is not None
        assert result.platform == "GitHub"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_by_platform_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        result = await repo.get_by_platform("profile-123", "TikTok")

        assert result is None


# ---------------------------------------------------------------------------
# Ordered methods
# ---------------------------------------------------------------------------


class TestSocialNetworkRepositoryOrderedMethods:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_by_order_index_found(self, repo, collection):
        doc = make_social_network_doc(order_index=2)
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_order_index("profile-123", 2)

        collection.find_one.assert_called_once_with(
            {"profile_id": "profile-123", "order_index": 2}
        )
        assert result is not None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_by_order_index_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        assert await repo.get_by_order_index("profile-123", 99) is None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_all_ordered_ascending(self, repo, collection):
        docs = [
            make_social_network_doc(_id="sn-1", order_index=0),
            make_social_network_doc(_id="sn-2", order_index=1),
        ]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.get_all_ordered("profile-123")

        collection.find.assert_called_with({"profile_id": "profile-123"})
        cursor.sort.assert_called_once_with("order_index", 1)
        assert len(result) == 2

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_all_ordered_descending(self, repo, collection):
        docs = [
            make_social_network_doc(_id="sn-2", order_index=1),
            make_social_network_doc(_id="sn-1", order_index=0),
        ]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.get_all_ordered("profile-123", ascending=False)

        cursor.sort.assert_called_once_with("order_index", -1)
        assert len(result) == 2

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_reorder_move_down(self, repo, collection):
        doc = make_social_network_doc(_id="sn-1", order_index=0)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "sn-1", 3)

        collection.update_many.assert_called_once_with(
            {"profile_id": "profile-123", "order_index": {"$gt": 0, "$lte": 3}},
            {"$inc": {"order_index": -1}},
        )
        collection.update_one.assert_called_once_with(
            {"_id": "sn-1"}, {"$set": {"order_index": 3}}
        )

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_reorder_move_up(self, repo, collection):
        doc = make_social_network_doc(_id="sn-1", order_index=4)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "sn-1", 1)

        collection.update_many.assert_called_once_with(
            {"profile_id": "profile-123", "order_index": {"$gte": 1, "$lt": 4}},
            {"$inc": {"order_index": 1}},
        )
        collection.update_one.assert_called_once_with(
            {"_id": "sn-1"}, {"$set": {"order_index": 1}}
        )

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_reorder_same_index_noop(self, repo, collection):
        doc = make_social_network_doc(_id="sn-1", order_index=2)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "sn-1", 2)

        collection.update_many.assert_not_called()
        collection.update_one.assert_not_called()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_reorder_noop_on_missing_entity(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        await repo.reorder("profile-123", "nonexistent", 1)

        collection.update_many.assert_not_called()
        collection.update_one.assert_not_called()


# ---------------------------------------------------------------------------
# Mapper integration
# ---------------------------------------------------------------------------


class TestSocialNetworkRepositoryMapperCalls:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_add_calls_mapper_to_persistence(self, repo, collection):
        entity = MagicMock()
        entity.id = "sn-1"

        with patch.object(
            repo._mapper, "to_persistence", return_value={"_id": "sn-1"}
        ) as mock_mapper:
            await repo.add(entity)
            mock_mapper.assert_called_once_with(entity)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_by_id_calls_mapper_to_domain(self, repo, collection):
        doc = make_social_network_doc()
        collection.find_one = AsyncMock(return_value=doc)

        with patch.object(repo._mapper, "to_domain") as mock_mapper:
            mock_mapper.return_value = MagicMock()
            await repo.get_by_id("sn-123")
            mock_mapper.assert_called_once_with(doc)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_by_platform_calls_mapper_to_domain(self, repo, collection):
        doc = make_social_network_doc(platform="GitHub", url="https://github.com/azfe")
        collection.find_one = AsyncMock(return_value=doc)

        with patch.object(repo._mapper, "to_domain") as mock_mapper:
            mock_mapper.return_value = MagicMock()
            await repo.get_by_platform("profile-123", "GitHub")
            mock_mapper.assert_called_once_with(doc)
