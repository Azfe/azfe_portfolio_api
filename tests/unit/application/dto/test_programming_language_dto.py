"""Tests for ProgrammingLanguage DTOs."""

from app.application.dto.programming_language_dto import (
    ProgrammingLanguageListResponse,
    ProgrammingLanguageResponse,
)

from .conftest import DT, DT2, make_entity


def _make_pl_entity(**overrides):
    defaults = {
        "id": "pl-1",
        "profile_id": "p-1",
        "name": "Python",
        "order_index": 0,
        "level": "advanced",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestProgrammingLanguageResponseFromEntity:
    def test_maps_all_fields(self):
        entity = _make_pl_entity()
        resp = ProgrammingLanguageResponse.from_entity(entity)

        assert resp.id == "pl-1"
        assert resp.profile_id == "p-1"
        assert resp.name == "Python"
        assert resp.order_index == 0
        assert resp.level == "advanced"

    def test_datetime_to_isoformat(self):
        entity = _make_pl_entity()
        resp = ProgrammingLanguageResponse.from_entity(entity)

        assert resp.created_at == DT.isoformat()
        assert resp.updated_at == DT2.isoformat()

    def test_none_level(self):
        entity = _make_pl_entity(level=None)
        resp = ProgrammingLanguageResponse.from_entity(entity)
        assert resp.level is None


class TestProgrammingLanguageListResponseFromEntities:
    def test_maps_list(self):
        entities = [
            _make_pl_entity(id="pl-1", name="Python"),
            _make_pl_entity(id="pl-2", name="Rust"),
        ]
        resp = ProgrammingLanguageListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.programming_languages) == 2

    def test_empty_list(self):
        resp = ProgrammingLanguageListResponse.from_entities([])
        assert resp.total == 0
        assert resp.programming_languages == []
