"""Unit tests for ContactMessageRepository."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.infrastructure.repositories.contact_message_repository import (
    ContactMessageRepository,
)

from .conftest import make_contact_message_doc


@pytest.fixture
def repo(mock_db):
    return ContactMessageRepository(mock_db)


@pytest.fixture
def collection(repo):
    return repo._collection


class TestContactMessageCRUD:
    @pytest.mark.asyncio
    async def test_add(self, repo, collection):
        entity = MagicMock()
        entity.id = "msg-1"

        result = await repo.add(entity)

        collection.insert_one.assert_called_once()
        assert result is entity

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, collection):
        doc = make_contact_message_doc()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_id("msg-123")

        assert result is not None
        assert result.name == "Jane Doe"
        assert result.status == "pending"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, collection):
        collection.find_one = AsyncMock(return_value=None)

        assert await repo.get_by_id("nope") is None

    @pytest.mark.asyncio
    async def test_delete_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

        assert await repo.delete("msg-1") is True

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo, collection):
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))

        assert await repo.delete("nope") is False


class TestContactMessageListAll:
    @pytest.mark.asyncio
    async def test_list_all_default_sort_by_created_at_desc(self, repo, collection):
        """list_all without sort_by should default to created_at descending."""
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        await repo.list_all()

        cursor.sort.assert_called_once_with("created_at", -1)

    @pytest.mark.asyncio
    async def test_list_all_custom_sort(self, repo, collection):
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        await repo.list_all(sort_by="name", ascending=True)

        cursor.sort.assert_called_once_with("name", 1)


class TestContactMessageSpecialMethods:
    @pytest.mark.asyncio
    async def test_get_pending_messages(self, repo, collection):
        docs = [make_contact_message_doc(_id="m1"), make_contact_message_doc(_id="m2")]
        cursor = collection.find.return_value
        cursor.sort = MagicMock(return_value=cursor)
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.get_pending_messages()

        collection.find.assert_called_with({"status": "pending"})
        cursor.sort.assert_called_with("created_at", -1)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_messages_by_status(self, repo, collection):
        docs = [make_contact_message_doc(status="read")]
        cursor = collection.find.return_value
        cursor.sort = MagicMock(return_value=cursor)
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.get_messages_by_status("read")

        collection.find.assert_called_with({"status": "read"})
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_mark_as_read_success(self, repo, collection):
        collection.update_one = AsyncMock(return_value=MagicMock(modified_count=1))

        result = await repo.mark_as_read("msg-1")

        assert result is True
        call_args = collection.update_one.call_args
        assert call_args[0][0] == {"_id": "msg-1", "status": "pending"}
        update_doc = call_args[0][1]
        assert update_doc["$set"]["status"] == "read"
        assert "read_at" in update_doc["$set"]

    @pytest.mark.asyncio
    async def test_mark_as_read_not_found(self, repo, collection):
        collection.update_one = AsyncMock(return_value=MagicMock(modified_count=0))

        result = await repo.mark_as_read("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_mark_as_replied_success(self, repo, collection):
        collection.update_one = AsyncMock(return_value=MagicMock(modified_count=1))

        result = await repo.mark_as_replied("msg-1")

        assert result is True
        call_args = collection.update_one.call_args
        assert call_args[0][0] == {
            "_id": "msg-1",
            "status": {"$in": ["pending", "read"]},
        }
        update_doc = call_args[0][1]
        assert update_doc["$set"]["status"] == "replied"
        assert "replied_at" in update_doc["$set"]
        assert "read_at" in update_doc["$set"]

    @pytest.mark.asyncio
    async def test_mark_as_replied_not_found(self, repo, collection):
        collection.update_one = AsyncMock(return_value=MagicMock(modified_count=0))

        result = await repo.mark_as_replied("nonexistent")

        assert result is False
