"""Tests for WorkExperience DTOs."""

from app.application.dto.work_experience_dto import (
    WorkExperienceListResponse,
    WorkExperienceResponse,
)

from .conftest import DT, DT2, DT_END, DT_START, make_entity


def _make_experience_entity(**overrides):
    defaults = {
        "id": "w-1",
        "profile_id": "p-1",
        "role": "Developer",
        "company": "Acme",
        "start_date": DT_START,
        "end_date": DT_END,
        "description": "Full-stack dev",
        "responsibilities": ["Code", "Review"],
        "order_index": 0,
    }
    defaults.update(overrides)
    entity = make_entity(**defaults)
    entity.is_current_position.return_value = overrides.get("_is_current", False)
    return entity


class TestWorkExperienceResponseFromEntity:
    def test_maps_all_fields(self):
        entity = _make_experience_entity()
        resp = WorkExperienceResponse.from_entity(entity)

        assert resp.id == "w-1"
        assert resp.role == "Developer"
        assert resp.company == "Acme"
        assert resp.start_date == DT_START
        assert resp.end_date == DT_END
        assert resp.description == "Full-stack dev"
        assert resp.order_index == 0
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    def test_responsibilities_are_copied(self):
        original = ["Code", "Review"]
        entity = _make_experience_entity(responsibilities=original)
        resp = WorkExperienceResponse.from_entity(entity)

        assert resp.responsibilities == ["Code", "Review"]
        assert resp.responsibilities is not original

    def test_is_current_from_entity_method(self):
        entity = _make_experience_entity(_is_current=True)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.is_current is True

    def test_is_not_current(self):
        entity = _make_experience_entity(_is_current=False)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.is_current is False

    def test_none_optional_fields(self):
        entity = _make_experience_entity(end_date=None, description=None)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.end_date is None
        assert resp.description is None

    def test_empty_responsibilities(self):
        entity = _make_experience_entity(responsibilities=[])
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.responsibilities == []


class TestWorkExperienceListResponseFromEntities:
    def test_maps_list(self):
        entities = [
            _make_experience_entity(id="w-1"),
            _make_experience_entity(id="w-2", role="Lead"),
        ]
        resp = WorkExperienceListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.experiences) == 2

    def test_empty_list(self):
        resp = WorkExperienceListResponse.from_entities([])
        assert resp.total == 0
        assert resp.experiences == []
