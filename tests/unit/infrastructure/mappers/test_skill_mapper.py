"""Unit tests for SkillMapper."""

from app.domain.entities import Skill
from app.infrastructure.mappers.skill_mapper import SkillMapper

from .conftest import DT_CREATED, DT_UPDATED


class TestSkillMapperToDomain:
    def setup_method(self):
        self.mapper = SkillMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "s-1",
            "profile_id": "p-1",
            "name": "Python",
            "category": "backend",
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "s-1"
        assert entity.profile_id == "p-1"
        assert entity.name == "Python"
        assert entity.category == "backend"
        assert entity.order_index == 0
        assert entity.level is None

    def test_with_optional_level(self):
        doc = {
            "_id": "s-1",
            "profile_id": "p-1",
            "name": "Python",
            "category": "backend",
            "order_index": 0,
            "level": "expert",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.level == "expert"


class TestSkillMapperToPersistence:
    def setup_method(self):
        self.mapper = SkillMapper()

    def test_required_fields_only(self):
        entity = Skill(
            id="s-1",
            profile_id="p-1",
            name="Python",
            category="backend",
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["_id"] == "s-1"
        assert doc["name"] == "Python"
        assert "level" not in doc

    def test_optional_level_included(self):
        entity = Skill(
            id="s-1",
            profile_id="p-1",
            name="Python",
            category="backend",
            order_index=0,
            level="expert",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert doc["level"] == "expert"

    def test_round_trip(self):
        doc = {
            "_id": "s-1",
            "profile_id": "p-1",
            "name": "Python",
            "category": "backend",
            "order_index": 0,
            "level": "expert",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
