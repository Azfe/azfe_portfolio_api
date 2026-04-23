from datetime import date, timedelta

from fastapi import APIRouter, Depends, status

from app.api.dependencies import (
    get_contact_message_repository,
    get_create_contact_message_use_case,
    get_delete_contact_message_use_case,
    get_list_contact_messages_use_case,
)
from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.contact_messages_schema import (
    ContactMessageCreate,
    ContactMessageResponse,
)
from app.application.dto import (
    ContactMessageResponse as ContactMessageDTO,
    CreateContactMessageRequest,
    DeleteContactMessageRequest,
    ListContactMessagesRequest,
)
from app.application.use_cases.contact_message import (
    CreateContactMessageUseCase,
    DeleteContactMessageUseCase,
    ListContactMessagesUseCase,
)
from app.infrastructure.repositories import ContactMessageRepository
from app.shared.shared_exceptions import NotFoundException

router = APIRouter(prefix="/contact-messages", tags=["Contact Messages"])


@router.get(
    "/stats/summary",
    response_model=dict,
    summary="Estadísticas de mensajes (ADMIN)",
    description="Obtiene estadísticas sobre los mensajes recibidos",
)
async def get_contact_messages_stats(
    use_case: ListContactMessagesUseCase = Depends(get_list_contact_messages_use_case),
):
    result = await use_case.execute(ListContactMessagesRequest(ascending=False))
    messages = result.messages

    today = date.today()
    dated_messages = [m for m in messages if m.created_at is not None]

    stats: dict = {
        "total": result.total,
        "today": len(
            [
                m
                for m in dated_messages
                if m.created_at is not None and m.created_at.date() == today
            ]
        ),
        "this_week": len(
            [
                m
                for m in dated_messages
                if m.created_at is not None
                and m.created_at.date() >= today - timedelta(days=7)
            ]
        ),
        "this_month": len(
            [
                m
                for m in dated_messages
                if m.created_at is not None
                and m.created_at.date() >= today - timedelta(days=30)
            ]
        ),
        "by_day": {},
    }

    for i in range(7):
        day = today - timedelta(days=i)
        count = len(
            [
                m
                for m in dated_messages
                if m.created_at is not None and m.created_at.date() == day
            ]
        )
        stats["by_day"][str(day)] = count

    return stats


@router.get(
    "/recent/{limit}",
    response_model=list[ContactMessageResponse],
    summary="Mensajes recientes (ADMIN)",
    description="Obtiene los N mensajes más recientes",
)
async def get_recent_contact_messages(
    limit: int = 10,
    use_case: ListContactMessagesUseCase = Depends(get_list_contact_messages_use_case),
):
    if limit > 50:
        limit = 50

    result = await use_case.execute(ListContactMessagesRequest(ascending=False))
    return result.messages[:limit]


@router.get(
    "",
    response_model=list[ContactMessageResponse],
    summary="Listar mensajes de contacto (ADMIN)",
    description="Obtiene todos los mensajes de contacto recibidos",
)
async def get_contact_messages(
    use_case: ListContactMessagesUseCase = Depends(get_list_contact_messages_use_case),
):
    result = await use_case.execute(ListContactMessagesRequest(ascending=False))
    return result.messages


@router.get(
    "/{message_id}",
    response_model=ContactMessageResponse,
    summary="Obtener mensaje de contacto (ADMIN)",
    description="Obtiene un mensaje de contacto específico por ID",
)
async def get_contact_message(
    message_id: str,
    repo: ContactMessageRepository = Depends(get_contact_message_repository),
):
    entity = await repo.get_by_id(message_id)
    if not entity:
        raise NotFoundException("ContactMessage", message_id)
    return ContactMessageDTO.from_entity(entity)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enviar mensaje de contacto (PÚBLICO)",
    description="Crea un nuevo mensaje desde el formulario de contacto público",
)
async def create_contact_message(
    message_data: ContactMessageCreate,
    use_case: CreateContactMessageUseCase = Depends(
        get_create_contact_message_use_case
    ),
):
    await use_case.execute(
        CreateContactMessageRequest(
            name=message_data.name,
            email=message_data.email,
            message=message_data.message,
        )
    )
    return MessageResponse(
        success=True,
        message="¡Mensaje enviado correctamente! Te responderemos pronto.",
    )


@router.delete(
    "/{message_id}",
    response_model=MessageResponse,
    summary="Eliminar mensaje de contacto (ADMIN)",
    description="Elimina un mensaje de contacto",
)
async def delete_contact_message(
    message_id: str,
    use_case: DeleteContactMessageUseCase = Depends(
        get_delete_contact_message_use_case
    ),
):
    await use_case.execute(DeleteContactMessageRequest(message_id=message_id))
    return MessageResponse(
        success=True, message=f"Mensaje '{message_id}' eliminado correctamente"
    )
