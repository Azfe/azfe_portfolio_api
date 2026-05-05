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


class TestContactMessageUpdate:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_update_calls_replace_one_without_id(self, repo, collection):
        """update() should strip _id from the doc and call replace_one."""
        entity = MagicMock()
        entity.id = "msg-upd-1"

        result = await repo.update(entity)

        collection.replace_one.assert_called_once()
        call_args = collection.replace_one.call_args
        filter_arg = call_args[0][0]
        replacement_doc = call_args[0][1]
        assert filter_arg == {"_id": "msg-upd-1"}
        assert "_id" not in replacement_doc
        assert result is entity

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_update_returns_same_entity(self, repo, collection):
        """update() must return the exact entity that was passed in."""
        entity = MagicMock()
        entity.id = "msg-upd-2"

        returned = await repo.update(entity)

        assert returned is entity


class TestContactMessageCountAndExists:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_count_without_filters_passes_empty_dict(self, repo, collection):
        """count(None) should call count_documents with {}."""
        collection.count_documents = AsyncMock(return_value=5)

        result = await repo.count(filters=None)

        collection.count_documents.assert_called_once_with({})
        assert result == 5

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_count_with_filters(self, repo, collection):
        """count() with an explicit filter dict should forward it unchanged."""
        collection.count_documents = AsyncMock(return_value=3)

        result = await repo.count(filters={"status": "pending"})

        collection.count_documents.assert_called_once_with({"status": "pending"})
        assert result == 3

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_exists_returns_true_when_count_positive(self, repo, collection):
        """exists() should return True when count_documents > 0."""
        collection.count_documents = AsyncMock(return_value=1)

        result = await repo.exists("msg-123")

        collection.count_documents.assert_called_once_with({"_id": "msg-123"})
        assert result is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_exists_returns_false_when_count_zero(self, repo, collection):
        """exists() should return False when count_documents == 0."""
        collection.count_documents = AsyncMock(return_value=0)

        result = await repo.exists("ghost-id")

        assert result is False


class TestContactMessageFindBy:
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_find_by_returns_matching_entities(self, repo, collection):
        """find_by() should pass kwargs as a filter and return mapped entities."""
        from .conftest import make_contact_message_doc

        docs = [
            make_contact_message_doc(_id="m1", status="read"),
            make_contact_message_doc(_id="m2", status="read"),
        ]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.find_by(status="read")

        collection.find.assert_called_once_with({"status": "read"})
        assert len(result) == 2

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_find_by_returns_empty_list_when_no_matches(self, repo, collection):
        """find_by() should return an empty list when the cursor yields nothing."""
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        result = await repo.find_by(status="nonexistent")

        assert result == []

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_find_by_multiple_filters(self, repo, collection):
        """find_by() should forward all kwargs as a combined filter."""
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        await repo.find_by(status="pending", name="Jane Doe")

        collection.find.assert_called_once_with({"status": "pending", "name": "Jane Doe"})
