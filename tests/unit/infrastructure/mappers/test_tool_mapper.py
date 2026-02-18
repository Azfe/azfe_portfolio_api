"""Unit tests for ToolMapper."""

from app.domain.entities import Tool
from app.infrastructure.mappers.tool_mapper import ToolMapper

from .conftest import DT_CREATED, DT_UPDATED


class TestToolMapperToDomain:
    def setup_method(self):
        self.mapper = ToolMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "tool-1",
            "profile_id": "p-1",
            "name": "Docker",
            "category": "devops",
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "tool-1"
        assert entity.name == "Docker"
        assert entity.category == "devops"
        assert entity.icon_url is None

    def test_with_icon_url(self):
        doc = {
            "_id": "tool-1",
            "profile_id": "p-1",
            "name": "Docker",
            "category": "devops",
            "order_index": 0,
            "icon_url": "https://img.com/docker.png",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.icon_url == "https://img.com/docker.png"


class TestToolMapperToPersistence:
    def setup_method(self):
        self.mapper = ToolMapper()

    def test_excludes_none_icon_url(self):
        entity = Tool(
            id="tool-1",
            profile_id="p-1",
            name="Docker",
            category="devops",
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert "icon_url" not in doc

    def test_includes_icon_url_when_set(self):
        entity = Tool(
            id="tool-1",
            profile_id="p-1",
            name="Docker",
            category="devops",
            order_index=0,
            icon_url="https://img.com/docker.png",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert doc["icon_url"] == "https://img.com/docker.png"

    def test_round_trip(self):
        doc = {
            "_id": "tool-1",
            "profile_id": "p-1",
            "name": "Docker",
            "category": "devops",
            "order_index": 0,
            "icon_url": "https://img.com/docker.png",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
