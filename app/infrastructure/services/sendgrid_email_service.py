import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Mail

from app.shared.interfaces.email_service import EmailMessage, IEmailService

logger = logging.getLogger(__name__)


class SendGridEmailService(IEmailService):
    def __init__(self, settings) -> None:
        self._settings = settings
        api_key = settings.SENDGRID_API_KEY
        logger.info(
            "SendGridEmailService initialised: api_key_length=%d from_email=%r",
            len(api_key),
            settings.SMTP_FROM,
        )
        self._client = SendGridAPIClient(api_key=api_key)

    async def send(self, message: EmailMessage) -> None:
        from_email = self._settings.SMTP_FROM
        to_email = message.to
        subject = message.subject

        logger.info(
            "SendGrid send: from=%r to=%r subject=%r",
            from_email,
            to_email,
            subject,
        )

        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
        )
        mail.add_content(Content("text/plain", message.body_text))
        mail.add_content(Content("text/html", message.body_html))

        try:
            response = self._client.send(mail)
            logger.info(
                "SendGrid response: status_code=%s to=%r",
                response.status_code,
                to_email,
            )
        except Exception as exc:
            status_code = getattr(exc, "status_code", None)
            body = getattr(exc, "body", None) or getattr(exc, "message", None)
            logger.error(
                "SendGrid request failed: status_code=%s body=%r error=%s",
                status_code,
                body,
                exc,
            )
            raise
