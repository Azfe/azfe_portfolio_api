from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.infrastructure.services.null_email_service import NullEmailService
from app.infrastructure.services.smtp_email_service import SmtpEmailService
from app.shared.interfaces.email_service import EmailMessage

pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


def _make_message(**overrides):
    defaults = {
        "to": "dest@example.com",
        "subject": "Test subject",
        "body_html": "<p>Test</p>",
        "body_text": "Test",
    }
    defaults.update(overrides)
    return EmailMessage(**defaults)


def _make_settings(**overrides):
    settings = MagicMock()
    settings.SMTP_HOST = "smtp.gmail.com"
    settings.SMTP_PORT = 587
    settings.SMTP_USER = "user@example.com"
    settings.SMTP_PASSWORD = "secret"
    settings.SMTP_FROM = "sender@example.com"
    settings.SMTP_USE_TLS = True
    for key, value in overrides.items():
        setattr(settings, key, value)
    return settings


class TestNullEmailService:
    async def test_send_does_not_raise(self):
        service = NullEmailService()
        message = _make_message()
        await service.send(message)

    async def test_send_returns_none(self):
        service = NullEmailService()
        result = await service.send(_make_message())
        assert result is None


class TestSmtpEmailService:
    async def test_send_calls_aiosmtplib_with_correct_params(self):
        settings = _make_settings()
        service = SmtpEmailService(settings)
        message = _make_message()

        with patch(
            "app.infrastructure.services.smtp_email_service.aiosmtplib.send",
            new_callable=AsyncMock,
        ) as mock_send:
            await service.send(message)

        mock_send.assert_awaited_once()
        _, kwargs = mock_send.call_args
        assert kwargs["hostname"] == settings.SMTP_HOST
        assert kwargs["port"] == settings.SMTP_PORT
        assert kwargs["username"] == settings.SMTP_USER
        assert kwargs["password"] == settings.SMTP_PASSWORD
        assert kwargs["start_tls"] == settings.SMTP_USE_TLS

    async def test_send_reraises_exception_on_failure(self):
        settings = _make_settings()
        service = SmtpEmailService(settings)
        message = _make_message()

        with (
            patch(
                "app.infrastructure.services.smtp_email_service.aiosmtplib.send",
                new_callable=AsyncMock,
                side_effect=ConnectionRefusedError("SMTP connection refused"),
            ),
            pytest.raises(ConnectionRefusedError),
        ):
            await service.send(message)
