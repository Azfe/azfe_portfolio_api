"""Tests for WorkExperience DTOs."""

from datetime import datetime

import pytest

from app.application.dto.work_experience_dto import (
    WorkExperienceListResponse,
    WorkExperienceResponse,
)

from .conftest import DT, DT2, DT_END, DT_START, make_entity


def _make_experience_entity(**overrides):
    defaults = {
        "id": "w-1",
        "profile_id": "p-1",
        "role": "Developer",
        "company": "Acme",
        "start_date": DT_START,
        "end_date": DT_END,
        "description": "Full-stack dev",
        "location": None,
        "responsibilities": ["Code", "Review"],
        "order_index": 0,
    }
    defaults.update(overrides)
    entity = make_entity(**defaults)
    entity.is_current_position.return_value = overrides.get("_is_current", False)
    return entity


class TestWorkExperienceResponseFromEntity:
    def test_maps_all_fields(self):
        entity = _make_experience_entity()
        resp = WorkExperienceResponse.from_entity(entity)

        assert resp.id == "w-1"
        assert resp.role == "Developer"
        assert resp.company == "Acme"
        assert resp.start_date == DT_START
        assert resp.end_date == DT_END
        assert resp.description == "Full-stack dev"
        assert resp.order_index == 0
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    def test_responsibilities_are_copied(self):
        original = ["Code", "Review"]
        entity = _make_experience_entity(responsibilities=original)
        resp = WorkExperienceResponse.from_entity(entity)

        assert resp.responsibilities == ["Code", "Review"]
        assert resp.responsibilities is not original

    def test_is_current_from_entity_method(self):
        entity = _make_experience_entity(_is_current=True)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.is_current is True

    def test_is_not_current(self):
        entity = _make_experience_entity(_is_current=False)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.is_current is False

    def test_none_optional_fields(self):
        entity = _make_experience_entity(end_date=None, description=None, location=None)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.end_date is None
        assert resp.description is None
        assert resp.location is None

    def test_location_is_mapped(self):
        entity = _make_experience_entity(location="Madrid, Spain")
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.location == "Madrid, Spain"

    def test_location_none_by_default(self):
        entity = _make_experience_entity()
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.location is None

    def test_empty_responsibilities(self):
        entity = _make_experience_entity(responsibilities=[])
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.responsibilities == []


class TestWorkExperienceResponseDurationMonths:
    """Tests for duration_months calculation in WorkExperienceResponse.from_entity()."""

    def test_closed_position_exact_months(self):
        """Closed position with a fixed date range returns exact month count."""
        start = datetime(2023, 1, 1)
        end = datetime(2023, 7, 1)  # 6 months
        entity = _make_experience_entity(start_date=start, end_date=end)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.duration_months == 6

    def test_closed_position_exactly_one_month(self):
        """Closed position spanning exactly one calendar month."""
        start = datetime(2023, 3, 1)
        end = datetime(2023, 4, 1)  # 1 month
        entity = _make_experience_entity(start_date=start, end_date=end)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.duration_months == 1

    def test_closed_position_exactly_twelve_months(self):
        """Closed position spanning exactly 12 months (one year)."""
        start = datetime(2022, 1, 1)
        end = datetime(2023, 1, 1)  # 12 months
        entity = _make_experience_entity(start_date=start, end_date=end)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.duration_months == 12

    @pytest.mark.unit
    def test_current_position_duration_greater_than_zero(self):
        """Active position (end_date=None) computes duration up to today, which is > 0."""
        # A start date far in the past guarantees duration > 0 regardless of test date.
        start = datetime(2020, 1, 1)
        entity = _make_experience_entity(
            start_date=start, end_date=None, _is_current=True
        )
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.duration_months > 0

    @pytest.mark.unit
    def test_current_position_duration_reflects_months_to_now(self):
        """Active position duration equals months from start_date to the current month."""
        start = datetime(2020, 6, 1)
        entity = _make_experience_entity(
            start_date=start, end_date=None, _is_current=True
        )
        resp = WorkExperienceResponse.from_entity(entity)

        now = datetime.utcnow()
        expected = (now.year - start.year) * 12 + (now.month - start.month)
        assert resp.duration_months == expected

    @pytest.mark.unit
    def test_is_current_true_when_no_end_date(self):
        """is_current is True when end_date is None."""
        entity = _make_experience_entity(end_date=None, _is_current=True)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.is_current is True

    @pytest.mark.unit
    def test_is_current_false_when_has_end_date(self):
        """is_current is False when end_date is set."""
        entity = _make_experience_entity(end_date=DT_END, _is_current=False)
        resp = WorkExperienceResponse.from_entity(entity)
        assert resp.is_current is False


class TestWorkExperienceListResponseFromEntities:
    def test_maps_list(self):
        entities = [
            _make_experience_entity(id="w-1"),
            _make_experience_entity(id="w-2", role="Lead"),
        ]
        resp = WorkExperienceListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.experiences) == 2

    def test_empty_list(self):
        resp = WorkExperienceListResponse.from_entities([])
        assert resp.total == 0
        assert resp.experiences == []
