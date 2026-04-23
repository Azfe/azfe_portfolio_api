"""Tests for WorkExperience Entity."""

from datetime import datetime

import pytest

from app.domain.entities.work_experience import WorkExperience
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidCompanyError,
    InvalidDateRangeError,
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidRoleError,
)


@pytest.mark.entity
class TestWorkExperienceCreation:
    """Test WorkExperience creation."""

    def test_create_with_required_fields(self, profile_id):
        we = WorkExperience.create(
            profile_id=profile_id,
            role="Backend Developer",
            company="Acme Corp",
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert we.role == "Backend Developer"
        assert we.company == "Acme Corp"
        assert we.order_index == 0
        assert we.end_date is None
        assert we.responsibilities == []
        assert we.description is None

    def test_create_with_all_fields(self, profile_id):
        we = WorkExperience.create(
            profile_id=profile_id,
            role="Senior Dev",
            company="Tech Inc",
            start_date=datetime(2022, 1, 1),
            order_index=1,
            description="Led backend team",
            end_date=datetime(2023, 6, 1),
            responsibilities=["Code review", "Architecture"],
        )
        assert we.description == "Led backend team"
        assert we.end_date == datetime(2023, 6, 1)
        assert len(we.responsibilities) == 2

    def test_create_generates_uuid(self, profile_id):
        we = WorkExperience.create(
            profile_id=profile_id,
            role="Dev",
            company="Co",
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert we.id is not None
        assert len(we.id) > 0


@pytest.mark.entity
@pytest.mark.business_rule
class TestWorkExperienceValidation:
    """Test WorkExperience validation rules."""

    def test_empty_role_raises_error(self, profile_id):
        with pytest.raises(InvalidRoleError):
            WorkExperience.create(
                profile_id=profile_id,
                role="",
                company="Acme",
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_role_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            WorkExperience.create(
                profile_id=profile_id,
                role="x" * 101,
                company="Acme",
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_empty_company_raises_error(self, profile_id):
        with pytest.raises(InvalidCompanyError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Dev",
                company="",
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_company_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Dev",
                company="x" * 101,
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_end_date_before_start_date_raises_error(self, profile_id):
        with pytest.raises(InvalidDateRangeError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Dev",
                company="Acme",
                start_date=datetime(2023, 6, 1),
                order_index=0,
                end_date=datetime(2023, 1, 1),
            )

    def test_negative_order_index_raises_error(self, profile_id):
        with pytest.raises(InvalidOrderIndexError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Dev",
                company="Acme",
                start_date=datetime(2023, 1, 1),
                order_index=-1,
            )

    def test_description_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Dev",
                company="Acme",
                start_date=datetime(2023, 1, 1),
                order_index=0,
                description="x" * 2001,
            )

    def test_empty_description_becomes_none(self, profile_id):
        we = WorkExperience.create(
            profile_id=profile_id,
            role="Dev",
            company="Acme",
            start_date=datetime(2023, 1, 1),
            order_index=0,
            description="   ",
        )
        assert we.description is None

    def test_too_many_responsibilities_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Dev",
                company="Acme",
                start_date=datetime(2023, 1, 1),
                order_index=0,
                responsibilities=[f"Task {i}" for i in range(21)],
            )

    def test_empty_responsibility_item_raises_error(self, profile_id):
        with pytest.raises(EmptyFieldError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Dev",
                company="Acme",
                start_date=datetime(2023, 1, 1),
                order_index=0,
                responsibilities=["Valid", ""],
            )

    def test_responsibility_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Dev",
                company="Acme",
                start_date=datetime(2023, 1, 1),
                order_index=0,
                responsibilities=["x" * 501],
            )

    def test_empty_profile_id_raises_error(self):
        with pytest.raises(EmptyFieldError):
            WorkExperience.create(
                profile_id="",
                role="Dev",
                company="Acme",
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )


@pytest.mark.entity
class TestWorkExperienceUpdate:
    """Test WorkExperience updates."""

    def _make(self, profile_id):
        return WorkExperience.create(
            profile_id=profile_id,
            role="Dev",
            company="Acme",
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )

    def test_update_info(self, profile_id):
        we = self._make(profile_id)
        we.update_info(role="Senior Dev", company="New Corp")
        assert we.role == "Senior Dev"
        assert we.company == "New Corp"

    def test_update_info_invalid_role_raises(self, profile_id):
        we = self._make(profile_id)
        with pytest.raises(InvalidRoleError):
            we.update_info(role="")

    def test_add_responsibility(self, profile_id):
        we = self._make(profile_id)
        we.add_responsibility("Code review")
        assert "Code review" in we.responsibilities

    def test_add_empty_responsibility_raises(self, profile_id):
        we = self._make(profile_id)
        with pytest.raises(EmptyFieldError):
            we.add_responsibility("")

    def test_add_responsibility_over_max_raises(self, profile_id):
        we = WorkExperience.create(
            profile_id=profile_id,
            role="Dev",
            company="Acme",
            start_date=datetime(2023, 1, 1),
            order_index=0,
            responsibilities=[f"Task {i}" for i in range(20)],
        )
        with pytest.raises(InvalidLengthError):
            we.add_responsibility("One more")

    def test_update_responsibilities(self, profile_id):
        we = self._make(profile_id)
        we.update_responsibilities(["Task A", "Task B"])
        assert we.responsibilities == ["Task A", "Task B"]

    def test_update_order(self, profile_id):
        we = self._make(profile_id)
        we.update_order(5)
        assert we.order_index == 5

    def test_update_order_negative_raises(self, profile_id):
        we = self._make(profile_id)
        with pytest.raises(InvalidOrderIndexError):
            we.update_order(-1)


@pytest.mark.entity
class TestWorkExperienceBusinessMethods:
    """Test WorkExperience business methods."""

    def test_is_current_position_no_end_date(self, profile_id):
        we = WorkExperience.create(
            profile_id=profile_id,
            role="Dev",
            company="Acme",
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert we.is_current_position() is True

    def test_is_not_current_position_with_end_date(self, profile_id):
        we = WorkExperience.create(
            profile_id=profile_id,
            role="Dev",
            company="Acme",
            start_date=datetime(2022, 1, 1),
            order_index=0,
            end_date=datetime(2023, 1, 1),
        )
        assert we.is_current_position() is False
