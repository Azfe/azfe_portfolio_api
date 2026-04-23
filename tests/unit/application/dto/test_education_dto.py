"""Tests for Education DTOs."""

from app.application.dto.education_dto import EducationListResponse, EducationResponse

from .conftest import DT, DT2, DT_END, DT_START, make_entity


def _make_education_entity(**overrides):
    defaults = {
        "id": "e-1",
        "profile_id": "p-1",
        "institution": "MIT",
        "degree": "BSc",
        "field": "CS",
        "start_date": DT_START,
        "end_date": DT_END,
        "description": "Great program",
        "order_index": 0,
    }
    defaults.update(overrides)
    entity = make_entity(**defaults)
    entity.is_ongoing.return_value = overrides.get("_is_ongoing", False)
    return entity


class TestEducationResponseFromEntity:
    def test_maps_all_fields(self):
        entity = _make_education_entity()
        resp = EducationResponse.from_entity(entity)

        assert resp.id == "e-1"
        assert resp.institution == "MIT"
        assert resp.degree == "BSc"
        assert resp.field == "CS"
        assert resp.start_date == DT_START
        assert resp.end_date == DT_END
        assert resp.description == "Great program"
        assert resp.order_index == 0
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    def test_is_ongoing_from_entity_method(self):
        entity = _make_education_entity(_is_ongoing=True)
        resp = EducationResponse.from_entity(entity)
        assert resp.is_ongoing is True

    def test_is_not_ongoing(self):
        entity = _make_education_entity(_is_ongoing=False)
        resp = EducationResponse.from_entity(entity)
        assert resp.is_ongoing is False

    def test_none_optional_fields(self):
        entity = _make_education_entity(end_date=None, description=None)
        resp = EducationResponse.from_entity(entity)
        assert resp.end_date is None
        assert resp.description is None


class TestEducationListResponseFromEntities:
    def test_maps_list(self):
        entities = [
            _make_education_entity(id="e-1"),
            _make_education_entity(id="e-2", institution="Stanford"),
        ]
        resp = EducationListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.education) == 2

    def test_empty_list(self):
        resp = EducationListResponse.from_entities([])
        assert resp.total == 0
        assert resp.education == []
