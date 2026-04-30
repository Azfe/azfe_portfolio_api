"""Tests for SocialNetwork DTOs."""

import pytest

from app.application.dto.social_network_dto import (
    SocialNetworkListResponse,
    SocialNetworkResponse,
)

from .conftest import DT, DT2, make_entity


def _make_social_network_entity(**overrides):
    defaults = {
        "id": "sn-1",
        "profile_id": "p-1",
        "platform": "LinkedIn",
        "url": "https://linkedin.com/in/azfe",
        "order_index": 0,
        "username": "azfe",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestSocialNetworkResponseFromEntity:
    @pytest.mark.unit
    def test_maps_all_fields(self):
        entity = _make_social_network_entity()
        resp = SocialNetworkResponse.from_entity(entity)

        assert resp.id == "sn-1"
        assert resp.profile_id == "p-1"
        assert resp.platform == "LinkedIn"
        assert resp.url == "https://linkedin.com/in/azfe"
        assert resp.order_index == 0
        assert resp.username == "azfe"
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_username_none_when_absent(self):
        entity = _make_social_network_entity(username=None)
        resp = SocialNetworkResponse.from_entity(entity)

        assert resp.username is None

    @pytest.mark.unit
    def test_required_fields_always_present(self):
        entity = _make_social_network_entity(username=None)
        resp = SocialNetworkResponse.from_entity(entity)

        assert resp.id == "sn-1"
        assert resp.profile_id == "p-1"
        assert resp.platform == "LinkedIn"
        assert resp.url == "https://linkedin.com/in/azfe"
        assert resp.order_index == 0

    @pytest.mark.unit
    def test_returns_correct_type(self):
        entity = _make_social_network_entity()
        resp = SocialNetworkResponse.from_entity(entity)

        assert isinstance(resp, SocialNetworkResponse)

    @pytest.mark.unit
    def test_timestamps_preserved(self):
        entity = _make_social_network_entity()
        resp = SocialNetworkResponse.from_entity(entity)

        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_different_order_index(self):
        entity = _make_social_network_entity(order_index=3)
        resp = SocialNetworkResponse.from_entity(entity)

        assert resp.order_index == 3

    @pytest.mark.unit
    def test_different_platform(self):
        entity = _make_social_network_entity(
            platform="GitHub",
            url="https://github.com/azfe",
            username="azfe",
        )
        resp = SocialNetworkResponse.from_entity(entity)

        assert resp.platform == "GitHub"
        assert resp.url == "https://github.com/azfe"
        assert resp.username == "azfe"


class TestSocialNetworkListResponseFromEntities:
    @pytest.mark.unit
    def test_maps_list(self):
        entities = [
            _make_social_network_entity(id="sn-1", platform="LinkedIn"),
            _make_social_network_entity(id="sn-2", platform="GitHub"),
        ]
        resp = SocialNetworkListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.social_networks) == 2

    @pytest.mark.unit
    def test_items_are_correctly_mapped(self):
        entities = [
            _make_social_network_entity(id="sn-1", platform="LinkedIn"),
            _make_social_network_entity(id="sn-2", platform="GitHub"),
        ]
        resp = SocialNetworkListResponse.from_entities(entities)

        assert resp.social_networks[0].platform == "LinkedIn"
        assert resp.social_networks[1].platform == "GitHub"

    @pytest.mark.unit
    def test_empty_list(self):
        resp = SocialNetworkListResponse.from_entities([])

        assert resp.total == 0
        assert resp.social_networks == []

    @pytest.mark.unit
    def test_returns_correct_type(self):
        resp = SocialNetworkListResponse.from_entities([])

        assert isinstance(resp, SocialNetworkListResponse)

    @pytest.mark.unit
    def test_single_item_list(self):
        entities = [_make_social_network_entity(id="sn-1")]
        resp = SocialNetworkListResponse.from_entities(entities)

        assert resp.total == 1
        assert len(resp.social_networks) == 1
        assert isinstance(resp.social_networks[0], SocialNetworkResponse)
