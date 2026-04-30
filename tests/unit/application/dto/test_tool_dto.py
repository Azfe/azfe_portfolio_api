"""Tests for Tool DTOs."""

import pytest

from app.application.dto.tool_dto import ToolListResponse, ToolResponse

from ..dto.conftest import DT, DT2, make_entity


def _make_tool_entity(**overrides):
    defaults = {
        "id": "t-1",
        "profile_id": "p-1",
        "name": "Docker",
        "order_index": 0,
        "category": "Container",
        "icon_url": "https://docker.com/icon.png",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestToolResponseFromEntity:
    @pytest.mark.unit
    def test_maps_all_fields(self):
        entity = _make_tool_entity()
        resp = ToolResponse.from_entity(entity)

        assert resp.id == "t-1"
        assert resp.profile_id == "p-1"
        assert resp.name == "Docker"
        assert resp.order_index == 0
        assert resp.category == "Container"
        assert resp.icon_url == "https://docker.com/icon.png"
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_optional_category_absent(self):
        entity = _make_tool_entity(category=None)
        resp = ToolResponse.from_entity(entity)

        assert resp.category is None

    @pytest.mark.unit
    def test_optional_icon_url_absent(self):
        entity = _make_tool_entity(icon_url=None)
        resp = ToolResponse.from_entity(entity)

        assert resp.icon_url is None

    @pytest.mark.unit
    def test_both_optional_fields_absent(self):
        entity = _make_tool_entity(category=None, icon_url=None)
        resp = ToolResponse.from_entity(entity)

        assert resp.category is None
        assert resp.icon_url is None

    @pytest.mark.unit
    def test_returns_correct_type(self):
        entity = _make_tool_entity()
        resp = ToolResponse.from_entity(entity)

        assert isinstance(resp, ToolResponse)

    @pytest.mark.unit
    def test_required_fields_always_present(self):
        entity = _make_tool_entity(category=None, icon_url=None)
        resp = ToolResponse.from_entity(entity)

        assert resp.id == "t-1"
        assert resp.profile_id == "p-1"
        assert resp.name == "Docker"
        assert resp.order_index == 0

    @pytest.mark.unit
    def test_timestamps_preserved(self):
        entity = _make_tool_entity()
        resp = ToolResponse.from_entity(entity)

        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_different_order_index(self):
        entity = _make_tool_entity(order_index=7)
        resp = ToolResponse.from_entity(entity)

        assert resp.order_index == 7

    @pytest.mark.unit
    def test_id_type_is_str(self):
        entity = _make_tool_entity()
        resp = ToolResponse.from_entity(entity)

        assert isinstance(resp.id, str)

    @pytest.mark.unit
    def test_name_type_is_str(self):
        entity = _make_tool_entity()
        resp = ToolResponse.from_entity(entity)

        assert isinstance(resp.name, str)

    @pytest.mark.unit
    def test_order_index_type_is_int(self):
        entity = _make_tool_entity()
        resp = ToolResponse.from_entity(entity)

        assert isinstance(resp.order_index, int)


class TestToolListResponseFromEntities:
    @pytest.mark.unit
    def test_maps_list(self):
        entities = [
            _make_tool_entity(id="t-1", name="Docker"),
            _make_tool_entity(id="t-2", name="PostgreSQL"),
        ]
        resp = ToolListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.tools) == 2

    @pytest.mark.unit
    def test_items_are_correctly_mapped(self):
        entities = [
            _make_tool_entity(id="t-1", name="Docker"),
            _make_tool_entity(id="t-2", name="PostgreSQL"),
        ]
        resp = ToolListResponse.from_entities(entities)

        assert resp.tools[0].name == "Docker"
        assert resp.tools[1].name == "PostgreSQL"

    @pytest.mark.unit
    def test_empty_list(self):
        resp = ToolListResponse.from_entities([])

        assert resp.total == 0
        assert resp.tools == []

    @pytest.mark.unit
    def test_returns_correct_type(self):
        resp = ToolListResponse.from_entities([])

        assert isinstance(resp, ToolListResponse)

    @pytest.mark.unit
    def test_single_item_list(self):
        entities = [_make_tool_entity(id="t-1")]
        resp = ToolListResponse.from_entities(entities)

        assert resp.total == 1
        assert len(resp.tools) == 1
        assert isinstance(resp.tools[0], ToolResponse)

    @pytest.mark.unit
    def test_total_matches_list_length(self):
        entities = [_make_tool_entity(id=f"t-{i}", name=f"Tool {i}") for i in range(5)]
        resp = ToolListResponse.from_entities(entities)

        assert resp.total == len(resp.tools) == 5
