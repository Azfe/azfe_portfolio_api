"""Tests for AdditionalTraining Entity."""

from datetime import datetime

import pytest

from app.domain.entities.additional_training import AdditionalTraining
from app.domain.exceptions import (
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidProviderError,
    InvalidTitleError,
    InvalidURLError,
)


@pytest.mark.entity
class TestAdditionalTrainingCreation:
    """Test AdditionalTraining creation."""

    def test_create_with_required_fields(self, profile_id):
        at = AdditionalTraining.create(
            profile_id=profile_id,
            title="Docker Mastery",
            provider="Udemy",
            completion_date=datetime(2023, 6, 1),
            order_index=0,
        )
        assert at.title == "Docker Mastery"
        assert at.provider == "Udemy"
        assert at.duration is None
        assert at.certificate_url is None
        assert at.description is None

    def test_create_with_all_fields(self, profile_id):
        at = AdditionalTraining.create(
            profile_id=profile_id,
            title="Docker Mastery",
            provider="Udemy",
            completion_date=datetime(2023, 6, 1),
            order_index=0,
            duration="40 hours",
            certificate_url="https://udemy.com/cert/123",
            description="Complete Docker course",
        )
        assert at.duration == "40 hours"
        assert at.certificate_url == "https://udemy.com/cert/123"
        assert at.description == "Complete Docker course"


@pytest.mark.entity
@pytest.mark.business_rule
class TestAdditionalTrainingValidation:
    """Test AdditionalTraining validation rules."""

    def test_empty_title_raises_error(self, profile_id):
        with pytest.raises(InvalidTitleError):
            AdditionalTraining.create(
                profile_id=profile_id,
                title="",
                provider="Udemy",
                completion_date=datetime(2023, 6, 1),
                order_index=0,
            )

    def test_title_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            AdditionalTraining.create(
                profile_id=profile_id,
                title="x" * 101,
                provider="Udemy",
                completion_date=datetime(2023, 6, 1),
                order_index=0,
            )

    def test_empty_provider_raises_error(self, profile_id):
        with pytest.raises(InvalidProviderError):
            AdditionalTraining.create(
                profile_id=profile_id,
                title="Docker",
                provider="",
                completion_date=datetime(2023, 6, 1),
                order_index=0,
            )

    def test_provider_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            AdditionalTraining.create(
                profile_id=profile_id,
                title="Docker",
                provider="x" * 101,
                completion_date=datetime(2023, 6, 1),
                order_index=0,
            )

    def test_duration_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            AdditionalTraining.create(
                profile_id=profile_id,
                title="Docker",
                provider="Udemy",
                completion_date=datetime(2023, 6, 1),
                order_index=0,
                duration="x" * 51,
            )

    def test_empty_duration_becomes_none(self, profile_id):
        at = AdditionalTraining.create(
            profile_id=profile_id,
            title="Docker",
            provider="Udemy",
            completion_date=datetime(2023, 6, 1),
            order_index=0,
            duration="   ",
        )
        assert at.duration is None

    def test_invalid_certificate_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            AdditionalTraining.create(
                profile_id=profile_id,
                title="Docker",
                provider="Udemy",
                completion_date=datetime(2023, 6, 1),
                order_index=0,
                certificate_url="not-a-url",
            )

    def test_empty_certificate_url_becomes_none(self, profile_id):
        at = AdditionalTraining.create(
            profile_id=profile_id,
            title="Docker",
            provider="Udemy",
            completion_date=datetime(2023, 6, 1),
            order_index=0,
            certificate_url="   ",
        )
        assert at.certificate_url is None

    def test_description_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            AdditionalTraining.create(
                profile_id=profile_id,
                title="Docker",
                provider="Udemy",
                completion_date=datetime(2023, 6, 1),
                order_index=0,
                description="x" * 501,
            )

    def test_empty_description_becomes_none(self, profile_id):
        at = AdditionalTraining.create(
            profile_id=profile_id,
            title="Docker",
            provider="Udemy",
            completion_date=datetime(2023, 6, 1),
            order_index=0,
            description="   ",
        )
        assert at.description is None

    def test_negative_order_index_raises_error(self, profile_id):
        with pytest.raises(InvalidOrderIndexError):
            AdditionalTraining.create(
                profile_id=profile_id,
                title="Docker",
                provider="Udemy",
                completion_date=datetime(2023, 6, 1),
                order_index=-1,
            )


@pytest.mark.entity
class TestAdditionalTrainingUpdate:
    """Test AdditionalTraining updates."""

    def _make(self, profile_id):
        return AdditionalTraining.create(
            profile_id=profile_id,
            title="Docker",
            provider="Udemy",
            completion_date=datetime(2023, 6, 1),
            order_index=0,
        )

    def test_update_info(self, profile_id):
        at = self._make(profile_id)
        at.update_info(title="Kubernetes", provider="Coursera", duration="20 hours")
        assert at.title == "Kubernetes"
        assert at.provider == "Coursera"
        assert at.duration == "20 hours"

    def test_update_info_invalid_title_raises(self, profile_id):
        at = self._make(profile_id)
        with pytest.raises(InvalidTitleError):
            at.update_info(title="")

    def test_update_certificate_url(self, profile_id):
        at = self._make(profile_id)
        at.update_info(certificate_url="https://example.com/cert")
        assert at.certificate_url == "https://example.com/cert"

    def test_update_order(self, profile_id):
        at = self._make(profile_id)
        at.update_order(5)
        assert at.order_index == 5

    def test_update_order_negative_raises(self, profile_id):
        at = self._make(profile_id)
        with pytest.raises(InvalidOrderIndexError):
            at.update_order(-1)
