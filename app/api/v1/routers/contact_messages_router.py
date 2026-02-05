from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Request, status

from app.api.schemas.common_schema import MessageResponse
from app.api.schemas.contact_messages_schema import (
    ContactMessageCreate,
    ContactMessageResponse,
)

router = APIRouter(prefix="/contact-messages", tags=["Contact Messages"])

# Mock data - Mensajes de contacto del perfil
MOCK_MESSAGES = [
    ContactMessageResponse(
        id="msg_001",
        name="María García",
        email="maria.garcia@empresa.com",
        message="Hola Juan, me gustaría contactarte para una oportunidad laboral en nuestra empresa. ¿Podrías enviarme tu disponibilidad para una llamada?",
        sent_at=datetime(2025, 1, 18, 10, 30, 0),
        created_at=datetime(2025, 1, 18, 10, 30, 0),
        updated_at=datetime(2025, 1, 18, 10, 30, 0),
    ),
    ContactMessageResponse(
        id="msg_002",
        name="Carlos Rodríguez",
        email="carlos.r@startup.io",
        message="Vi tu portfolio y me impresionó tu experiencia con Clean Architecture. Estamos buscando un desarrollador senior para nuestro equipo. ¿Te interesaría charlar?",
        sent_at=datetime(2025, 1, 17, 15, 45, 0),
        created_at=datetime(2025, 1, 17, 15, 45, 0),
        updated_at=datetime(2025, 1, 17, 15, 45, 0),
    ),
    ContactMessageResponse(
        id="msg_003",
        name="Ana Martínez",
        email="ana.martinez@consulting.com",
        message="Hola, estamos organizando una conferencia sobre arquitecturas de software y nos gustaría invitarte como speaker. ¿Estarías interesado?",
        sent_at=datetime(2025, 1, 16, 9, 20, 0),
        created_at=datetime(2025, 1, 16, 9, 20, 0),
        updated_at=datetime(2025, 1, 16, 9, 20, 0),
    ),
    ContactMessageResponse(
        id="msg_004",
        name="Pedro Sánchez",
        email="pedro.s@freelance.dev",
        message="Me gustaría colaborar contigo en un proyecto. Tengo una idea para una aplicación y creo que tu expertise sería perfecta. ¿Hacemos una videollamada?",
        sent_at=datetime(2025, 1, 15, 14, 10, 0),
        created_at=datetime(2025, 1, 15, 14, 10, 0),
        updated_at=datetime(2025, 1, 15, 14, 10, 0),
    ),
    ContactMessageResponse(
        id="msg_005",
        name="Laura Fernández",
        email="laura.f@university.edu",
        message="Soy estudiante de ingeniería y tu portfolio me ha inspirado mucho. ¿Podrías darme algunos consejos sobre cómo mejorar mis habilidades en desarrollo backend?",
        sent_at=datetime(2025, 1, 14, 11, 0, 0),
        created_at=datetime(2025, 1, 14, 11, 0, 0),
        updated_at=datetime(2025, 1, 14, 11, 0, 0),
    ),
]


@router.get(
    "",
    response_model=list[ContactMessageResponse],
    summary="Listar mensajes de contacto (ADMIN)",
    description="Obtiene todos los mensajes de contacto recibidos",
)
async def get_contact_messages():
    """
    Lista todos los mensajes de contacto del perfil único del sistema.

    Los mensajes se retornan ordenados por sent_at descendente (más recientes primero).

    ⚠️ **ENDPOINT PRIVADO**: Requiere autenticación de administrador.

    Returns:
        List[ContactMessageResponse]: Lista de mensajes ordenados por fecha

    Relación:
    - Todos los mensajes pertenecen al Profile único del sistema

    TODO: Implementar con GetContactMessagesUseCase
    TODO: Requiere autenticación de admin (JWT)
    TODO: Ordenar por sent_at DESC (más recientes primero)
    TODO: Considerar paginación si hay muchos mensajes
    """
    return sorted(MOCK_MESSAGES, key=lambda x: x.sent_at, reverse=True)


@router.get(
    "/{message_id}",
    response_model=ContactMessageResponse,
    summary="Obtener mensaje de contacto (ADMIN)",
    description="Obtiene un mensaje de contacto específico por ID",
)
async def get_contact_message(message_id: str):
    """
    Obtiene un mensaje de contacto por su ID.

    ⚠️ **ENDPOINT PRIVADO**: Requiere autenticación de administrador.

    Args:
        message_id: ID único del mensaje

    Returns:
        ContactMessageResponse: Mensaje encontrado

    Raises:
        HTTPException 404: Si el mensaje no existe

    TODO: Implementar con GetContactMessageUseCase
    TODO: Requiere autenticación de admin
    """
    for msg in MOCK_MESSAGES:
        if msg.id == message_id:
            return msg

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Mensaje con ID '{message_id}' no encontrado",
    )


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enviar mensaje de contacto (PÚBLICO)",
    description="Crea un nuevo mensaje desde el formulario de contacto público",
)
async def create_contact_message(_message_data: ContactMessageCreate, _request: Request):
    """
    Crea un nuevo mensaje de contacto desde el formulario público del portfolio.

    ✅ **ENDPOINT PÚBLICO**: No requiere autenticación.

    Este es el endpoint que el formulario de contacto del portfolio llama cuando
    un visitante envía un mensaje.

    **Invariantes validados automáticamente:**
    - `name` no puede estar vacío (min_length=1)
    - `email` no puede estar vacío y debe ser válido (EmailStr)
    - `message` no puede estar vacío (min_length=1)
    - `sent_at` se genera automáticamente en el servidor

    Args:
        message_data: Datos del mensaje (name, email, message)
        request: Request de FastAPI para obtener IP

    Returns:
        MessageResponse: Confirmación de envío

    Raises:
        HTTPException 422: Si los datos no cumplen las invariantes
        HTTPException 429: Si se excede el rate limit (anti-spam)

    Seguridad:
    - Este endpoint debe tener rate limiting para prevenir spam
    - Considerar implementar CAPTCHA (reCAPTCHA, hCaptcha)
    - Registrar IP del remitente para análisis de spam

    TODO: Implementar con CreateContactMessageUseCase
    TODO: Añadir rate limiting (ej: máximo 3 mensajes por IP por hora)
    TODO: Considerar integración con CAPTCHA
    TODO: Enviar notificación por email al admin cuando llega mensaje
    TODO: Registrar IP del cliente para seguridad
    """
    # Capturar IP para seguridad/anti-spam

    # TODO: Validar rate limit
    # if rate_limiter.is_exceeded(client_ip):
    #     raise HTTPException(
    #         status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    #         detail="Has enviado demasiados mensajes. Por favor, espera un momento."
    #     )

    # TODO: Validar CAPTCHA si está implementado
    # if not verify_captcha(captcha_token):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Validación de CAPTCHA fallida"
    #     )

    return MessageResponse(
        success=True, message="¡Mensaje enviado correctamente! Te responderemos pronto."
    )


@router.delete(
    "/{message_id}",
    response_model=MessageResponse,
    summary="Eliminar mensaje de contacto (ADMIN)",
    description="Elimina un mensaje de contacto",
)
async def delete_contact_message(message_id: str):
    """
    Elimina un mensaje de contacto.

    ⚠️ **ENDPOINT PRIVADO**: Requiere autenticación de administrador.

    Útil para limpiar spam o mensajes irrelevantes.

    Args:
        message_id: ID del mensaje a eliminar

    Returns:
        MessageResponse: Confirmación de eliminación

    Raises:
        HTTPException 404: Si el mensaje no existe

    TODO: Implementar con DeleteContactMessageUseCase
    TODO: Requiere autenticación de admin
    TODO: Considerar soft delete en vez de hard delete (para auditoría)
    """
    return MessageResponse(
        success=True, message=f"Mensaje '{message_id}' eliminado correctamente"
    )


@router.get(
    "/stats/summary",
    response_model=dict,
    summary="Estadísticas de mensajes (ADMIN)",
    description="Obtiene estadísticas sobre los mensajes recibidos",
)
async def get_contact_messages_stats():
    """
    Calcula estadísticas sobre los mensajes de contacto.

    ⚠️ **ENDPOINT PRIVADO**: Requiere autenticación de administrador.

    Útil para dashboard del admin panel.

    Returns:
        dict: Estadísticas
        Ejemplo:
        {
            "total": 42,
            "today": 3,
            "this_week": 12,
            "this_month": 28,
            "by_day": {
                "2025-01-20": 3,
                "2025-01-19": 5
            }
        }

    TODO: Implementar con GetContactMessagesStatsUseCase
    TODO: Requiere autenticación de admin
    TODO: Calcular métricas de tiempo real
    """
    from datetime import date, timedelta

    today = date.today()

    stats: dict[str, Any] = {
        "total": len(MOCK_MESSAGES),
        "today": len([m for m in MOCK_MESSAGES if m.sent_at.date() == today]),
        "this_week": len(
            [m for m in MOCK_MESSAGES if m.sent_at.date() >= today - timedelta(days=7)]
        ),
        "this_month": len(
            [m for m in MOCK_MESSAGES if m.sent_at.date() >= today - timedelta(days=30)]
        ),
        "by_day": {},
    }

    # Contar por día (últimos 7 días)
    for i in range(7):
        day = today - timedelta(days=i)
        count = len([m for m in MOCK_MESSAGES if m.sent_at.date() == day])
        stats["by_day"][str(day)] = count

    return stats


@router.get(
    "/recent/{limit}",
    response_model=list[ContactMessageResponse],
    summary="Mensajes recientes (ADMIN)",
    description="Obtiene los N mensajes más recientes",
)
async def get_recent_contact_messages(limit: int = 10):
    """
    Obtiene los mensajes más recientes.

    ⚠️ **ENDPOINT PRIVADO**: Requiere autenticación de administrador.

    Útil para mostrar en el dashboard del admin panel.

    Args:
        limit: Número de mensajes a retornar (default: 10, max: 50)

    Returns:
        List[ContactMessageResponse]: Mensajes más recientes

    TODO: Implementar con GetRecentContactMessagesUseCase
    TODO: Requiere autenticación de admin
    TODO: Limitar máximo a 50 mensajes
    """
    if limit > 50:
        limit = 50

    sorted_messages = sorted(MOCK_MESSAGES, key=lambda x: x.sent_at, reverse=True)
    return sorted_messages[:limit]
