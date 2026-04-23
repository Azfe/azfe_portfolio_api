"""Unit tests for AdditionalTrainingMapper."""

from app.domain.entities import AdditionalTraining
from app.infrastructure.mappers.additional_training_mapper import (
    AdditionalTrainingMapper,
)

from .conftest import DT_COMPLETION, DT_CREATED, DT_UPDATED


class TestAdditionalTrainingMapperToDomain:
    def setup_method(self):
        self.mapper = AdditionalTrainingMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "t-1",
            "profile_id": "p-1",
            "title": "Clean Arch",
            "provider": "Udemy",
            "completion_date": DT_COMPLETION,
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "t-1"
        assert entity.title == "Clean Arch"
        assert entity.provider == "Udemy"
        assert entity.duration is None
        assert entity.certificate_url is None
        assert entity.description is None

    def test_all_fields(self):
        doc = {
            "_id": "t-1",
            "profile_id": "p-1",
            "title": "Clean Arch",
            "provider": "Udemy",
            "completion_date": DT_COMPLETION,
            "order_index": 0,
            "duration": "40h",
            "certificate_url": "https://udemy.com/cert/123",
            "description": "Architecture course",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.duration == "40h"
        assert entity.certificate_url == "https://udemy.com/cert/123"
        assert entity.description == "Architecture course"


class TestAdditionalTrainingMapperToPersistence:
    def setup_method(self):
        self.mapper = AdditionalTrainingMapper()

    def test_excludes_none_optionals(self):
        entity = AdditionalTraining(
            id="t-1",
            profile_id="p-1",
            title="Clean Arch",
            provider="Udemy",
            completion_date=DT_COMPLETION,
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert "duration" not in doc
        assert "certificate_url" not in doc
        assert "description" not in doc

    def test_includes_optionals_when_set(self):
        entity = AdditionalTraining(
            id="t-1",
            profile_id="p-1",
            title="Clean Arch",
            provider="Udemy",
            completion_date=DT_COMPLETION,
            order_index=0,
            duration="40h",
            certificate_url="https://udemy.com/cert/123",
            description="Architecture course",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["duration"] == "40h"
        assert doc["certificate_url"] == "https://udemy.com/cert/123"
        assert doc["description"] == "Architecture course"

    def test_round_trip(self):
        doc = {
            "_id": "t-1",
            "profile_id": "p-1",
            "title": "Clean Arch",
            "provider": "Udemy",
            "completion_date": DT_COMPLETION,
            "order_index": 0,
            "duration": "40h",
            "certificate_url": "https://udemy.com/cert/123",
            "description": "Architecture course",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
