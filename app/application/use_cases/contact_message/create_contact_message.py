import logging

from app.application.dto import ContactMessageResponse, CreateContactMessageRequest
from app.config.settings import settings
from app.domain.entities import ContactMessage
from app.infrastructure.services.null_email_service import NullEmailService
from app.shared.interfaces import ICommandUseCase, IContactMessageRepository
from app.shared.interfaces.email_service import EmailMessage, IEmailService

logger = logging.getLogger(__name__)


class CreateContactMessageUseCase(
    ICommandUseCase[CreateContactMessageRequest, ContactMessageResponse]
):
    def __init__(
        self,
        contact_message_repository: IContactMessageRepository,
        email_service: IEmailService | None = None,
    ):
        self.message_repo = contact_message_repository
        self.email_service = email_service if email_service is not None else NullEmailService()

    async def execute(
        self, request: CreateContactMessageRequest
    ) -> ContactMessageResponse:
        message = ContactMessage.create(
            name=request.name,
            email=request.email,
            message=request.message,
        )

        created_message = await self.message_repo.add(message)

        await self._send_notification(created_message)

        return ContactMessageResponse.from_entity(created_message)

    async def _send_notification(self, message: ContactMessage) -> None:
        try:
            body_text = (
                f"Nuevo mensaje de contacto\n\n"
                f"Nombre: {message.name}\n"
                f"Email: {message.email}\n"
                f"Fecha: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n"
                f"Mensaje:\n{message.message}"
            )
            body_html = (
                f"<h2>Nuevo mensaje de contacto</h2>"
                f"<p><strong>Nombre:</strong> {message.name}</p>"
                f"<p><strong>Email:</strong> {message.email}</p>"
                f"<p><strong>Fecha:</strong> {message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC</p>"
                f"<hr><p>{message.message.replace(chr(10), '<br>')}</p>"
            )
            await self.email_service.send(
                EmailMessage(
                    to=settings.NOTIFICATION_EMAIL_TO,
                    subject=f"[azfe.dev] Nuevo mensaje de {message.name}",
                    body_html=body_html,
                    body_text=body_text,
                )
            )
        except Exception as exc:
            logger.warning("Email notification failed: %s", exc)
