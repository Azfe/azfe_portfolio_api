from typing import Any

from app.domain.entities import Language
from app.shared.interfaces.mapper import IMapper


class LanguageMapper(IMapper[Language, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> Language:
        return Language(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            name=persistence_model["name"],
            order_index=persistence_model["order_index"],
            proficiency=persistence_model.get("proficiency"),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: Language) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "name": domain_entity.name,
            "order_index": domain_entity.order_index,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.proficiency is not None:
            doc["proficiency"] = domain_entity.proficiency
        return doc
