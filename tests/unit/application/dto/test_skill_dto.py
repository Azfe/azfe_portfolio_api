"""Tests for Skill DTOs."""

from app.application.dto.skill_dto import SkillListResponse, SkillResponse

from .conftest import DT, DT2, make_entity


def _make_skill_entity(**overrides):
    defaults = {
        "id": "s-1",
        "profile_id": "p-1",
        "name": "Python",
        "category": "backend",
        "order_index": 0,
        "level": "expert",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestSkillResponseFromEntity:
    def test_maps_all_fields(self):
        entity = _make_skill_entity()
        resp = SkillResponse.from_entity(entity)

        assert resp.id == "s-1"
        assert resp.profile_id == "p-1"
        assert resp.name == "Python"
        assert resp.category == "backend"
        assert resp.order_index == 0
        assert resp.level == "expert"

    def test_datetime_to_isoformat(self):
        entity = _make_skill_entity()
        resp = SkillResponse.from_entity(entity)

        assert resp.created_at == DT.isoformat()
        assert resp.updated_at == DT2.isoformat()

    def test_none_level(self):
        entity = _make_skill_entity(level=None)
        resp = SkillResponse.from_entity(entity)

        assert resp.level is None


class TestSkillListResponseFromEntities:
    def test_maps_list(self):
        entities = [
            _make_skill_entity(id="s-1", name="Python"),
            _make_skill_entity(id="s-2", name="FastAPI"),
        ]
        resp = SkillListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.skills) == 2
        assert resp.skills[0].name == "Python"
        assert resp.skills[1].name == "FastAPI"

    def test_empty_list(self):
        resp = SkillListResponse.from_entities([])

        assert resp.total == 0
        assert resp.skills == []
