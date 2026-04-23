"""Unit tests for ContactInformationMapper."""

from app.domain.entities import ContactInformation
from app.infrastructure.mappers.contact_information_mapper import (
    ContactInformationMapper,
)

from .conftest import DT_CREATED, DT_UPDATED


class TestContactInformationMapperToDomain:
    def setup_method(self):
        self.mapper = ContactInformationMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "ci-1",
            "profile_id": "p-1",
            "email": "test@example.com",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "ci-1"
        assert entity.email == "test@example.com"
        assert entity.phone is None
        assert entity.linkedin is None
        assert entity.github is None
        assert entity.website is None

    def test_all_fields(self):
        doc = {
            "_id": "ci-1",
            "profile_id": "p-1",
            "email": "test@example.com",
            "phone": "+34 612-345-678",
            "linkedin": "https://linkedin.com/in/user",
            "github": "https://github.com/user",
            "website": "https://example.com",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.phone == "+34 612-345-678"
        assert entity.linkedin == "https://linkedin.com/in/user"
        assert entity.github == "https://github.com/user"
        assert entity.website == "https://example.com"


class TestContactInformationMapperToPersistence:
    def setup_method(self):
        self.mapper = ContactInformationMapper()

    def test_excludes_none_optionals(self):
        entity = ContactInformation(
            id="ci-1",
            profile_id="p-1",
            email="test@example.com",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert "phone" not in doc
        assert "linkedin" not in doc
        assert "github" not in doc
        assert "website" not in doc

    def test_includes_optionals_when_set(self):
        entity = ContactInformation(
            id="ci-1",
            profile_id="p-1",
            email="test@example.com",
            phone="+34 612-345-678",
            linkedin="https://linkedin.com/in/user",
            github="https://github.com/user",
            website="https://example.com",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["phone"] == "+34 612-345-678"
        assert doc["linkedin"] == "https://linkedin.com/in/user"
        assert doc["github"] == "https://github.com/user"
        assert doc["website"] == "https://example.com"

    def test_round_trip(self):
        doc = {
            "_id": "ci-1",
            "profile_id": "p-1",
            "email": "test@example.com",
            "phone": "+34 612-345-678",
            "linkedin": "https://linkedin.com/in/user",
            "github": "https://github.com/user",
            "website": "https://example.com",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
