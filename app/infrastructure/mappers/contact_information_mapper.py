from typing import Any

from app.domain.entities import ContactInformation
from app.shared.interfaces.mapper import IMapper


class ContactInformationMapper(IMapper[ContactInformation, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> ContactInformation:
        return ContactInformation(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            email=persistence_model["email"],
            phone=persistence_model.get("phone"),
            linkedin=persistence_model.get("linkedin"),
            github=persistence_model.get("github"),
            website=persistence_model.get("website"),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: ContactInformation) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "email": domain_entity.email,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.phone is not None:
            doc["phone"] = domain_entity.phone
        if domain_entity.linkedin is not None:
            doc["linkedin"] = domain_entity.linkedin
        if domain_entity.github is not None:
            doc["github"] = domain_entity.github
        if domain_entity.website is not None:
            doc["website"] = domain_entity.website
        return doc
