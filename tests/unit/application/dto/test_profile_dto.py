"""Tests for Profile DTOs."""

from app.application.dto.profile_dto import ProfileResponse

from .conftest import DT, DT2, make_entity


def _make_profile_entity(**overrides):
    defaults = {
        "id": "p-1",
        "name": "John Doe",
        "headline": "Developer",
        "bio": "A bio",
        "location": "Madrid",
        "avatar_url": "https://img.com/a.png",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestProfileResponseFromEntity:
    def test_maps_all_fields(self):
        entity = _make_profile_entity()
        resp = ProfileResponse.from_entity(entity)

        assert resp.id == "p-1"
        assert resp.name == "John Doe"
        assert resp.headline == "Developer"
        assert resp.bio == "A bio"
        assert resp.location == "Madrid"
        assert resp.avatar_url == "https://img.com/a.png"
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    def test_none_optional_fields(self):
        entity = _make_profile_entity(bio=None, location=None, avatar_url=None)
        resp = ProfileResponse.from_entity(entity)

        assert resp.bio is None
        assert resp.location is None
        assert resp.avatar_url is None
