"""Unit tests for WorkExperienceMapper."""

from app.domain.entities import WorkExperience
from app.infrastructure.mappers.experience_mapper import WorkExperienceMapper

from .conftest import DT_CREATED, DT_END, DT_START, DT_UPDATED


class TestWorkExperienceMapperToDomain:
    def setup_method(self):
        self.mapper = WorkExperienceMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "w-1",
            "profile_id": "p-1",
            "role": "Dev",
            "company": "Acme",
            "start_date": DT_START,
            "order_index": 0,
            "responsibilities": ["Code"],
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "w-1"
        assert entity.role == "Dev"
        assert entity.company == "Acme"
        assert entity.responsibilities == ["Code"]
        assert entity.description is None
        assert entity.end_date is None

    def test_all_fields(self):
        doc = {
            "_id": "w-1",
            "profile_id": "p-1",
            "role": "Dev",
            "company": "Acme",
            "start_date": DT_START,
            "order_index": 0,
            "description": "Full-stack dev",
            "end_date": DT_END,
            "responsibilities": ["Code", "Review"],
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.description == "Full-stack dev"
        assert entity.end_date == DT_END

    def test_missing_responsibilities_defaults_to_empty(self):
        doc = {
            "_id": "w-1",
            "profile_id": "p-1",
            "role": "Dev",
            "company": "Acme",
            "start_date": DT_START,
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.responsibilities == []


class TestWorkExperienceMapperToPersistence:
    def setup_method(self):
        self.mapper = WorkExperienceMapper()

    def test_excludes_none_optionals(self):
        entity = WorkExperience(
            id="w-1",
            profile_id="p-1",
            role="Dev",
            company="Acme",
            start_date=DT_START,
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert "description" not in doc
        assert "end_date" not in doc
        assert doc["responsibilities"] == []

    def test_includes_optionals_when_set(self):
        entity = WorkExperience(
            id="w-1",
            profile_id="p-1",
            role="Dev",
            company="Acme",
            start_date=DT_START,
            order_index=0,
            description="Full-stack",
            end_date=DT_END,
            responsibilities=["Code"],
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["description"] == "Full-stack"
        assert doc["end_date"] == DT_END

    def test_round_trip(self):
        doc = {
            "_id": "w-1",
            "profile_id": "p-1",
            "role": "Dev",
            "company": "Acme",
            "start_date": DT_START,
            "order_index": 0,
            "description": "Full-stack",
            "end_date": DT_END,
            "responsibilities": ["Code"],
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
