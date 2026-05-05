"""
Extended tests for DateRange Value Object.

Covers uncovered methods: create(), ongoing(), completed(), contains_date(),
overlaps_with(), with_end_date(), duration_days() ongoing, and __str__/__repr__.
"""

from datetime import datetime

import pytest

from app.domain.exceptions import EmptyFieldError, InvalidDateRangeError
from app.domain.value_objects.date_range import DateRange


@pytest.mark.value_object
class TestDateRangeFactoryMethods:
    """Test all factory methods."""

    def test_create_with_only_start_date(self):
        """create() with no end date should produce an ongoing range."""
        start = datetime(2023, 1, 1)
        dr = DateRange.create(start_date=start)

        assert dr.start_date == start
        assert dr.end_date is None
        assert dr.is_ongoing() is True

    def test_create_with_start_and_end_date(self):
        """create() with both dates should produce a completed range."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 6, 1)
        dr = DateRange.create(start_date=start, end_date=end)

        assert dr.start_date == start
        assert dr.end_date == end
        assert dr.is_completed() is True

    def test_create_raises_when_end_before_start(self):
        """create() should raise InvalidDateRangeError when end <= start."""
        start = datetime(2023, 6, 1)
        end = datetime(2023, 1, 1)

        with pytest.raises(InvalidDateRangeError):
            DateRange.create(start_date=start, end_date=end)

    def test_ongoing_factory(self):
        """ongoing() should produce a range with no end date."""
        start = datetime(2022, 3, 15)
        dr = DateRange.ongoing(start)

        assert dr.is_ongoing() is True
        assert dr.end_date is None

    def test_completed_factory(self):
        """completed() should produce a range with both dates set."""
        start = datetime(2020, 1, 1)
        end = datetime(2021, 1, 1)
        dr = DateRange.completed(start, end)

        assert dr.is_completed() is True
        assert dr.end_date == end


@pytest.mark.value_object
class TestDateRangeDurationOngoing:
    """Test duration_days() for ongoing ranges."""

    def test_duration_days_returns_none_when_ongoing(self):
        """duration_days() should return None for ongoing ranges."""
        dr = DateRange.ongoing(datetime(2023, 1, 1))

        assert dr.duration_days() is None


@pytest.mark.value_object
class TestDateRangeContainsDate:
    """Test contains_date() method."""

    def test_date_within_completed_range(self):
        """Should return True for a date inside the range."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 12, 31)
        dr = DateRange.completed(start, end)

        assert dr.contains_date(datetime(2023, 6, 15)) is True

    def test_date_on_start_boundary(self):
        """Should return True for a date equal to start."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 12, 31)
        dr = DateRange.completed(start, end)

        assert dr.contains_date(start) is True

    def test_date_on_end_boundary(self):
        """Should return True for a date equal to end."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 12, 31)
        dr = DateRange.completed(start, end)

        assert dr.contains_date(end) is True

    def test_date_before_range(self):
        """Should return False for a date before start."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 12, 31)
        dr = DateRange.completed(start, end)

        assert dr.contains_date(datetime(2022, 12, 31)) is False

    def test_date_after_range(self):
        """Should return False for a date after end."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 12, 31)
        dr = DateRange.completed(start, end)

        assert dr.contains_date(datetime(2024, 1, 1)) is False

    def test_ongoing_range_contains_future_date(self):
        """Ongoing range should contain any date after start."""
        dr = DateRange.ongoing(datetime(2020, 1, 1))

        assert dr.contains_date(datetime(2030, 1, 1)) is True

    def test_ongoing_range_does_not_contain_past_date(self):
        """Ongoing range should not contain a date before start."""
        dr = DateRange.ongoing(datetime(2023, 1, 1))

        assert dr.contains_date(datetime(2022, 12, 31)) is False


@pytest.mark.value_object
class TestDateRangeOverlapsWith:
    """Test overlaps_with() method."""

    def test_two_overlapping_completed_ranges(self):
        """Should return True when ranges overlap."""
        dr1 = DateRange.completed(datetime(2023, 1, 1), datetime(2023, 6, 30))
        dr2 = DateRange.completed(datetime(2023, 3, 1), datetime(2023, 9, 30))

        assert dr1.overlaps_with(dr2) is True
        assert dr2.overlaps_with(dr1) is True

    def test_two_non_overlapping_completed_ranges(self):
        """Should return False when ranges do not overlap."""
        dr1 = DateRange.completed(datetime(2022, 1, 1), datetime(2022, 6, 30))
        dr2 = DateRange.completed(datetime(2023, 1, 1), datetime(2023, 6, 30))

        assert dr1.overlaps_with(dr2) is False
        assert dr2.overlaps_with(dr1) is False

    def test_ongoing_range_overlaps_with_later_range(self):
        """An ongoing range starting before another should overlap."""
        ongoing = DateRange.ongoing(datetime(2020, 1, 1))
        later = DateRange.completed(datetime(2023, 1, 1), datetime(2023, 12, 31))

        assert ongoing.overlaps_with(later) is True

    def test_completed_range_overlaps_with_ongoing(self):
        """A completed range should overlap with an ongoing range that starts before it."""
        completed = DateRange.completed(datetime(2023, 1, 1), datetime(2023, 12, 31))
        ongoing = DateRange.ongoing(datetime(2022, 6, 1))

        assert completed.overlaps_with(ongoing) is True

    def test_two_ongoing_ranges_always_overlap(self):
        """Two ongoing ranges always overlap."""
        dr1 = DateRange.ongoing(datetime(2020, 1, 1))
        dr2 = DateRange.ongoing(datetime(2021, 1, 1))

        assert dr1.overlaps_with(dr2) is True

    def test_adjacent_ranges_do_not_overlap(self):
        """Adjacent ranges (end == next start) should not overlap per strict comparison."""
        dr1 = DateRange.completed(datetime(2022, 1, 1), datetime(2022, 12, 31))
        dr2 = DateRange.completed(datetime(2023, 1, 1), datetime(2023, 12, 31))

        # 2022-12-31 < 2023-01-01, so they should not overlap
        assert dr1.overlaps_with(dr2) is False


@pytest.mark.value_object
class TestDateRangeWithEndDate:
    """Test with_end_date() method."""

    def test_creates_new_range_with_end_date(self):
        """with_end_date() should return a new DateRange with the given end date."""
        start = datetime(2023, 1, 1)
        dr = DateRange.ongoing(start)

        new_end = datetime(2023, 12, 31)
        completed_dr = dr.with_end_date(new_end)

        assert completed_dr.start_date == start
        assert completed_dr.end_date == new_end
        assert completed_dr.is_completed() is True

    def test_original_range_unchanged(self):
        """Original range should remain unchanged after with_end_date()."""
        dr = DateRange.ongoing(datetime(2023, 1, 1))
        _ = dr.with_end_date(datetime(2023, 12, 31))

        assert dr.is_ongoing() is True


@pytest.mark.value_object
class TestDateRangeIsCompleted:
    """Test is_completed() method."""

    def test_is_completed_true_with_end_date(self):
        """is_completed() returns True for a range with end date."""
        dr = DateRange.completed(datetime(2022, 1, 1), datetime(2023, 1, 1))
        assert dr.is_completed() is True

    def test_is_completed_false_when_ongoing(self):
        """is_completed() returns False for an ongoing range."""
        dr = DateRange.ongoing(datetime(2022, 1, 1))
        assert dr.is_completed() is False


@pytest.mark.value_object
class TestDateRangeStringRepresentations:
    """Test __str__ and __repr__ methods."""

    def test_str_ongoing_range(self):
        """__str__ for ongoing range should end with 'Present'."""
        dr = DateRange.ongoing(datetime(2023, 1, 15))

        result = str(dr)

        assert result.endswith("Present")
        assert "2023-01-15" in result

    def test_str_completed_range(self):
        """__str__ for completed range should show both dates."""
        dr = DateRange.completed(datetime(2022, 3, 1), datetime(2023, 9, 30))

        result = str(dr)

        assert "2022-03-01" in result
        assert "2023-09-30" in result

    def test_repr(self):
        """__repr__ should include start and end date."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 12, 31)
        dr = DateRange.completed(start, end)

        result = repr(dr)

        assert "DateRange" in result
        assert "start_date" in result
        assert "end_date" in result


@pytest.mark.value_object
@pytest.mark.business_rule
class TestDateRangeValidationEdgeCases:
    """Test validation edge cases."""

    def test_equal_start_and_end_raises_error(self):
        """end_date equal to start_date should raise InvalidDateRangeError."""
        same = datetime(2023, 6, 1)

        with pytest.raises(InvalidDateRangeError):
            DateRange(start_date=same, end_date=same)

    def test_none_start_date_raises_empty_field_error(self):
        """None start_date should raise EmptyFieldError."""

        with pytest.raises(EmptyFieldError):
            DateRange(start_date=None)  # type: ignore[arg-type]
