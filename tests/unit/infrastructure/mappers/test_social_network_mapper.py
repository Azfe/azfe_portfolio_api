"""Unit tests for SocialNetworkMapper."""

from app.domain.entities import SocialNetwork
from app.infrastructure.mappers.social_network_mapper import SocialNetworkMapper

from .conftest import DT_CREATED, DT_UPDATED


class TestSocialNetworkMapperToDomain:
    def setup_method(self):
        self.mapper = SocialNetworkMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "sn-1",
            "profile_id": "p-1",
            "platform": "GitHub",
            "url": "https://github.com/user",
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "sn-1"
        assert entity.platform == "GitHub"
        assert entity.url == "https://github.com/user"
        assert entity.username is None

    def test_with_username(self):
        doc = {
            "_id": "sn-1",
            "profile_id": "p-1",
            "platform": "GitHub",
            "url": "https://github.com/user",
            "order_index": 0,
            "username": "user123",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.username == "user123"


class TestSocialNetworkMapperToPersistence:
    def setup_method(self):
        self.mapper = SocialNetworkMapper()

    def test_excludes_none_username(self):
        entity = SocialNetwork(
            id="sn-1",
            profile_id="p-1",
            platform="GitHub",
            url="https://github.com/user",
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert "username" not in doc

    def test_includes_username_when_set(self):
        entity = SocialNetwork(
            id="sn-1",
            profile_id="p-1",
            platform="GitHub",
            url="https://github.com/user",
            order_index=0,
            username="user123",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)
        assert doc["username"] == "user123"

    def test_round_trip(self):
        doc = {
            "_id": "sn-1",
            "profile_id": "p-1",
            "platform": "GitHub",
            "url": "https://github.com/user",
            "order_index": 0,
            "username": "user123",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
