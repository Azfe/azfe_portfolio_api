import email.message

import aiosmtplib

from app.shared.interfaces.email_service import EmailMessage, IEmailService


class SmtpEmailService(IEmailService):
    def __init__(self, settings) -> None:
        self._settings = settings

    async def send(self, message: EmailMessage) -> None:
        msg = email.message.EmailMessage()
        msg["From"] = self._settings.SMTP_FROM
        msg["To"] = message.to
        msg["Subject"] = message.subject
        msg.set_content(message.body_text)
        msg.add_alternative(message.body_html, subtype="html")

        await aiosmtplib.send(
            msg,
            hostname=self._settings.SMTP_HOST,
            port=self._settings.SMTP_PORT,
            username=self._settings.SMTP_USER,
            password=self._settings.SMTP_PASSWORD,
            start_tls=self._settings.SMTP_USE_TLS,
        )
