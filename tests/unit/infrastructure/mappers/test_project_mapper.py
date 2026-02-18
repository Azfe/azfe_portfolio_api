"""Unit tests for ProjectMapper."""

from app.domain.entities import Project
from app.infrastructure.mappers.project_mapper import ProjectMapper

from .conftest import DT_CREATED, DT_END, DT_START, DT_UPDATED


class TestProjectMapperToDomain:
    def setup_method(self):
        self.mapper = ProjectMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "proj-1",
            "profile_id": "p-1",
            "title": "My Project",
            "description": "A comprehensive test project description that needs to be at least one hundred characters long for validation to pass correctly.",
            "start_date": DT_START,
            "order_index": 0,
            "technologies": ["Python"],
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "proj-1"
        assert entity.title == "My Project"
        assert entity.technologies == ["Python"]
        assert entity.end_date is None
        assert entity.live_url is None
        assert entity.repo_url is None

    def test_all_fields(self):
        doc = {
            "_id": "proj-1",
            "profile_id": "p-1",
            "title": "My Project",
            "description": "A comprehensive test project description that needs to be at least one hundred characters long for validation to pass correctly.",
            "start_date": DT_START,
            "order_index": 0,
            "end_date": DT_END,
            "live_url": "https://example.com",
            "repo_url": "https://github.com/user/repo",
            "technologies": ["Python", "FastAPI"],
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.end_date == DT_END
        assert entity.live_url == "https://example.com"
        assert entity.repo_url == "https://github.com/user/repo"

    def test_missing_technologies_defaults_to_empty(self):
        doc = {
            "_id": "proj-1",
            "profile_id": "p-1",
            "title": "My Project",
            "description": "A comprehensive test project description that needs to be at least one hundred characters long for validation to pass correctly.",
            "start_date": DT_START,
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.technologies == []


class TestProjectMapperToPersistence:
    def setup_method(self):
        self.mapper = ProjectMapper()

    def test_excludes_none_optionals(self):
        entity = Project(
            id="proj-1",
            profile_id="p-1",
            title="My Project",
            description="A comprehensive test project description that needs to be at least one hundred characters long for validation to pass correctly.",
            start_date=DT_START,
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert "end_date" not in doc
        assert "live_url" not in doc
        assert "repo_url" not in doc
        assert doc["technologies"] == []

    def test_includes_optionals_when_set(self):
        entity = Project(
            id="proj-1",
            profile_id="p-1",
            title="My Project",
            description="A comprehensive test project description that needs to be at least one hundred characters long for validation to pass correctly.",
            start_date=DT_START,
            order_index=0,
            end_date=DT_END,
            live_url="https://example.com",
            repo_url="https://github.com/user/repo",
            technologies=["Python"],
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["end_date"] == DT_END
        assert doc["live_url"] == "https://example.com"
        assert doc["repo_url"] == "https://github.com/user/repo"

    def test_round_trip(self):
        doc = {
            "_id": "proj-1",
            "profile_id": "p-1",
            "title": "My Project",
            "description": "A comprehensive test project description that needs to be at least one hundred characters long for validation to pass correctly.",
            "start_date": DT_START,
            "order_index": 0,
            "end_date": DT_END,
            "live_url": "https://example.com",
            "repo_url": "https://github.com/user/repo",
            "technologies": ["Python"],
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
