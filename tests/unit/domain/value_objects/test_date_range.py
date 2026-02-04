"""
Tests for DateRange Value Object.
"""

import pytest
from datetime import datetime
from app.domain.value_objects.date_range import DateRange
from app.domain.exceptions import InvalidDateRangeError


@pytest.mark.value_object
class TestDateRangeCreation:
    """Test DateRange creation."""

    def test_create_completed_range(self, yesterday, today):
        """Should create completed range."""
        dr = DateRange.completed(yesterday, today)
        
        assert dr.start_date == yesterday
        assert dr.end_date == today

    def test_create_ongoing_range(self, yesterday):
        """Should create ongoing range."""
        dr = DateRange.ongoing(yesterday)
        
        assert dr.start_date == yesterday
        assert dr.end_date is None


@pytest.mark.value_object
class TestDateRangeValidation:
    """Test DateRange validation."""

    def test_end_before_start_raises_error(self, yesterday, today):
        """Should raise error when end < start."""
        with pytest.raises(InvalidDateRangeError):
            DateRange.completed(today, yesterday)


@pytest.mark.value_object
class TestDateRangeQueries:
    """Test DateRange queries."""

    def test_is_ongoing_true(self, yesterday):
        """Should return True for ongoing."""
        dr = DateRange.ongoing(yesterday)
        
        assert dr.is_ongoing() is True

    def test_is_ongoing_false(self, yesterday, today):
        """Should return False for completed."""
        dr = DateRange.completed(yesterday, today)
        
        assert dr.is_ongoing() is False

    def test_duration_days(self):
        """Should calculate duration."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 11)
        dr = DateRange.completed(start, end)
        
        assert dr.duration_days() == 10


@pytest.mark.value_object
class TestDateRangeImmutability:
    """Test DateRange immutability."""

    def test_immutable(self, yesterday, today):
        """Should not allow modification."""
        dr = DateRange.completed(yesterday, today)
        
        with pytest.raises(AttributeError):
            dr.start_date = datetime.now()