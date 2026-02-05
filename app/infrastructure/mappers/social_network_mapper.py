from typing import Any

from app.domain.entities import SocialNetwork
from app.shared.interfaces.mapper import IMapper


class SocialNetworkMapper(IMapper[SocialNetwork, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> SocialNetwork:
        return SocialNetwork(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            platform=persistence_model["platform"],
            url=persistence_model["url"],
            order_index=persistence_model["order_index"],
            username=persistence_model.get("username"),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: SocialNetwork) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "platform": domain_entity.platform,
            "url": domain_entity.url,
            "order_index": domain_entity.order_index,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.username is not None:
            doc["username"] = domain_entity.username
        return doc
