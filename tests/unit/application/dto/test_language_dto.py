"""Tests for Language DTOs."""

from app.application.dto.language_dto import LanguageListResponse, LanguageResponse

from .conftest import DT, DT2, make_entity


def _make_language_entity(**overrides):
    defaults = {
        "id": "lang-1",
        "profile_id": "p-1",
        "name": "English",
        "order_index": 0,
        "proficiency": "c2",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestLanguageResponseFromEntity:
    def test_maps_all_fields(self):
        entity = _make_language_entity()
        resp = LanguageResponse.from_entity(entity)

        assert resp.id == "lang-1"
        assert resp.profile_id == "p-1"
        assert resp.name == "English"
        assert resp.order_index == 0
        assert resp.proficiency == "c2"

    def test_datetime_to_isoformat(self):
        entity = _make_language_entity()
        resp = LanguageResponse.from_entity(entity)

        assert resp.created_at == DT.isoformat()
        assert resp.updated_at == DT2.isoformat()

    def test_none_proficiency(self):
        entity = _make_language_entity(proficiency=None)
        resp = LanguageResponse.from_entity(entity)
        assert resp.proficiency is None


class TestLanguageListResponseFromEntities:
    def test_maps_list(self):
        entities = [
            _make_language_entity(id="l-1", name="English"),
            _make_language_entity(id="l-2", name="Spanish"),
        ]
        resp = LanguageListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.languages) == 2

    def test_empty_list(self):
        resp = LanguageListResponse.from_entities([])
        assert resp.total == 0
        assert resp.languages == []
