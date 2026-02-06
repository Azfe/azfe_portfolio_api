from typing import Any

from app.domain.entities import Education
from app.shared.interfaces.mapper import IMapper


class EducationMapper(IMapper[Education, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> Education:
        return Education(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            institution=persistence_model["institution"],
            degree=persistence_model["degree"],
            field=persistence_model["field"],
            start_date=persistence_model["start_date"],
            order_index=persistence_model["order_index"],
            description=persistence_model.get("description"),
            end_date=persistence_model.get("end_date"),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: Education) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "institution": domain_entity.institution,
            "degree": domain_entity.degree,
            "field": domain_entity.field,
            "start_date": domain_entity.start_date,
            "order_index": domain_entity.order_index,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.description is not None:
            doc["description"] = domain_entity.description
        if domain_entity.end_date is not None:
            doc["end_date"] = domain_entity.end_date
        return doc
