"""Tests for Skill DTOs."""

import pytest

from app.application.dto.skill_dto import (
    EditSkillRequest,
    SkillListResponse,
    SkillResponse,
)

from .conftest import DT, DT2, make_entity


def _make_skill_entity(**overrides):
    defaults = {
        "id": "s-1",
        "profile_id": "p-1",
        "name": "Python",
        "order_index": 0,
        "level": "expert",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestEditSkillRequest:
    @pytest.mark.unit
    def test_order_index_defaults_to_none(self):
        """order_index is optional — must default to None."""
        req = EditSkillRequest(skill_id="s-1")
        assert req.order_index is None

    @pytest.mark.unit
    def test_accepts_order_index_when_provided(self):
        """order_index is accepted when explicitly supplied."""
        req = EditSkillRequest(skill_id="s-1", order_index=7)
        assert req.order_index == 7

    @pytest.mark.unit
    def test_all_fields_optional_except_skill_id(self):
        """Only skill_id is required; name and level also default to None."""
        req = EditSkillRequest(skill_id="s-99")
        assert req.name is None
        assert req.level is None
        assert req.order_index is None

    @pytest.mark.unit
    def test_full_construction(self):
        """All fields provided together are stored correctly."""
        req = EditSkillRequest(
            skill_id="s-1",
            name="Go",
            level="advanced",
            order_index=3,
        )
        assert req.skill_id == "s-1"
        assert req.name == "Go"
        assert req.level == "advanced"
        assert req.order_index == 3


class TestSkillResponseFromEntity:
    def test_maps_all_fields(self):
        entity = _make_skill_entity()
        resp = SkillResponse.from_entity(entity)

        assert resp.id == "s-1"
        assert resp.profile_id == "p-1"
        assert resp.name == "Python"
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
