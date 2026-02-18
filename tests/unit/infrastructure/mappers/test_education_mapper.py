"""Unit tests for EducationMapper."""

from app.domain.entities import Education
from app.infrastructure.mappers.education_mapper import EducationMapper

from .conftest import DT_CREATED, DT_END, DT_START, DT_UPDATED


class TestEducationMapperToDomain:
    def setup_method(self):
        self.mapper = EducationMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "e-1",
            "profile_id": "p-1",
            "institution": "MIT",
            "degree": "BSc",
            "field": "CS",
            "start_date": DT_START,
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "e-1"
        assert entity.institution == "MIT"
        assert entity.degree == "BSc"
        assert entity.field == "CS"
        assert entity.description is None
        assert entity.end_date is None

    def test_all_fields(self):
        doc = {
            "_id": "e-1",
            "profile_id": "p-1",
            "institution": "MIT",
            "degree": "BSc",
            "field": "CS",
            "start_date": DT_START,
            "order_index": 0,
            "description": "Great program",
            "end_date": DT_END,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.description == "Great program"
        assert entity.end_date == DT_END


class TestEducationMapperToPersistence:
    def setup_method(self):
        self.mapper = EducationMapper()

    def test_excludes_none_optionals(self):
        entity = Education(
            id="e-1",
            profile_id="p-1",
            institution="MIT",
            degree="BSc",
            field="CS",
            start_date=DT_START,
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert "description" not in doc
        assert "end_date" not in doc

    def test_includes_optionals_when_set(self):
        entity = Education(
            id="e-1",
            profile_id="p-1",
            institution="MIT",
            degree="BSc",
            field="CS",
            start_date=DT_START,
            order_index=0,
            description="Great program",
            end_date=DT_END,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["description"] == "Great program"
        assert doc["end_date"] == DT_END

    def test_round_trip(self):
        doc = {
            "_id": "e-1",
            "profile_id": "p-1",
            "institution": "MIT",
            "degree": "BSc",
            "field": "CS",
            "start_date": DT_START,
            "order_index": 0,
            "description": "Great program",
            "end_date": DT_END,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
