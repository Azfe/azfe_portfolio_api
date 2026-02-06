from typing import Any

from app.domain.entities import Skill
from app.shared.interfaces.mapper import IMapper


class SkillMapper(IMapper[Skill, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> Skill:
        return Skill(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            name=persistence_model["name"],
            category=persistence_model["category"],
            order_index=persistence_model["order_index"],
            level=persistence_model.get("level"),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: Skill) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "name": domain_entity.name,
            "category": domain_entity.category,
            "order_index": domain_entity.order_index,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.level is not None:
            doc["level"] = domain_entity.level
        return doc
