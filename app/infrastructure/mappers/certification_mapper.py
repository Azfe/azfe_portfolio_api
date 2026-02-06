from typing import Any

from app.domain.entities import Certification
from app.shared.interfaces.mapper import IMapper


class CertificationMapper(IMapper[Certification, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> Certification:
        return Certification(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            title=persistence_model["title"],
            issuer=persistence_model["issuer"],
            issue_date=persistence_model["issue_date"],
            order_index=persistence_model["order_index"],
            expiry_date=persistence_model.get("expiry_date"),
            credential_id=persistence_model.get("credential_id"),
            credential_url=persistence_model.get("credential_url"),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: Certification) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "title": domain_entity.title,
            "issuer": domain_entity.issuer,
            "issue_date": domain_entity.issue_date,
            "order_index": domain_entity.order_index,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.expiry_date is not None:
            doc["expiry_date"] = domain_entity.expiry_date
        if domain_entity.credential_id is not None:
            doc["credential_id"] = domain_entity.credential_id
        if domain_entity.credential_url is not None:
            doc["credential_url"] = domain_entity.credential_url
        return doc
