"""Tests for ContactMessage use cases (Delete and List).

CreateContactMessageUseCase is covered in test_create_contact_message.py.
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.application.dto import DeleteContactMessageRequest, ListContactMessagesRequest
from app.application.use_cases.contact_message.delete_contact_message import (
    DeleteContactMessageUseCase,
)
from app.application.use_cases.contact_message.list_contact_messages import (
    ListContactMessagesUseCase,
)
from app.domain.entities.contact_message import ContactMessage
from app.shared.shared_exceptions import NotFoundException

pytestmark = [pytest.mark.unit, pytest.mark.asyncio]

_BASE_TIME = datetime(2024, 6, 1, 12, 0, 0)


def _make_entity(
    name: str = "Ana García",
    email: str = "ana@example.com",
    message: str = "Hola, me interesa tu trabajo en proyectos backend.",
    created_at: datetime | None = None,
) -> ContactMessage:
    entity = ContactMessage.create(name=name, email=email, message=message)
    if created_at is not None:
        entity.created_at = created_at
    return entity


class TestDeleteContactMessageUseCase:
    @pytest.mark.unit
    async def test_delete_existing_message_returns_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteContactMessageUseCase(contact_message_repository=repo)
        result = await uc.execute(DeleteContactMessageRequest(message_id="msg-001"))

        assert result.success is True
        repo.delete.assert_awaited_once_with("msg-001")

    @pytest.mark.unit
    async def test_delete_nonexistent_message_raises_not_found(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteContactMessageUseCase(contact_message_repository=repo)
        with pytest.raises(NotFoundException):
            await uc.execute(DeleteContactMessageRequest(message_id="nonexistent"))

        repo.delete.assert_awaited_once_with("nonexistent")


class TestListContactMessagesUseCase:
    @pytest.mark.unit
    async def test_list_returns_empty_when_no_messages(self):
        repo = AsyncMock()
        repo.list_all.return_value = []

        uc = ListContactMessagesUseCase(contact_message_repository=repo)
        result = await uc.execute(ListContactMessagesRequest())

        assert result.total == 0
        assert result.messages == []
        repo.list_all.assert_awaited_once()

    @pytest.mark.unit
    async def test_list_returns_all_messages(self):
        repo = AsyncMock()
        entities = [
            _make_entity(name="Ana García"),
            _make_entity(name="Carlos López", email="carlos@example.com"),
            _make_entity(name="María Ruiz", email="maria@example.com"),
        ]
        repo.list_all.return_value = entities

        uc = ListContactMessagesUseCase(contact_message_repository=repo)
        result = await uc.execute(ListContactMessagesRequest())

        assert result.total == 3
        assert len(result.messages) == 3

    @pytest.mark.unit
    async def test_list_ascending_returns_oldest_first(self):
        repo = AsyncMock()
        oldest = _make_entity(name="Primero", created_at=_BASE_TIME)
        middle = _make_entity(
            name="Segundo",
            email="segundo@example.com",
            created_at=_BASE_TIME + timedelta(hours=1),
        )
        newest = _make_entity(
            name="Tercero",
            email="tercero@example.com",
            created_at=_BASE_TIME + timedelta(hours=2),
        )
        # Deliver in arbitrary order from the repo
        repo.list_all.return_value = [newest, oldest, middle]

        uc = ListContactMessagesUseCase(contact_message_repository=repo)
        result = await uc.execute(ListContactMessagesRequest(ascending=True))

        timestamps = [m.created_at for m in result.messages]
        assert timestamps == sorted(timestamps)
        assert result.messages[0].name == "Primero"
        assert result.messages[-1].name == "Tercero"

    @pytest.mark.unit
    async def test_list_descending_returns_newest_first(self):
        repo = AsyncMock()
        oldest = _make_entity(name="Primero", created_at=_BASE_TIME)
        middle = _make_entity(
            name="Segundo",
            email="segundo@example.com",
            created_at=_BASE_TIME + timedelta(hours=1),
        )
        newest = _make_entity(
            name="Tercero",
            email="tercero@example.com",
            created_at=_BASE_TIME + timedelta(hours=2),
        )
        # Deliver in arbitrary order from the repo
        repo.list_all.return_value = [oldest, newest, middle]

        uc = ListContactMessagesUseCase(contact_message_repository=repo)
        result = await uc.execute(ListContactMessagesRequest(ascending=False))

        timestamps = [m.created_at for m in result.messages]
        assert timestamps == sorted(timestamps, reverse=True)
        assert result.messages[0].name == "Tercero"
        assert result.messages[-1].name == "Primero"
