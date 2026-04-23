"""Unit tests for ProgrammingLanguageMapper."""

from app.domain.entities import ProgrammingLanguage
from app.infrastructure.mappers.programming_language_mapper import (
    ProgrammingLanguageMapper,
)

from .conftest import DT_CREATED, DT_UPDATED


class TestProgrammingLanguageMapperToDomain:
    def setup_method(self):
        self.mapper = ProgrammingLanguageMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "pl-1",
            "profile_id": "p-1",
            "name": "Python",
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "pl-1"
        assert entity.name == "Python"
        assert entity.level is None

    def test_with_level(self):
        doc = {
            "_id": "pl-1",
            "profile_id": "p-1",
            "name": "Python",
            "order_index": 0,
            "level": "advanced",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.level == "advanced"


class TestProgrammingLanguageMapperToPersistence:
    def setup_method(self):
        self.mapper = ProgrammingLanguageMapper()

    def test_excludes_none_level(self):
        entity = ProgrammingLanguage(
            id="pl-1",
            profile_id="p-1",
            name="Python",
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert "level" not in doc

    def test_includes_level_when_set(self):
        entity = ProgrammingLanguage(
            id="pl-1",
            profile_id="p-1",
            name="Python",
            order_index=0,
            level="advanced",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert doc["level"] == "advanced"

    def test_round_trip(self):
        doc = {
            "_id": "pl-1",
            "profile_id": "p-1",
            "name": "Python",
            "order_index": 0,
            "level": "advanced",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
