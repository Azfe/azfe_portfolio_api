"""Unit tests for ContactMessageMapper."""

from app.domain.entities import ContactMessage
from app.infrastructure.mappers.contact_message_mapper import ContactMessageMapper

from .conftest import DT_CREATED, DT_READ, DT_REPLIED


class TestContactMessageMapperToDomain:
    def setup_method(self):
        self.mapper = ContactMessageMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "msg-1",
            "name": "Jane",
            "email": "jane@example.com",
            "message": "Hello, this is a test message for contact.",
            "created_at": DT_CREATED,
            "status": "pending",
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "msg-1"
        assert entity.name == "Jane"
        assert entity.email == "jane@example.com"
        assert entity.message == "Hello, this is a test message for contact."
        assert entity.status == "pending"
        assert entity.read_at is None
        assert entity.replied_at is None

    def test_all_fields(self):
        doc = {
            "_id": "msg-1",
            "name": "Jane",
            "email": "jane@example.com",
            "message": "Hello, this is a test message for contact.",
            "created_at": DT_CREATED,
            "status": "replied",
            "read_at": DT_READ,
            "replied_at": DT_REPLIED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.status == "replied"
        assert entity.read_at == DT_READ
        assert entity.replied_at == DT_REPLIED

    def test_missing_status_defaults_to_pending(self):
        doc = {
            "_id": "msg-1",
            "name": "Jane",
            "email": "jane@example.com",
            "message": "Hello, this is a test message for contact.",
            "created_at": DT_CREATED,
        }
        entity = self.mapper.to_domain(doc)
        assert entity.status == "pending"


class TestContactMessageMapperToPersistence:
    def setup_method(self):
        self.mapper = ContactMessageMapper()

    def test_excludes_none_optionals(self):
        entity = ContactMessage(
            id="msg-1",
            name="Jane",
            email="jane@example.com",
            message="Hello, this is a test message for contact.",
            created_at=DT_CREATED,
            status="pending",
        )
        doc = self.mapper.to_persistence(entity)

        assert "read_at" not in doc
        assert "replied_at" not in doc
        assert doc["status"] == "pending"

    def test_includes_optionals_when_set(self):
        entity = ContactMessage(
            id="msg-1",
            name="Jane",
            email="jane@example.com",
            message="Hello, this is a test message for contact.",
            created_at=DT_CREATED,
            status="replied",
            read_at=DT_READ,
            replied_at=DT_REPLIED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["read_at"] == DT_READ
        assert doc["replied_at"] == DT_REPLIED

    def test_round_trip(self):
        doc = {
            "_id": "msg-1",
            "name": "Jane",
            "email": "jane@example.com",
            "message": "Hello, this is a test message for contact.",
            "created_at": DT_CREATED,
            "status": "replied",
            "read_at": DT_READ,
            "replied_at": DT_REPLIED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
