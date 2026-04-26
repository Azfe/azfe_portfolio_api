import logging

import resend

from app.shared.interfaces.email_service import EmailMessage, IEmailService

logger = logging.getLogger(__name__)


class ResendEmailService(IEmailService):
    """Email service implementation backed by the Resend API.

    Resend's Python SDK is synchronous, but the call is lightweight enough
    to run directly from an async context without blocking the event loop
    in any meaningful way for a low-volume notification use case.
    If throughput becomes a concern, wrap with ``asyncio.to_thread``.
    """

    def __init__(self, api_key: str, from_address: str) -> None:
        resend.api_key = api_key
        self._from_address = from_address

    async def send(self, message: EmailMessage) -> None:
        params: resend.Emails.SendParams = {
            "from": self._from_address,
            "to": [message.to],
            "subject": message.subject,
            "html": message.body_html,
            "text": message.body_text,
        }
        response = resend.Emails.send(params)
        logger.debug("ResendEmailService: email sent id=%s to=%s", response["id"], message.to)
