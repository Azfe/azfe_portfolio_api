"""Tests for base DTOs."""

from datetime import datetime

from app.application.dto.base_dto import (
    DateRangeDTO,
    ErrorResponse,
    PaginationRequest,
    SuccessResponse,
)


class TestSuccessResponse:
    def test_defaults(self):
        resp = SuccessResponse()
        assert resp.success is True
        assert resp.message == "Operation completed successfully"

    def test_custom_message(self):
        resp = SuccessResponse(message="Done")
        assert resp.message == "Done"


class TestErrorResponse:
    def test_creation(self):
        resp = ErrorResponse(message="Something failed")
        assert resp.success is False
        assert resp.message == "Something failed"
        assert resp.errors == []

    def test_with_errors_list(self):
        resp = ErrorResponse(message="Validation", errors=["field required"])
        assert resp.errors == ["field required"]


class TestPaginationRequest:
    def test_defaults(self):
        req = PaginationRequest()
        assert req.skip == 0
        assert req.limit == 100
        assert req.sort_by is None
        assert req.ascending is True

    def test_negative_skip_clamped_to_zero(self):
        req = PaginationRequest(skip=-5)
        assert req.skip == 0

    def test_zero_limit_clamped_to_one(self):
        req = PaginationRequest(limit=0)
        assert req.limit == 1

    def test_negative_limit_clamped_to_one(self):
        req = PaginationRequest(limit=-10)
        assert req.limit == 1

    def test_limit_over_1000_clamped(self):
        req = PaginationRequest(limit=5000)
        assert req.limit == 1000

    def test_limit_at_boundary_1000(self):
        req = PaginationRequest(limit=1000)
        assert req.limit == 1000

    def test_limit_at_boundary_1(self):
        req = PaginationRequest(limit=1)
        assert req.limit == 1

    def test_custom_sort(self):
        req = PaginationRequest(sort_by="name", ascending=False)
        assert req.sort_by == "name"
        assert req.ascending is False


class TestDateRangeDTO:
    def test_with_end_date(self):
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        dto = DateRangeDTO(start_date=start, end_date=end)
        assert dto.start_date == start
        assert dto.end_date == end

    def test_without_end_date(self):
        start = datetime(2024, 1, 1)
        dto = DateRangeDTO(start_date=start)
        assert dto.end_date is None
