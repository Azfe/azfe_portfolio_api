"""
Extended tests for WorkExperience Entity.

Covers uncovered lines: empty string normalization for description/location,
add_responsibility(), update_responsibilities(), update_technologies(), update_order(),
is_current_position(), location too long, and __repr__.
"""

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

START = datetime(2022, 1, 1)
END = datetime(2023, 6, 30)


def _make_experience(profile_id, **kwargs):
    defaults = {
        "profile_id": profile_id,
        "role": "Backend Developer",
        "company": "Tech Corp",
        "start_date": START,
        "order_index": 0,
    }
    defaults.update(kwargs)
    return WorkExperience.create(**defaults)


@pytest.mark.entity
class TestWorkExperienceEmptyStringNormalization:
    """Test that optional fields with empty strings normalize to None."""

    def test_empty_description_normalized_to_none(self, profile_id):
        """Empty description should be stored as None."""
        exp = _make_experience(profile_id, description="")

        assert exp.description is None

    def test_whitespace_description_normalized_to_none(self, profile_id):
        """Whitespace-only description should be stored as None."""
        exp = _make_experience(profile_id, description="   ")

        assert exp.description is None


@pytest.mark.entity
@pytest.mark.business_rule
class TestWorkExperienceValidation:
    """Test validation rules for WorkExperience."""

    def test_empty_role_raises_error(self, profile_id):
        """Empty role should raise InvalidRoleError."""
        with pytest.raises(InvalidRoleError):
            _make_experience(profile_id, role="")

    def test_role_too_long_raises_error(self, profile_id):
        """Role > 100 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_experience(profile_id, role="x" * 101)

    def test_empty_company_raises_error(self, profile_id):
        """Empty company should raise InvalidCompanyError."""
        with pytest.raises(InvalidCompanyError):
            _make_experience(profile_id, company="")

    def test_company_too_long_raises_error(self, profile_id):
        """Company > 100 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_experience(profile_id, company="x" * 101)

    def test_description_too_long_raises_error(self, profile_id):
        """Description > 2000 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_experience(profile_id, description="x" * 2001)

    def test_location_too_long_raises_error(self, profile_id):
        """Location > 100 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_experience(profile_id, location="x" * 101)

    def test_end_date_before_start_raises_error(self, profile_id):
        """end_date before start_date should raise InvalidDateRangeError."""
        with pytest.raises(InvalidDateRangeError):
            _make_experience(
                profile_id,
                start_date=datetime(2023, 1, 1),
                end_date=datetime(2022, 1, 1),
            )

    def test_negative_order_index_raises_error(self, profile_id):
        """Negative order_index should raise InvalidOrderIndexError."""
        with pytest.raises(InvalidOrderIndexError):
            _make_experience(profile_id, order_index=-1)

    def test_too_many_responsibilities_raises_error(self, profile_id):
        """More than 20 responsibilities should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_experience(
                profile_id,
                responsibilities=[f"Task {i}" for i in range(21)],
            )

    def test_empty_responsibility_item_raises_error(self, profile_id):
        """Empty string in responsibilities should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            _make_experience(profile_id, responsibilities=["valid task", ""])

    def test_responsibility_item_too_long_raises_error(self, profile_id):
        """Responsibility item > 500 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_experience(profile_id, responsibilities=["x" * 501])

    def test_too_many_technologies_raises_error(self, profile_id):
        """More than 20 technologies should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_experience(
                profile_id,
                technologies=[f"Tech{i}" for i in range(21)],
            )

    def test_empty_technology_item_raises_error(self, profile_id):
        """Empty string in technologies list should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            _make_experience(profile_id, technologies=["Python", ""])

    def test_technology_item_too_long_raises_error(self, profile_id):
        """Technology item > 150 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            _make_experience(profile_id, technologies=["x" * 151])


@pytest.mark.entity
class TestWorkExperienceIsCurrentPosition:
    """Test is_current_position() method."""

    def test_is_current_when_no_end_date(self, profile_id):
        """Should return True when no end_date is set."""
        exp = _make_experience(profile_id)

        assert exp.is_current_position() is True

    def test_is_not_current_when_end_date_set(self, profile_id):
        """Should return False when end_date is set."""
        exp = _make_experience(profile_id, end_date=END)

        assert exp.is_current_position() is False


@pytest.mark.entity
class TestWorkExperienceUpdateInfo:
    """Test update_info() method extended scenarios."""

    def test_update_role(self, profile_id):
        """Should update role field."""
        exp = _make_experience(profile_id)
        exp.update_info(role="Senior Backend Developer")

        assert exp.role == "Senior Backend Developer"

    def test_update_company(self, profile_id):
        """Should update company field."""
        exp = _make_experience(profile_id)
        exp.update_info(company="New Company")

        assert exp.company == "New Company"

    def test_update_description(self, profile_id):
        """Should update description."""
        exp = _make_experience(profile_id)
        exp.update_info(description="New description for the role")

        assert exp.description == "New description for the role"

    def test_update_location(self, profile_id):
        """Should update location."""
        exp = _make_experience(profile_id)
        exp.update_info(location="Barcelona, Spain")

        assert exp.location == "Barcelona, Spain"

    def test_update_start_date(self, profile_id):
        """Should update start_date."""
        exp = _make_experience(profile_id)
        new_start = datetime(2021, 6, 1)
        exp.update_info(start_date=new_start)

        assert exp.start_date == new_start

    def test_update_end_date(self, profile_id):
        """Should update end_date."""
        exp = _make_experience(profile_id)
        exp.update_info(end_date=END)

        assert exp.end_date == END

    def test_update_info_invalid_dates_raises(self, profile_id):
        """Setting end_date before start_date should raise error."""
        exp = _make_experience(profile_id, start_date=datetime(2023, 1, 1))

        with pytest.raises(InvalidDateRangeError):
            exp.update_info(end_date=datetime(2022, 1, 1))

    def test_update_info_invalid_role_raises(self, profile_id):
        """Empty role should raise InvalidRoleError."""
        exp = _make_experience(profile_id)

        with pytest.raises(InvalidRoleError):
            exp.update_info(role="")

    def test_update_info_invalid_company_raises(self, profile_id):
        """Empty company should raise error."""
        exp = _make_experience(profile_id)

        with pytest.raises(InvalidCompanyError):
            exp.update_info(company="")

    def test_update_info_invalid_description_raises(self, profile_id):
        """Too-long description should raise error."""
        exp = _make_experience(profile_id)

        with pytest.raises(InvalidLengthError):
            exp.update_info(description="x" * 2001)

    def test_update_info_invalid_location_raises(self, profile_id):
        """Too-long location should raise error."""
        exp = _make_experience(profile_id)

        with pytest.raises(InvalidLengthError):
            exp.update_info(location="x" * 101)


@pytest.mark.entity
class TestWorkExperienceAddResponsibility:
    """Test add_responsibility() method."""

    def test_add_responsibility(self, profile_id):
        """Should add a responsibility to the list."""
        exp = _make_experience(profile_id)
        exp.add_responsibility("Design system architecture")

        assert "Design system architecture" in exp.responsibilities

    def test_add_empty_responsibility_raises(self, profile_id):
        """Empty responsibility should raise EmptyFieldError."""
        exp = _make_experience(profile_id)

        with pytest.raises(EmptyFieldError):
            exp.add_responsibility("")

    def test_add_too_long_responsibility_raises(self, profile_id):
        """Responsibility > 500 chars should raise InvalidLengthError."""
        exp = _make_experience(profile_id)

        with pytest.raises(InvalidLengthError):
            exp.add_responsibility("x" * 501)

    def test_add_responsibility_when_full_raises(self, profile_id):
        """Adding more than 20 responsibilities should raise InvalidLengthError."""
        exp = _make_experience(
            profile_id,
            responsibilities=[f"Task {i}" for i in range(20)],
        )

        with pytest.raises(InvalidLengthError):
            exp.add_responsibility("One more task")


@pytest.mark.entity
class TestWorkExperienceUpdateResponsibilities:
    """Test update_responsibilities() method."""

    def test_update_responsibilities(self, profile_id):
        """Should replace the responsibilities list."""
        exp = _make_experience(profile_id, responsibilities=["Old task"])
        exp.update_responsibilities(["New task 1", "New task 2"])

        assert exp.responsibilities == ["New task 1", "New task 2"]

    def test_update_responsibilities_empty_list(self, profile_id):
        """Should accept empty list."""
        exp = _make_experience(profile_id, responsibilities=["Some task"])
        exp.update_responsibilities([])

        assert exp.responsibilities == []

    def test_update_responsibilities_invalid_raises(self, profile_id):
        """Invalid items should raise error."""
        exp = _make_experience(profile_id)

        with pytest.raises(EmptyFieldError):
            exp.update_responsibilities(["valid", ""])


@pytest.mark.entity
class TestWorkExperienceUpdateTechnologies:
    """Test update_technologies() method."""

    def test_update_technologies(self, profile_id):
        """Should replace the technologies list."""
        exp = _make_experience(profile_id, technologies=["Python"])
        exp.update_technologies(["FastAPI", "MongoDB", "Docker"])

        assert exp.technologies == ["FastAPI", "MongoDB", "Docker"]

    def test_update_technologies_invalid_raises(self, profile_id):
        """More than 20 items should raise error."""
        exp = _make_experience(profile_id)

        with pytest.raises(InvalidLengthError):
            exp.update_technologies([f"Tech{i}" for i in range(21)])


@pytest.mark.entity
class TestWorkExperienceUpdateOrder:
    """Test update_order() method."""

    def test_update_order(self, profile_id):
        """Should update order_index."""
        exp = _make_experience(profile_id, order_index=0)
        exp.update_order(3)

        assert exp.order_index == 3

    def test_update_order_negative_raises(self, profile_id):
        """Negative order_index should raise InvalidOrderIndexError."""
        exp = _make_experience(profile_id)

        with pytest.raises(InvalidOrderIndexError):
            exp.update_order(-1)


@pytest.mark.entity
class TestWorkExperienceRepr:
    """Test __repr__ method."""

    def test_repr_contains_role_and_company(self, profile_id):
        """__repr__ should include role and company."""
        exp = _make_experience(profile_id)

        result = repr(exp)

        assert "WorkExperience" in result
        assert "Backend Developer" in result
        assert "Tech Corp" in result
