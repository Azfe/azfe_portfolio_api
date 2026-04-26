import logging

from app.shared.interfaces.email_service import EmailMessage, IEmailService

logger = logging.getLogger(__name__)


class NullEmailService(IEmailService):
    async def send(self, message: EmailMessage) -> None:
        logger.debug("NullEmailService: email not sent (email disabled) to=%s", message.to)
