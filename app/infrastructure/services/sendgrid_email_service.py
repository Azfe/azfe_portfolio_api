import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Email, Mail, To

from app.shared.interfaces.email_service import EmailMessage, IEmailService

logger = logging.getLogger(__name__)


class SendGridEmailService(IEmailService):
    def __init__(self, settings) -> None:
        self._settings = settings
        self._client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    async def send(self, message: EmailMessage) -> None:
        mail = Mail(
            from_email=Email(self._settings.SMTP_FROM),
            to_emails=To(message.to),
            subject=message.subject,
        )
        mail.add_content(Content("text/plain", message.body_text))
        mail.add_content(Content("text/html", message.body_html))

        response = self._client.send(mail)
        logger.info(
            "SendGrid email sent to=%s status_code=%s",
            message.to,
            response.status_code,
        )
