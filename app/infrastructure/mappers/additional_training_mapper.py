from typing import Any

from app.domain.entities import AdditionalTraining
from app.shared.interfaces.mapper import IMapper


class AdditionalTrainingMapper(IMapper[AdditionalTraining, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> AdditionalTraining:
        return AdditionalTraining(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            title=persistence_model["title"],
            provider=persistence_model["provider"],
            completion_date=persistence_model["completion_date"],
            order_index=persistence_model["order_index"],
            duration=persistence_model.get("duration"),
            certificate_url=persistence_model.get("certificate_url"),
            description=persistence_model.get("description"),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: AdditionalTraining) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "title": domain_entity.title,
            "provider": domain_entity.provider,
            "completion_date": domain_entity.completion_date,
            "order_index": domain_entity.order_index,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.duration is not None:
            doc["duration"] = domain_entity.duration
        if domain_entity.certificate_url is not None:
            doc["certificate_url"] = domain_entity.certificate_url
        if domain_entity.description is not None:
            doc["description"] = domain_entity.description
        return doc
