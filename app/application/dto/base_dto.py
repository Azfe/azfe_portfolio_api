"""
Base DTOs Module.

Data Transfer Objects for transferring data between layers.
These are simple data containers without business logic.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SuccessResponse:
    """Generic success response."""

    success: bool = True
    message: str = "Operation completed successfully"


@dataclass
class ErrorResponse:
    """Generic error response."""

    message: str
    success: bool = False
    errors: list[str] = field(default_factory=list)


@dataclass
class PaginationRequest:
    """Pagination parameters for list queries."""

    skip: int = 0
    limit: int = 100
    sort_by: str | None = None
    ascending: bool = True

    def __post_init__(self):
        if self.skip < 0:
            self.skip = 0
        if self.limit < 1:
            self.limit = 1
        if self.limit > 1000:
            self.limit = 1000


@dataclass
class DateRangeDTO:
    """DTO for date ranges."""

    start_date: datetime
    end_date: datetime | None = None
