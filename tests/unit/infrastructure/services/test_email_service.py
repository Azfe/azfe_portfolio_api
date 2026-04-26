from unittest.mock import patch

import pytest

from app.infrastructure.services.null_email_service import NullEmailService
from app.infrastructure.services.resend_email_service import ResendEmailService
from app.shared.interfaces.email_service import EmailMessage

pytestmark = [pytest.mark.unit, pytest.mark.asyncio]

_API_KEY = "re_test_key"
_FROM_ADDRESS = "sender@example.com"


def _make_message(**overrides):
    defaults = {
        "to": "dest@example.com",
        "subject": "Test subject",
        "body_html": "<p>Test</p>",
        "body_text": "Test",
    }
    defaults.update(overrides)
    return EmailMessage(**defaults)


class TestNullEmailService:
    async def test_send_does_not_raise(self):
        service = NullEmailService()
        message = _make_message()
        await service.send(message)

    async def test_send_returns_none(self):
        service = NullEmailService()
        result = await service.send(_make_message())
        assert result is None


class TestResendEmailService:
    async def test_send_calls_resend_sdk_with_correct_params(self):
        service = ResendEmailService(api_key=_API_KEY, from_address=_FROM_ADDRESS)
        message = _make_message()

        mock_response = {"id": "email-id-123"}

        with patch(
            "app.infrastructure.services.resend_email_service.resend.Emails.send",
            return_value=mock_response,
        ) as mock_send:
            await service.send(message)

        mock_send.assert_called_once()
        (params,), _ = mock_send.call_args
        assert params["from"] == _FROM_ADDRESS
        assert params["to"] == [message.to]
        assert params["subject"] == message.subject
        assert params["html"] == message.body_html
        assert params["text"] == message.body_text

    async def test_send_sets_api_key_on_construction(self):
        import resend as resend_module

        ResendEmailService(api_key=_API_KEY, from_address=_FROM_ADDRESS)

        assert resend_module.api_key == _API_KEY

    async def test_send_reraises_exception_on_sdk_failure(self):
        service = ResendEmailService(api_key=_API_KEY, from_address=_FROM_ADDRESS)
        message = _make_message()

        with (
            patch(
                "app.infrastructure.services.resend_email_service.resend.Emails.send",
                side_effect=Exception("Resend API error"),
            ),
            pytest.raises(Exception, match="Resend API error"),
        ):
            await service.send(message)
