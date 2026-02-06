from typing import Any

from app.domain.entities import WorkExperience
from app.shared.interfaces.mapper import IMapper


class WorkExperienceMapper(IMapper[WorkExperience, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> WorkExperience:
        return WorkExperience(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            role=persistence_model["role"],
            company=persistence_model["company"],
            start_date=persistence_model["start_date"],
            order_index=persistence_model["order_index"],
            description=persistence_model.get("description"),
            end_date=persistence_model.get("end_date"),
            responsibilities=persistence_model.get("responsibilities", []),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: WorkExperience) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "role": domain_entity.role,
            "company": domain_entity.company,
            "start_date": domain_entity.start_date,
            "order_index": domain_entity.order_index,
            "responsibilities": domain_entity.responsibilities,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.description is not None:
            doc["description"] = domain_entity.description
        if domain_entity.end_date is not None:
            doc["end_date"] = domain_entity.end_date
        return doc
