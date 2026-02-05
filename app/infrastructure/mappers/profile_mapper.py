from typing import Any

from app.domain.entities import Profile
from app.shared.interfaces.mapper import IMapper


class ProfileMapper(IMapper[Profile, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> Profile:
        return Profile(
            id=str(persistence_model["_id"]),
            name=persistence_model["name"],
            headline=persistence_model["headline"],
            bio=persistence_model.get("bio"),
            location=persistence_model.get("location"),
            avatar_url=persistence_model.get("avatar_url"),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: Profile) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "name": domain_entity.name,
            "headline": domain_entity.headline,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.bio is not None:
            doc["bio"] = domain_entity.bio
        if domain_entity.location is not None:
            doc["location"] = domain_entity.location
        if domain_entity.avatar_url is not None:
            doc["avatar_url"] = domain_entity.avatar_url
        return doc
