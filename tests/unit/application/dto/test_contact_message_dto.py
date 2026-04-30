"""Tests for ContactMessage DTOs."""

from datetime import datetime

import pytest

from app.application.dto.contact_message_dto import (
    ContactMessageListResponse,
    ContactMessageResponse,
)

from .conftest import DT, make_entity


def _make_contact_message_entity(**overrides):
    """Build a MagicMock ContactMessage entity with sensible defaults."""
    defaults = {
        "id": "cm-1",
        "name": "Alex Zapata",
        "email": "alex@azfe.dev",
        "message": "Hello, I would like to get in touch with you.",
        "status": "pending",
        "created_at": DT,
        "read_at": None,
        "replied_at": None,
    }
    defaults.update(overrides)
    # ContactMessage has no updated_at; remove it from the mock baseline
    entity = make_entity(**defaults)
    # make_entity always sets updated_at — remove it to avoid false assertions
    del entity.updated_at
    return entity


class TestContactMessageResponseFromEntity:
    @pytest.mark.unit
    def test_maps_all_fields(self):
        read_at = datetime(2025, 2, 1, 9, 0, 0)
        replied_at = datetime(2025, 2, 2, 10, 0, 0)
        entity = _make_contact_message_entity(
            read_at=read_at,
            replied_at=replied_at,
            status="replied",
        )
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.id == "cm-1"
        assert resp.name == "Alex Zapata"
        assert resp.email == "alex@azfe.dev"
        assert resp.message == "Hello, I would like to get in touch with you."
        assert resp.status == "replied"
        assert resp.created_at == DT
        assert resp.read_at == read_at
        assert resp.replied_at == replied_at

    @pytest.mark.unit
    def test_optional_read_at_is_none(self):
        entity = _make_contact_message_entity(read_at=None)
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.read_at is None

    @pytest.mark.unit
    def test_optional_replied_at_is_none(self):
        entity = _make_contact_message_entity(replied_at=None)
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.replied_at is None

    @pytest.mark.unit
    def test_all_optional_timestamp_fields_absent(self):
        entity = _make_contact_message_entity(read_at=None, replied_at=None)
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.read_at is None
        assert resp.replied_at is None

    @pytest.mark.unit
    def test_required_fields_always_present(self):
        entity = _make_contact_message_entity(read_at=None, replied_at=None)
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.id == "cm-1"
        assert resp.name == "Alex Zapata"
        assert resp.email == "alex@azfe.dev"
        assert resp.message == "Hello, I would like to get in touch with you."
        assert resp.status == "pending"
        assert resp.created_at == DT

    @pytest.mark.unit
    def test_returns_correct_type(self):
        entity = _make_contact_message_entity()
        resp = ContactMessageResponse.from_entity(entity)

        assert isinstance(resp, ContactMessageResponse)

    @pytest.mark.unit
    def test_created_at_preserved(self):
        entity = _make_contact_message_entity()
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.created_at == DT

    @pytest.mark.unit
    def test_status_read(self):
        read_at = datetime(2025, 3, 5, 14, 0, 0)
        entity = _make_contact_message_entity(status="read", read_at=read_at)
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.status == "read"
        assert resp.read_at == read_at
        assert resp.replied_at is None

    @pytest.mark.unit
    def test_status_pending_default(self):
        entity = _make_contact_message_entity(status="pending")
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.status == "pending"

    @pytest.mark.unit
    def test_field_types(self):
        read_at = datetime(2025, 2, 1, 9, 0, 0)
        replied_at = datetime(2025, 2, 2, 10, 0, 0)
        entity = _make_contact_message_entity(
            read_at=read_at,
            replied_at=replied_at,
            status="replied",
        )
        resp = ContactMessageResponse.from_entity(entity)

        assert isinstance(resp.id, str)
        assert isinstance(resp.name, str)
        assert isinstance(resp.email, str)
        assert isinstance(resp.message, str)
        assert isinstance(resp.status, str)
        assert isinstance(resp.created_at, datetime)
        assert isinstance(resp.read_at, datetime)
        assert isinstance(resp.replied_at, datetime)

    @pytest.mark.unit
    def test_different_sender(self):
        entity = _make_contact_message_entity(
            id="cm-99",
            name="Jane Doe",
            email="jane@example.com",
        )
        resp = ContactMessageResponse.from_entity(entity)

        assert resp.id == "cm-99"
        assert resp.name == "Jane Doe"
        assert resp.email == "jane@example.com"


class TestContactMessageListResponseFromEntities:
    @pytest.mark.unit
    def test_maps_list(self):
        entities = [
            _make_contact_message_entity(id="cm-1", name="Alex Zapata"),
            _make_contact_message_entity(id="cm-2", name="Jane Doe"),
        ]
        resp = ContactMessageListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.messages) == 2

    @pytest.mark.unit
    def test_items_are_correctly_mapped(self):
        entities = [
            _make_contact_message_entity(id="cm-1", name="Alex Zapata"),
            _make_contact_message_entity(id="cm-2", name="Jane Doe"),
        ]
        resp = ContactMessageListResponse.from_entities(entities)

        assert resp.messages[0].name == "Alex Zapata"
        assert resp.messages[1].name == "Jane Doe"

    @pytest.mark.unit
    def test_empty_list(self):
        resp = ContactMessageListResponse.from_entities([])

        assert resp.total == 0
        assert resp.messages == []

    @pytest.mark.unit
    def test_returns_correct_type(self):
        resp = ContactMessageListResponse.from_entities([])

        assert isinstance(resp, ContactMessageListResponse)

    @pytest.mark.unit
    def test_single_item_list(self):
        entities = [_make_contact_message_entity(id="cm-1")]
        resp = ContactMessageListResponse.from_entities(entities)

        assert resp.total == 1
        assert len(resp.messages) == 1
        assert isinstance(resp.messages[0], ContactMessageResponse)

    @pytest.mark.unit
    def test_items_preserve_status(self):
        read_at = datetime(2025, 3, 1, 8, 0, 0)
        entities = [
            _make_contact_message_entity(id="cm-1", status="pending"),
            _make_contact_message_entity(id="cm-2", status="read", read_at=read_at),
        ]
        resp = ContactMessageListResponse.from_entities(entities)

        assert resp.messages[0].status == "pending"
        assert resp.messages[1].status == "read"
