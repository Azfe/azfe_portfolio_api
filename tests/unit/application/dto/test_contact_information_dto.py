"""Tests for ContactInformation DTOs."""

from datetime import datetime

import pytest

from app.application.dto.contact_information_dto import ContactInformationResponse

from .conftest import DT, DT2, make_entity


def _make_contact_information_entity(**overrides):
    """Build a MagicMock ContactInformation entity with sensible defaults."""
    defaults = {
        "id": "ci-1",
        "profile_id": "p-1",
        "email": "alex@azfe.dev",
        "phone": "+34600123456",
        "linkedin": "https://linkedin.com/in/alexzapata",
        "github": "https://github.com/alexzapata",
        "website": "https://azfe.dev",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestContactInformationResponseFromEntity:
    @pytest.mark.unit
    def test_maps_all_fields(self):
        entity = _make_contact_information_entity()
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.id == "ci-1"
        assert resp.profile_id == "p-1"
        assert resp.email == "alex@azfe.dev"
        assert resp.phone == "+34600123456"
        assert resp.linkedin == "https://linkedin.com/in/alexzapata"
        assert resp.github == "https://github.com/alexzapata"
        assert resp.website == "https://azfe.dev"
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_returns_correct_type(self):
        entity = _make_contact_information_entity()
        resp = ContactInformationResponse.from_entity(entity)

        assert isinstance(resp, ContactInformationResponse)

    @pytest.mark.unit
    def test_timestamps_preserved(self):
        entity = _make_contact_information_entity()
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_none_phone(self):
        entity = _make_contact_information_entity(phone=None)
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.phone is None

    @pytest.mark.unit
    def test_none_linkedin(self):
        entity = _make_contact_information_entity(linkedin=None)
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.linkedin is None

    @pytest.mark.unit
    def test_none_github(self):
        entity = _make_contact_information_entity(github=None)
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.github is None

    @pytest.mark.unit
    def test_none_website(self):
        entity = _make_contact_information_entity(website=None)
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.website is None

    @pytest.mark.unit
    def test_all_optional_fields_absent(self):
        entity = _make_contact_information_entity(
            phone=None,
            linkedin=None,
            github=None,
            website=None,
        )
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.phone is None
        assert resp.linkedin is None
        assert resp.github is None
        assert resp.website is None

    @pytest.mark.unit
    def test_required_fields_always_present(self):
        entity = _make_contact_information_entity(
            phone=None,
            linkedin=None,
            github=None,
            website=None,
        )
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.id == "ci-1"
        assert resp.profile_id == "p-1"
        assert resp.email == "alex@azfe.dev"

    @pytest.mark.unit
    def test_email_only(self):
        """Minimum viable entity: only required fields are set."""
        entity = _make_contact_information_entity(
            phone=None,
            linkedin=None,
            github=None,
            website=None,
        )
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.email == "alex@azfe.dev"
        assert resp.phone is None
        assert resp.linkedin is None
        assert resp.github is None
        assert resp.website is None

    @pytest.mark.unit
    def test_field_types(self):
        entity = _make_contact_information_entity()
        resp = ContactInformationResponse.from_entity(entity)

        assert isinstance(resp.id, str)
        assert isinstance(resp.profile_id, str)
        assert isinstance(resp.email, str)
        assert isinstance(resp.phone, str)
        assert isinstance(resp.linkedin, str)
        assert isinstance(resp.github, str)
        assert isinstance(resp.website, str)
        assert isinstance(resp.created_at, datetime)
        assert isinstance(resp.updated_at, datetime)

    @pytest.mark.unit
    def test_different_email(self):
        entity = _make_contact_information_entity(email="contact@example.com")
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.email == "contact@example.com"

    @pytest.mark.unit
    def test_profile_id_propagated(self):
        entity = _make_contact_information_entity(profile_id="profile-xyz")
        resp = ContactInformationResponse.from_entity(entity)

        assert resp.profile_id == "profile-xyz"
