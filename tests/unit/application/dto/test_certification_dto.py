"""Tests for Certification DTOs."""

import pytest

from app.application.dto.certification_dto import (
    CertificationListResponse,
    CertificationResponse,
)

from .conftest import DT, DT2, DT_END, DT_START, make_entity

# Fixed dates that are deterministic regardless of when the tests run.
# PAST_DATE is definitively in the past; FUTURE_DATE is definitively in the future.
PAST_DATE = DT_START  # 2024-01-01 — already passed
FUTURE_DATE = DT_END  # 2024-12-31 — still in the future relative to issue_date,
# but we drive is_expired via the mock return value, not
# by re-implementing the logic here.


def _make_certification_entity(**overrides):
    """Build a MagicMock certification entity with sensible defaults."""
    defaults = {
        "id": "cert-1",
        "profile_id": "p-1",
        "title": "AWS Certified Solutions Architect",
        "issuer": "Amazon Web Services",
        "issue_date": DT_START,
        "order_index": 0,
        "expiry_date": DT_END,
        "credential_id": "AWS-SAA-C03-12345",
        "credential_url": "https://aws.amazon.com/verify/cert-123",
    }
    # Separate the special _is_expired control key before passing to make_entity
    is_expired_value = overrides.pop("_is_expired", False)
    defaults.update(overrides)
    entity = make_entity(**defaults)
    entity.is_expired.return_value = is_expired_value
    return entity


class TestCertificationResponseFromEntity:
    @pytest.mark.unit
    def test_maps_all_fields(self):
        entity = _make_certification_entity()
        resp = CertificationResponse.from_entity(entity)

        assert resp.id == "cert-1"
        assert resp.profile_id == "p-1"
        assert resp.title == "AWS Certified Solutions Architect"
        assert resp.issuer == "Amazon Web Services"
        assert resp.issue_date == DT_START
        assert resp.order_index == 0
        assert resp.expiry_date == DT_END
        assert resp.credential_id == "AWS-SAA-C03-12345"
        assert resp.credential_url == "https://aws.amazon.com/verify/cert-123"
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_returns_correct_type(self):
        entity = _make_certification_entity()
        resp = CertificationResponse.from_entity(entity)

        assert isinstance(resp, CertificationResponse)

    @pytest.mark.unit
    def test_timestamps_preserved(self):
        entity = _make_certification_entity()
        resp = CertificationResponse.from_entity(entity)

        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_none_expiry_date(self):
        entity = _make_certification_entity(expiry_date=None, _is_expired=False)
        resp = CertificationResponse.from_entity(entity)

        assert resp.expiry_date is None

    @pytest.mark.unit
    def test_none_credential_id(self):
        entity = _make_certification_entity(credential_id=None)
        resp = CertificationResponse.from_entity(entity)

        assert resp.credential_id is None

    @pytest.mark.unit
    def test_none_credential_url(self):
        entity = _make_certification_entity(credential_url=None)
        resp = CertificationResponse.from_entity(entity)

        assert resp.credential_url is None

    @pytest.mark.unit
    def test_all_optional_fields_absent(self):
        entity = _make_certification_entity(
            expiry_date=None,
            credential_id=None,
            credential_url=None,
            _is_expired=False,
        )
        resp = CertificationResponse.from_entity(entity)

        assert resp.expiry_date is None
        assert resp.credential_id is None
        assert resp.credential_url is None

    @pytest.mark.unit
    def test_required_fields_always_present(self):
        entity = _make_certification_entity(
            expiry_date=None,
            credential_id=None,
            credential_url=None,
            _is_expired=False,
        )
        resp = CertificationResponse.from_entity(entity)

        assert resp.id == "cert-1"
        assert resp.profile_id == "p-1"
        assert resp.title == "AWS Certified Solutions Architect"
        assert resp.issuer == "Amazon Web Services"
        assert resp.issue_date == DT_START
        assert resp.order_index == 0

    @pytest.mark.unit
    def test_different_order_index(self):
        entity = _make_certification_entity(order_index=7)
        resp = CertificationResponse.from_entity(entity)

        assert resp.order_index == 7


class TestCertificationResponseIsExpired:
    """Tests focused on the `is_expired` calculated field."""

    @pytest.mark.unit
    def test_is_expired_true_when_entity_returns_true(self):
        """is_expired=True when entity.is_expired() returns True (past expiry_date)."""
        entity = _make_certification_entity(
            expiry_date=PAST_DATE,
            _is_expired=True,
        )
        resp = CertificationResponse.from_entity(entity)

        assert resp.is_expired is True

    @pytest.mark.unit
    def test_is_expired_false_when_no_expiry_date(self):
        """is_expired=False when no expiry_date is set."""
        entity = _make_certification_entity(
            expiry_date=None,
            _is_expired=False,
        )
        resp = CertificationResponse.from_entity(entity)

        assert resp.is_expired is False

    @pytest.mark.unit
    def test_is_expired_false_when_expiry_date_in_future(self):
        """is_expired=False when expiry_date is in the future."""
        entity = _make_certification_entity(
            expiry_date=FUTURE_DATE,
            _is_expired=False,
        )
        resp = CertificationResponse.from_entity(entity)

        assert resp.is_expired is False

    @pytest.mark.unit
    def test_is_expired_delegates_to_entity_method(self):
        """from_entity() calls entity.is_expired() to compute the field."""
        entity = _make_certification_entity(_is_expired=True)
        CertificationResponse.from_entity(entity)

        entity.is_expired.assert_called_once()


class TestCertificationListResponseFromEntities:
    @pytest.mark.unit
    def test_maps_list(self):
        entities = [
            _make_certification_entity(id="cert-1", title="AWS SAA"),
            _make_certification_entity(id="cert-2", title="GCP ACE"),
        ]
        resp = CertificationListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.certifications) == 2

    @pytest.mark.unit
    def test_items_are_correctly_mapped(self):
        entities = [
            _make_certification_entity(id="cert-1", title="AWS SAA"),
            _make_certification_entity(id="cert-2", title="GCP ACE"),
        ]
        resp = CertificationListResponse.from_entities(entities)

        assert resp.certifications[0].title == "AWS SAA"
        assert resp.certifications[1].title == "GCP ACE"

    @pytest.mark.unit
    def test_empty_list(self):
        resp = CertificationListResponse.from_entities([])

        assert resp.total == 0
        assert resp.certifications == []

    @pytest.mark.unit
    def test_returns_correct_type(self):
        resp = CertificationListResponse.from_entities([])

        assert isinstance(resp, CertificationListResponse)

    @pytest.mark.unit
    def test_single_item_list(self):
        entities = [_make_certification_entity(id="cert-1")]
        resp = CertificationListResponse.from_entities(entities)

        assert resp.total == 1
        assert len(resp.certifications) == 1
        assert isinstance(resp.certifications[0], CertificationResponse)

    @pytest.mark.unit
    def test_items_preserve_is_expired_flag(self):
        """Each item in the list carries the correct is_expired value."""
        expired = _make_certification_entity(
            id="cert-1", title="Old Cert", expiry_date=PAST_DATE, _is_expired=True
        )
        active = _make_certification_entity(
            id="cert-2", title="Active Cert", expiry_date=FUTURE_DATE, _is_expired=False
        )
        resp = CertificationListResponse.from_entities([expired, active])

        assert resp.certifications[0].is_expired is True
        assert resp.certifications[1].is_expired is False
