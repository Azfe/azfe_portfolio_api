"""Unit tests for ProfileMapper."""

from app.infrastructure.mappers.profile_mapper import ProfileMapper

from .conftest import DT_CREATED, DT_UPDATED


class TestProfileMapperToDomain:
    def setup_method(self):
        self.mapper = ProfileMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "p-1",
            "name": "John",
            "headline": "Dev",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "p-1"
        assert entity.name == "John"
        assert entity.headline == "Dev"
        assert entity.bio is None
        assert entity.location is None
        assert entity.avatar_url is None
        assert entity.created_at == DT_CREATED

    def test_all_fields(self):
        doc = {
            "_id": "p-1",
            "name": "John",
            "headline": "Dev",
            "bio": "A bio",
            "location": "Madrid",
            "avatar_url": "https://img.com/a.png",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.bio == "A bio"
        assert entity.location == "Madrid"
        assert entity.avatar_url == "https://img.com/a.png"

    def test_id_is_cast_to_str(self):
        doc = {
            "_id": 123,
            "name": "John",
            "headline": "Dev",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.id == "123"


class TestProfileMapperToPersistence:
    def setup_method(self):
        self.mapper = ProfileMapper()

    def test_required_fields_only(self):
        from app.domain.entities import Profile

        entity = Profile(
            id="p-1",
            name="John",
            headline="Dev",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["_id"] == "p-1"
        assert doc["name"] == "John"
        assert doc["headline"] == "Dev"
        assert "bio" not in doc
        assert "location" not in doc
        assert "avatar_url" not in doc

    def test_all_optional_fields_included(self):
        from app.domain.entities import Profile

        entity = Profile(
            id="p-1",
            name="John",
            headline="Dev",
            bio="A bio",
            location="Madrid",
            avatar_url="https://img.com/a.png",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["bio"] == "A bio"
        assert doc["location"] == "Madrid"
        assert doc["avatar_url"] == "https://img.com/a.png"

    def test_round_trip(self):
        doc = {
            "_id": "p-1",
            "name": "John",
            "headline": "Dev",
            "bio": "A bio",
            "location": "Madrid",
            "avatar_url": "https://img.com/a.png",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)

        assert result == doc
