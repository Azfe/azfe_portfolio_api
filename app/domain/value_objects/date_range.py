"""
DateRange Value Object.

Represents an immutable period with start and optional end dates.
Used for work experiences, education, projects, etc.

Value Object Principles:
- Immutability: Cannot be changed after creation
- Self-validation: Validates on construction
- Equality by value: Two DateRanges are equal if dates match
"""

from dataclasses import dataclass
from datetime import datetime

from ..exceptions import EmptyFieldError, InvalidDateRangeError


@dataclass(frozen=True)
class DateRange:
    """
    DateRange Value Object representing a time period.

    Attributes:
        start_date: When the period starts (required)
        end_date: When the period ends (None if ongoing)

    Business Rules:
        - start_date is required
        - end_date must be after start_date if provided
        - Immutable after creation
    """

    start_date: datetime
    end_date: datetime | None = None

    def __post_init__(self):
        """Validate invariants after initialization."""
        self._validate()

    @staticmethod
    def create(start_date: datetime, end_date: datetime | None = None) -> "DateRange":
        """
        Factory method to create a DateRange.

        Args:
            start_date: Start of the period
            end_date: End of the period (None if ongoing)

        Returns:
            A new DateRange instance

        Raises:
            EmptyFieldError: If start_date is None
            InvalidDateRangeError: If end_date is before start_date
        """
        return DateRange(start_date=start_date, end_date=end_date)

    @staticmethod
    def ongoing(start_date: datetime) -> "DateRange":
        """
        Create an ongoing DateRange (no end date).

        Args:
            start_date: Start of the period

        Returns:
            A DateRange with no end date
        """
        return DateRange(start_date=start_date, end_date=None)

    @staticmethod
    def completed(start_date: datetime, end_date: datetime) -> "DateRange":
        """
        Create a completed DateRange (with end date).

        Args:
            start_date: Start of the period
            end_date: End of the period

        Returns:
            A DateRange with both start and end
        """
        return DateRange(start_date=start_date, end_date=end_date)

    def is_ongoing(self) -> bool:
        """Check if this is an ongoing period (no end date)."""
        return self.end_date is None

    def is_completed(self) -> bool:
        """Check if this period has ended."""
        return self.end_date is not None

    def duration_days(self) -> int | None:
        """
        Calculate duration in days.

        Returns:
            Number of days if completed, None if ongoing
        """
        if self.is_ongoing():
            return None
        # Type assertion: end_date is not None after is_ongoing() check
        assert self.end_date is not None
        return (self.end_date - self.start_date).days

    def contains_date(self, date: datetime) -> bool:
        """
        Check if a given date falls within this range.

        Args:
            date: Date to check

        Returns:
            True if date is within range
        """
        return date >= self.start_date and (
            self.end_date is None or date <= self.end_date
        )

    def overlaps_with(self, other: "DateRange") -> bool:
        """
        Check if this DateRange overlaps with another.

        Args:
            other: Another DateRange

        Returns:
            True if ranges overlap
        """
        # If either range is ongoing, check if start dates overlap
        if self.is_ongoing() or other.is_ongoing():
            return self.start_date <= (
                other.end_date or datetime.max
            ) and other.start_date <= (self.end_date or datetime.max)

        # Both ranges have end dates - add type assertions for MyPy
        assert self.end_date is not None
        assert other.end_date is not None
        return self.start_date <= other.end_date and other.start_date <= self.end_date

    def with_end_date(self, end_date: datetime) -> "DateRange":
        """
        Create a new DateRange with a different end date.

        Args:
            end_date: New end date

        Returns:
            A new DateRange instance
        """
        return DateRange(start_date=self.start_date, end_date=end_date)

    def _validate(self) -> None:
        """Validate the date range invariants."""
        if self.start_date is None:
            raise EmptyFieldError("start_date")

        if self.end_date is not None and self.end_date <= self.start_date:
            raise InvalidDateRangeError(str(self.start_date), str(self.end_date))

    def __str__(self) -> str:
        """String representation for display."""
        if self.is_ongoing():
            return f"{self.start_date.strftime('%Y-%m-%d')} - Present"
        # Type assertion: end_date is not None after is_ongoing() check
        assert self.end_date is not None
        return f"{self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')}"

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"DateRange(start_date={self.start_date}, end_date={self.end_date})"
