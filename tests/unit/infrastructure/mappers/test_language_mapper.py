"""Unit tests for LanguageMapper."""

from app.domain.entities import Language
from app.infrastructure.mappers.language_mapper import LanguageMapper

from .conftest import DT_CREATED, DT_UPDATED


class TestLanguageMapperToDomain:
    def setup_method(self):
        self.mapper = LanguageMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "lang-1",
            "profile_id": "p-1",
            "name": "English",
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "lang-1"
        assert entity.name == "English"
        assert entity.proficiency is None

    def test_with_proficiency(self):
        doc = {
            "_id": "lang-1",
            "profile_id": "p-1",
            "name": "English",
            "order_index": 0,
            "proficiency": "c2",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.proficiency == "c2"


class TestLanguageMapperToPersistence:
    def setup_method(self):
        self.mapper = LanguageMapper()

    def test_excludes_none_proficiency(self):
        entity = Language(
            id="lang-1",
            profile_id="p-1",
            name="English",
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert "proficiency" not in doc

    def test_includes_proficiency_when_set(self):
        entity = Language(
            id="lang-1",
            profile_id="p-1",
            name="English",
            order_index=0,
            proficiency="c2",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert doc["proficiency"] == "c2"

    def test_round_trip(self):
        doc = {
            "_id": "lang-1",
            "profile_id": "p-1",
            "name": "English",
            "order_index": 0,
            "proficiency": "c2",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
