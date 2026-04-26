from unittest.mock import AsyncMock

import pytest

from app.application.dto import CreateContactMessageRequest
from app.application.use_cases.contact_message.create_contact_message import (
    CreateContactMessageUseCase,
)
from app.domain.entities.contact_message import ContactMessage

pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


def _make_entity():
    return ContactMessage.create(
        name="Ana García",
        email="ana@example.com",
        message="Hola, me interesa tu trabajo en proyectos backend.",
    )


def _make_request():
    return CreateContactMessageRequest(
        name="Ana García",
        email="ana@example.com",
        message="Hola, me interesa tu trabajo en proyectos backend.",
    )


class TestCreateContactMessageUseCase:
    async def test_execute_returns_response(self):
        repo = AsyncMock()
        email_service = AsyncMock()
        entity = _make_entity()
        repo.add.return_value = entity

        uc = CreateContactMessageUseCase(
            contact_message_repository=repo,
            email_service=email_service,
        )
        response = await uc.execute(_make_request())

        assert response.name == entity.name
        assert response.email == entity.email
        repo.add.assert_awaited_once()

    async def test_execute_calls_email_service_send(self):
        repo = AsyncMock()
        email_service = AsyncMock()
        entity = _make_entity()
        repo.add.return_value = entity

        uc = CreateContactMessageUseCase(
            contact_message_repository=repo,
            email_service=email_service,
        )
        await uc.execute(_make_request())

        email_service.send.assert_awaited_once()
        call_args = email_service.send.call_args[0][0]
        assert entity.name in call_args.subject
        assert entity.email in call_args.body_text
        assert entity.name in call_args.body_html

    async def test_execute_succeeds_when_email_service_raises(self):
        repo = AsyncMock()
        email_service = AsyncMock()
        email_service.send.side_effect = ConnectionRefusedError("SMTP down")
        entity = _make_entity()
        repo.add.return_value = entity

        uc = CreateContactMessageUseCase(
            contact_message_repository=repo,
            email_service=email_service,
        )
        response = await uc.execute(_make_request())

        assert response.name == entity.name
        repo.add.assert_awaited_once()

    async def test_uses_null_email_service_when_none_provided(self):
        repo = AsyncMock()
        entity = _make_entity()
        repo.add.return_value = entity

        uc = CreateContactMessageUseCase(contact_message_repository=repo)
        response = await uc.execute(_make_request())

        assert response.name == entity.name
