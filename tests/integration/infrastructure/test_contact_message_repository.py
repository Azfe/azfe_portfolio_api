"""Integration tests for ContactMessageRepository against real MongoDB."""

from datetime import datetime

from app.infrastructure.repositories import ContactMessageRepository

from .conftest import make_contact_message


class TestContactMessageRepositoryCRUD:
    async def test_add_and_retrieve(
        self, contact_message_repo: ContactMessageRepository
    ):
        msg = make_contact_message()
        await contact_message_repo.add(msg)

        fetched = await contact_message_repo.get_by_id(msg.id)
        assert fetched is not None
        assert fetched.name == "Jane Doe"
        assert fetched.email == "jane@example.com"
        assert fetched.status == "pending"

    async def test_update(self, contact_message_repo: ContactMessageRepository):
        msg = make_contact_message()
        await contact_message_repo.add(msg)

        updated = make_contact_message(
            name="Updated Name",
            message="This is an updated message for the contact form.",
        )
        await contact_message_repo.update(updated)

        fetched = await contact_message_repo.get_by_id(msg.id)
        assert fetched is not None
        assert fetched.name == "Updated Name"

    async def test_delete(self, contact_message_repo: ContactMessageRepository):
        msg = make_contact_message()
        await contact_message_repo.add(msg)

        assert await contact_message_repo.delete(msg.id) is True
        assert await contact_message_repo.get_by_id(msg.id) is None

    async def test_delete_nonexistent(
        self, contact_message_repo: ContactMessageRepository
    ):
        assert await contact_message_repo.delete("nonexistent") is False

    async def test_list_all(self, contact_message_repo: ContactMessageRepository):
        await contact_message_repo.add(
            make_contact_message(id="m1", created_at=datetime(2024, 1, 1))
        )
        await contact_message_repo.add(
            make_contact_message(id="m2", created_at=datetime(2024, 6, 1))
        )

        result = await contact_message_repo.list_all()
        assert len(result) == 2

    async def test_count(self, contact_message_repo: ContactMessageRepository):
        assert await contact_message_repo.count() == 0
        await contact_message_repo.add(make_contact_message())
        assert await contact_message_repo.count() == 1

    async def test_exists(self, contact_message_repo: ContactMessageRepository):
        msg = make_contact_message()
        await contact_message_repo.add(msg)

        assert await contact_message_repo.exists(msg.id) is True
        assert await contact_message_repo.exists("nonexistent") is False


class TestContactMessageRepositoryStatusQueries:
    async def test_get_pending_messages(
        self, contact_message_repo: ContactMessageRepository
    ):
        await contact_message_repo.add(make_contact_message(id="m1"))
        await contact_message_repo.add(make_contact_message(id="m2"))
        await contact_message_repo.add(make_contact_message(id="m3", status="read"))

        result = await contact_message_repo.get_pending_messages()
        assert len(result) == 2
        assert all(m.status == "pending" for m in result)

    async def test_get_pending_messages_empty(
        self, contact_message_repo: ContactMessageRepository
    ):
        result = await contact_message_repo.get_pending_messages()
        assert result == []

    async def test_get_messages_by_status(
        self, contact_message_repo: ContactMessageRepository
    ):
        await contact_message_repo.add(make_contact_message(id="m1"))
        await contact_message_repo.add(make_contact_message(id="m2", status="read"))
        await contact_message_repo.add(make_contact_message(id="m3", status="replied"))

        pending = await contact_message_repo.get_messages_by_status("pending")
        assert len(pending) == 1

        read = await contact_message_repo.get_messages_by_status("read")
        assert len(read) == 1

        replied = await contact_message_repo.get_messages_by_status("replied")
        assert len(replied) == 1


class TestContactMessageRepositoryMarkOperations:
    async def test_mark_as_read(self, contact_message_repo: ContactMessageRepository):
        msg = make_contact_message()
        await contact_message_repo.add(msg)

        result = await contact_message_repo.mark_as_read(msg.id)
        assert result is True

        fetched = await contact_message_repo.get_by_id(msg.id)
        assert fetched is not None
        assert fetched.status == "read"
        assert fetched.read_at is not None

    async def test_mark_as_read_nonexistent(
        self, contact_message_repo: ContactMessageRepository
    ):
        result = await contact_message_repo.mark_as_read("nonexistent")
        assert result is False

    async def test_mark_as_replied(
        self, contact_message_repo: ContactMessageRepository
    ):
        msg = make_contact_message()
        await contact_message_repo.add(msg)

        result = await contact_message_repo.mark_as_replied(msg.id)
        assert result is True

        fetched = await contact_message_repo.get_by_id(msg.id)
        assert fetched is not None
        assert fetched.status == "replied"
        assert fetched.replied_at is not None
        assert fetched.read_at is not None

    async def test_mark_as_replied_nonexistent(
        self, contact_message_repo: ContactMessageRepository
    ):
        result = await contact_message_repo.mark_as_replied("nonexistent")
        assert result is False

    async def test_mark_read_then_replied(
        self, contact_message_repo: ContactMessageRepository
    ):
        msg = make_contact_message()
        await contact_message_repo.add(msg)

        await contact_message_repo.mark_as_read(msg.id)
        await contact_message_repo.mark_as_replied(msg.id)

        fetched = await contact_message_repo.get_by_id(msg.id)
        assert fetched is not None
        assert fetched.status == "replied"
        assert fetched.read_at is not None
        assert fetched.replied_at is not None
