from typing import Any

from app.domain.entities import ContactMessage
from app.shared.interfaces.mapper import IMapper


class ContactMessageMapper(IMapper[ContactMessage, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> ContactMessage:
        return ContactMessage(
            id=str(persistence_model["_id"]),
            name=persistence_model["name"],
            email=persistence_model["email"],
            message=persistence_model["message"],
            created_at=persistence_model["created_at"],
            status=persistence_model.get("status", "pending"),
            read_at=persistence_model.get("read_at"),
            replied_at=persistence_model.get("replied_at"),
        )

    def to_persistence(self, domain_entity: ContactMessage) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "name": domain_entity.name,
            "email": domain_entity.email,
            "message": domain_entity.message,
            "created_at": domain_entity.created_at,
            "status": domain_entity.status,
        }
        if domain_entity.read_at is not None:
            doc["read_at"] = domain_entity.read_at
        if domain_entity.replied_at is not None:
            doc["replied_at"] = domain_entity.replied_at
        return doc
