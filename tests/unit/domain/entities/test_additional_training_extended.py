"""
Extended tests for AdditionalTraining Entity.

Covers uncovered lines: empty string normalization for duration/certificate_url/description,
update_technologies(), update_order(), update_info() with individual fields,
technology too long, and __repr__.
"""

from datetime import datetime

import pytest

from app.domain.entities.additional_training import AdditionalTraining
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidProviderError,
    InvalidTitleError,
    InvalidURLError,
)

COMPLETION_DATE = datetime(2024, 1, 15)


def _make_training(profile_id, **kwargs):
    defaults = {
        "profile_id": profile_id,
        "title": "Python Course",
        "provider": "Udemy",
        "completion_date": COMPLETION_DATE,
        "order_index": 0,
    }
    defaults.update(kwargs)
    return AdditionalTraining.create(**defaults)


@pytest.mark.entity
class TestAdditionalTrainingEmptyStringNormalization:
    """Test that optional fields with empty strings are normalized to None."""

    def test_empty_duration_normalized_to_none(self, profile_id):
        """Empty duration should be stored as None."""
        training = _make_training(profile_id, duration="")

        assert training.duration is None

    def test_whitespace_duration_normalized_to_none(self, profile_id):
        """Whitespace duration should be stored as None."""
        training = _make_training(profile_id, duration="   ")

        assert training.duration is None

    def test_empty_certificate_url_normalized_to_none(self, profile_id):
        """Empty certificate_url should be stored as None."""
        training = _make_training(profile_id, certificate_url="")

        assert training.certificate_url is None

    def test_whitespace_certificate_url_normalized_to_none(self, profile_id):
        """Whitespace certificate_url should be stored as None."""
        training = _make_training(profile_id, certificate_url="   ")

        assert training.certificate_url is None

    def test_empty_description_normalized_to_none(self, profile_id):
        """Empty description should be stored as None."""
        training = _make_training(profile_id, description="")

        assert training.description is None

    def test_whitespace_description_normalized_to_none(self, profile_id):
        """Whitespace description should be stored as None."""
        training = _make_training(profile_id, description="   ")

        assert training.description is None


@pytest.mark.entity
@pytest.mark.business_rule
class TestAdditionalTrainingValidation:
    """Test validation rules for AdditionalTraining."""

    def test_empty_profile_id_at_update_raises_error(self):
        """Empty profile_id should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            AdditionalTraining.create(
                profile_id="   ",
                title="Course",
                provider="Udemy",
                completion_date=COMPLETION_DATE,
                order_index=0,
            )

    def test_empty_title_raises_error(self, profile_id):
        """Empty title should raise InvalidTitleError."""
        with pytest.raises(InvalidTitleError):
            _make_training(profile_id, title="")

    def test_title_too_long_raises_error(self, profile_id):
        """Title > 100 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_training(profile_id, title="x" * 101)

    def test_empty_provider_raises_error(self, profile_id):
        """Empty provider should raise InvalidProviderError."""
        with pytest.raises(InvalidProviderError):
            _make_training(profile_id, provider="")

    def test_provider_too_long_raises_error(self, profile_id):
        """Provider > 100 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_training(profile_id, provider="x" * 101)

    def test_duration_too_long_raises_error(self, profile_id):
        """Duration > 50 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_training(profile_id, duration="x" * 51)

    def test_invalid_certificate_url_raises_error(self, profile_id):
        """Invalid URL format for certificate_url should raise InvalidURLError."""
        with pytest.raises(InvalidURLError):
            _make_training(profile_id, certificate_url="not-a-url")

    def test_description_too_long_raises_error(self, profile_id):
        """Description > 500 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_training(profile_id, description="x" * 501)

    def test_negative_order_index_raises_error(self, profile_id):
        """Negative order_index should raise InvalidOrderIndexError."""
        with pytest.raises(InvalidOrderIndexError):
            _make_training(profile_id, order_index=-1)

    def test_too_many_technologies_raises_error(self, profile_id):
        """More than 20 technologies should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_training(profile_id, technologies=[f"Tech{i}" for i in range(21)])

    def test_empty_technology_item_raises_error(self, profile_id):
        """Empty string in technologies list should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            _make_training(profile_id, technologies=["Python", ""])

    def test_technology_item_too_long_raises_error(self, profile_id):
        """Technology item > 150 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_training(profile_id, technologies=["x" * 151])


@pytest.mark.entity
class TestAdditionalTrainingUpdateInfo:
    """Test update_info() method."""

    def test_update_title(self, profile_id):
        """Should update title."""
        training = _make_training(profile_id)
        training.update_info(title="New Title")

        assert training.title == "New Title"

    def test_update_provider(self, profile_id):
        """Should update provider."""
        training = _make_training(profile_id)
        training.update_info(provider="Coursera")

        assert training.provider == "Coursera"

    def test_update_completion_date(self, profile_id):
        """Should update completion_date."""
        training = _make_training(profile_id)
        new_date = datetime(2025, 6, 1)
        training.update_info(completion_date=new_date)

        assert training.completion_date == new_date

    def test_update_duration(self, profile_id):
        """Should update duration."""
        training = _make_training(profile_id)
        training.update_info(duration="60h")

        assert training.duration == "60h"

    def test_update_certificate_url(self, profile_id):
        """Should update certificate_url."""
        training = _make_training(profile_id)
        training.update_info(certificate_url="https://example.com/cert")

        assert training.certificate_url == "https://example.com/cert"

    def test_update_description(self, profile_id):
        """Should update description."""
        training = _make_training(profile_id)
        training.update_info(description="New description")

        assert training.description == "New description"

    def test_update_info_invalid_title_raises(self, profile_id):
        """Updating with invalid title should raise error."""
        training = _make_training(profile_id)

        with pytest.raises(InvalidTitleError):
            training.update_info(title="")

    def test_update_info_invalid_certificate_url_raises(self, profile_id):
        """Updating with invalid URL should raise error."""
        training = _make_training(profile_id)

        with pytest.raises(InvalidURLError):
            training.update_info(certificate_url="not-a-url")


@pytest.mark.entity
class TestAdditionalTrainingUpdateTechnologies:
    """Test update_technologies() method."""

    def test_update_technologies(self, profile_id):
        """Should replace technologies list."""
        training = _make_training(profile_id, technologies=["Python"])
        training.update_technologies(["FastAPI", "MongoDB"])

        assert training.technologies == ["FastAPI", "MongoDB"]

    def test_update_technologies_empty_list(self, profile_id):
        """Should accept empty list."""
        training = _make_training(profile_id, technologies=["Python"])
        training.update_technologies([])

        assert training.technologies == []

    def test_update_technologies_invalid_raises(self, profile_id):
        """Updating with invalid technologies should raise error."""
        training = _make_training(profile_id)

        with pytest.raises(InvalidLengthError):
            training.update_technologies([f"Tech{i}" for i in range(21)])


@pytest.mark.entity
class TestAdditionalTrainingUpdateOrder:
    """Test update_order() method."""

    def test_update_order(self, profile_id):
        """Should update order_index."""
        training = _make_training(profile_id, order_index=0)
        training.update_order(5)

        assert training.order_index == 5

    def test_update_order_negative_raises(self, profile_id):
        """Negative order_index should raise InvalidOrderIndexError."""
        training = _make_training(profile_id)

        with pytest.raises(InvalidOrderIndexError):
            training.update_order(-1)


@pytest.mark.entity
class TestAdditionalTrainingRepr:
    """Test __repr__ method."""

    def test_repr_contains_relevant_fields(self, profile_id):
        """__repr__ should include id, title, and provider."""
        training = _make_training(profile_id)

        result = repr(training)

        assert "AdditionalTraining" in result
        assert "Python Course" in result
        assert "Udemy" in result
