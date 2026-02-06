from typing import Any

from app.domain.entities import Project
from app.shared.interfaces.mapper import IMapper


class ProjectMapper(IMapper[Project, dict[str, Any]]):

    def to_domain(self, persistence_model: dict[str, Any]) -> Project:
        return Project(
            id=str(persistence_model["_id"]),
            profile_id=persistence_model["profile_id"],
            title=persistence_model["title"],
            description=persistence_model["description"],
            start_date=persistence_model["start_date"],
            order_index=persistence_model["order_index"],
            end_date=persistence_model.get("end_date"),
            live_url=persistence_model.get("live_url"),
            repo_url=persistence_model.get("repo_url"),
            technologies=persistence_model.get("technologies", []),
            created_at=persistence_model["created_at"],
            updated_at=persistence_model["updated_at"],
        )

    def to_persistence(self, domain_entity: Project) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "_id": domain_entity.id,
            "profile_id": domain_entity.profile_id,
            "title": domain_entity.title,
            "description": domain_entity.description,
            "start_date": domain_entity.start_date,
            "order_index": domain_entity.order_index,
            "technologies": domain_entity.technologies,
            "created_at": domain_entity.created_at,
            "updated_at": domain_entity.updated_at,
        }
        if domain_entity.end_date is not None:
            doc["end_date"] = domain_entity.end_date
        if domain_entity.live_url is not None:
            doc["live_url"] = domain_entity.live_url
        if domain_entity.repo_url is not None:
            doc["repo_url"] = domain_entity.repo_url
        return doc
