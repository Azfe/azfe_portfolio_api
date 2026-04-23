"""Tests for Certification Entity."""

from datetime import datetime, timedelta

import pytest

from app.domain.entities.certification import Certification
from app.domain.exceptions import (
    InvalidDateRangeError,
    InvalidIssuerError,
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidTitleError,
    InvalidURLError,
)


@pytest.mark.entity
class TestCertificationCreation:
    """Test Certification creation."""

    def test_create_with_required_fields(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS Solutions Architect",
            issuer="Amazon",
            issue_date=datetime(2023, 6, 1),
            order_index=0,
        )
        assert c.title == "AWS Solutions Architect"
        assert c.issuer == "Amazon"
        assert c.expiry_date is None
        assert c.credential_id is None
        assert c.credential_url is None

    def test_create_with_all_fields(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS Solutions Architect",
            issuer="Amazon",
            issue_date=datetime(2023, 6, 1),
            order_index=0,
            expiry_date=datetime(2026, 6, 1),
            credential_id="ABC-123",
            credential_url="https://aws.amazon.com/verify/ABC-123",
        )
        assert c.expiry_date == datetime(2026, 6, 1)
        assert c.credential_id == "ABC-123"
        assert c.credential_url == "https://aws.amazon.com/verify/ABC-123"


@pytest.mark.entity
@pytest.mark.business_rule
class TestCertificationValidation:
    """Test Certification validation rules."""

    def test_empty_title_raises_error(self, profile_id):
        with pytest.raises(InvalidTitleError):
            Certification.create(
                profile_id=profile_id,
                title="",
                issuer="Amazon",
                issue_date=datetime(2023, 6, 1),
                order_index=0,
            )

    def test_title_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Certification.create(
                profile_id=profile_id,
                title="x" * 101,
                issuer="Amazon",
                issue_date=datetime(2023, 6, 1),
                order_index=0,
            )

    def test_empty_issuer_raises_error(self, profile_id):
        with pytest.raises(InvalidIssuerError):
            Certification.create(
                profile_id=profile_id,
                title="AWS",
                issuer="",
                issue_date=datetime(2023, 6, 1),
                order_index=0,
            )

    def test_issuer_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Certification.create(
                profile_id=profile_id,
                title="AWS",
                issuer="x" * 101,
                issue_date=datetime(2023, 6, 1),
                order_index=0,
            )

    def test_expiry_before_issue_raises_error(self, profile_id):
        with pytest.raises(InvalidDateRangeError):
            Certification.create(
                profile_id=profile_id,
                title="AWS",
                issuer="Amazon",
                issue_date=datetime(2023, 6, 1),
                order_index=0,
                expiry_date=datetime(2023, 1, 1),
            )

    def test_credential_id_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Certification.create(
                profile_id=profile_id,
                title="AWS",
                issuer="Amazon",
                issue_date=datetime(2023, 6, 1),
                order_index=0,
                credential_id="x" * 101,
            )

    def test_invalid_credential_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            Certification.create(
                profile_id=profile_id,
                title="AWS",
                issuer="Amazon",
                issue_date=datetime(2023, 6, 1),
                order_index=0,
                credential_url="not-a-url",
            )

    def test_negative_order_index_raises_error(self, profile_id):
        with pytest.raises(InvalidOrderIndexError):
            Certification.create(
                profile_id=profile_id,
                title="AWS",
                issuer="Amazon",
                issue_date=datetime(2023, 6, 1),
                order_index=-1,
            )

    def test_empty_credential_id_becomes_none(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS",
            issuer="Amazon",
            issue_date=datetime(2023, 6, 1),
            order_index=0,
            credential_id="   ",
        )
        assert c.credential_id is None

    def test_empty_credential_url_becomes_none(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS",
            issuer="Amazon",
            issue_date=datetime(2023, 6, 1),
            order_index=0,
            credential_url="   ",
        )
        assert c.credential_url is None


@pytest.mark.entity
class TestCertificationUpdate:
    """Test Certification updates."""

    def _make(self, profile_id):
        return Certification.create(
            profile_id=profile_id,
            title="AWS",
            issuer="Amazon",
            issue_date=datetime(2023, 6, 1),
            order_index=0,
        )

    def test_update_info(self, profile_id):
        c = self._make(profile_id)
        c.update_info(title="Azure", issuer="Microsoft")
        assert c.title == "Azure"
        assert c.issuer == "Microsoft"

    def test_update_info_invalid_title_raises(self, profile_id):
        c = self._make(profile_id)
        with pytest.raises(InvalidTitleError):
            c.update_info(title="")

    def test_update_credential_url(self, profile_id):
        c = self._make(profile_id)
        c.update_info(credential_url="https://verify.example.com/123")
        assert c.credential_url == "https://verify.example.com/123"

    def test_update_order(self, profile_id):
        c = self._make(profile_id)
        c.update_order(3)
        assert c.order_index == 3


@pytest.mark.entity
class TestCertificationBusinessMethods:
    """Test Certification business methods."""

    def test_is_expired_past_date(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS",
            issuer="Amazon",
            issue_date=datetime(2020, 1, 1),
            order_index=0,
            expiry_date=datetime(2021, 1, 1),
        )
        assert c.is_expired() is True

    def test_is_not_expired_future_date(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS",
            issuer="Amazon",
            issue_date=datetime(2023, 1, 1),
            order_index=0,
            expiry_date=datetime.utcnow() + timedelta(days=365),
        )
        assert c.is_expired() is False

    def test_is_not_expired_no_expiry(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS",
            issuer="Amazon",
            issue_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert c.is_expired() is False

    def test_has_no_expiry(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS",
            issuer="Amazon",
            issue_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert c.has_no_expiry() is True

    def test_has_expiry(self, profile_id):
        c = Certification.create(
            profile_id=profile_id,
            title="AWS",
            issuer="Amazon",
            issue_date=datetime(2023, 1, 1),
            order_index=0,
            expiry_date=datetime(2026, 1, 1),
        )
        assert c.has_no_expiry() is False
