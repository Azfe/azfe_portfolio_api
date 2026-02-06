"""
Unit tests for Education Entity.

Tests cover:
- Entity creation with factory method
- Field validation (required and optional)
- Date range validation
- Update operations
- Business rules enforcement
- Temporal coherence
"""

import uuid
from datetime import datetime

import pytest

from app.domain.entities.education import Education
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidDateRangeError,
    InvalidInstitutionError,
    InvalidLengthError,
    InvalidOrderIndexError,
)

# ==========================================
# VALID EDUCATION CREATION TESTS
# ==========================================


class TestEducationCreation:
    """Tests for valid Education entity creation."""

    def test_create_with_all_required_fields(self, profile_id, today):
        """Should create Education with all required fields."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        assert education.id is not None
        assert education.profile_id == profile_id
        assert education.institution == "Universidad Complutense de Madrid"
        assert education.degree == "Bachelor of Science"
        assert education.field == "Computer Science"
        assert education.start_date == today
        assert education.order_index == 0
        assert education.description is None
        assert education.end_date is None
        assert education.created_at is not None
        assert education.updated_at is not None

    def test_create_with_optional_fields(self, profile_id, today, yesterday):
        """Should create Education with all optional fields."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=yesterday,
            end_date=today,
            order_index=0,
            description="Focused on software engineering and algorithms",
        )

        assert education.description == "Focused on software engineering and algorithms"
        assert education.end_date == today

    def test_create_generates_unique_id(self, profile_id, today):
        """Should generate unique UUID for each education."""
        education1 = Education.create(
            profile_id=profile_id,
            institution="Institution 1",
            degree="Degree 1",
            field="Field 1",
            start_date=today,
            order_index=0,
        )
        education2 = Education.create(
            profile_id=profile_id,
            institution="Institution 2",
            degree="Degree 2",
            field="Field 2",
            start_date=today,
            order_index=1,
        )

        assert education1.id != education2.id
        # Verify they are valid UUIDs
        uuid.UUID(education1.id)
        uuid.UUID(education2.id)

    def test_create_sets_timestamps(self, profile_id, today):
        """Should set created_at and updated_at timestamps."""
        before = datetime.utcnow()
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )
        after = datetime.utcnow()

        assert before <= education.created_at <= after
        assert before <= education.updated_at <= after

    def test_create_with_order_index_zero(self, profile_id, today):
        """Should accept order_index of 0 (first position)."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        assert education.order_index == 0


# ==========================================
# FIELD VALIDATION TESTS
# ==========================================


class TestEducationFieldValidation:
    """Tests for Education field validation."""

    def test_empty_profile_id_raises_error(self, today):
        """Should raise EmptyFieldError for empty profile_id."""
        with pytest.raises(EmptyFieldError) as exc_info:
            Education.create(
                profile_id="",
                institution="Universidad Complutense de Madrid",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

        assert "profile_id" in str(exc_info.value)

    def test_whitespace_profile_id_raises_error(self, today):
        """Should raise EmptyFieldError for whitespace-only profile_id."""
        with pytest.raises(EmptyFieldError):
            Education.create(
                profile_id="   ",
                institution="Universidad Complutense de Madrid",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

    def test_empty_institution_raises_error(self, profile_id, today):
        """Should raise InvalidInstitutionError for empty institution."""
        with pytest.raises(InvalidInstitutionError):
            Education.create(
                profile_id=profile_id,
                institution="",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

    def test_whitespace_institution_raises_error(self, profile_id, today):
        """Should raise InvalidInstitutionError for whitespace-only institution."""
        with pytest.raises(InvalidInstitutionError):
            Education.create(
                profile_id=profile_id,
                institution="   ",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

    def test_too_long_institution_raises_error(self, profile_id, today):
        """Should raise InvalidLengthError for institution exceeding max length."""
        long_institution = "A" * 101

        with pytest.raises(InvalidLengthError) as exc_info:
            Education.create(
                profile_id=profile_id,
                institution=long_institution,
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

        assert "institution" in str(exc_info.value)

    def test_max_length_institution_is_valid(self, profile_id, today):
        """Should accept institution at exact max length."""
        max_institution = "A" * 100

        education = Education.create(
            profile_id=profile_id,
            institution=max_institution,
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        assert education.institution == max_institution

    def test_empty_degree_raises_error(self, profile_id, today):
        """Should raise EmptyFieldError for empty degree."""
        with pytest.raises(EmptyFieldError) as exc_info:
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense de Madrid",
                degree="",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

        assert "degree" in str(exc_info.value)

    def test_too_long_degree_raises_error(self, profile_id, today):
        """Should raise InvalidLengthError for degree exceeding max length."""
        long_degree = "A" * 101

        with pytest.raises(InvalidLengthError) as exc_info:
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense de Madrid",
                degree=long_degree,
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

        assert "degree" in str(exc_info.value)

    def test_max_length_degree_is_valid(self, profile_id, today):
        """Should accept degree at exact max length."""
        max_degree = "A" * 100

        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree=max_degree,
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        assert education.degree == max_degree

    def test_empty_field_raises_error(self, profile_id, today):
        """Should raise EmptyFieldError for empty field."""
        with pytest.raises(EmptyFieldError) as exc_info:
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense de Madrid",
                degree="Bachelor of Science",
                field="",
                start_date=today,
                order_index=0,
            )

        assert "field" in str(exc_info.value)

    def test_too_long_field_raises_error(self, profile_id, today):
        """Should raise InvalidLengthError for field exceeding max length."""
        long_field = "A" * 101

        with pytest.raises(InvalidLengthError) as exc_info:
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense de Madrid",
                degree="Bachelor of Science",
                field=long_field,
                start_date=today,
                order_index=0,
            )

        assert "field" in str(exc_info.value)

    def test_max_length_field_is_valid(self, profile_id, today):
        """Should accept field at exact max length."""
        max_field = "A" * 100

        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field=max_field,
            start_date=today,
            order_index=0,
        )

        assert education.field == max_field

    def test_too_long_description_raises_error(self, profile_id, today):
        """Should raise InvalidLengthError for description exceeding max length."""
        long_description = "A" * 1001

        with pytest.raises(InvalidLengthError) as exc_info:
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense de Madrid",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=0,
                description=long_description,
            )

        assert "description" in str(exc_info.value)

    def test_max_length_description_is_valid(self, profile_id, today):
        """Should accept description at exact max length."""
        max_description = "A" * 1000

        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
            description=max_description,
        )

        assert education.description == max_description

    def test_whitespace_description_becomes_none(self, profile_id, today):
        """Should convert whitespace-only description to None."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
            description="   ",
        )

        assert education.description is None

    def test_negative_order_index_raises_error(self, profile_id, today):
        """Should raise InvalidOrderIndexError for negative order_index."""
        with pytest.raises(InvalidOrderIndexError):
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense de Madrid",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=-1,
            )


# ==========================================
# DATE VALIDATION TESTS
# ==========================================


class TestEducationDateValidation:
    """Tests for Education date validation."""

    def test_end_date_before_start_date_raises_error(
        self, profile_id, today, yesterday
    ):
        """Should raise InvalidDateRangeError when end_date is before start_date."""
        with pytest.raises(InvalidDateRangeError):
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense de Madrid",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                end_date=yesterday,
                order_index=0,
            )

    def test_end_date_equal_to_start_date_raises_error(self, profile_id, today):
        """Should raise InvalidDateRangeError when end_date equals start_date."""
        with pytest.raises(InvalidDateRangeError):
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense de Madrid",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                end_date=today,
                order_index=0,
            )

    def test_end_date_after_start_date_is_valid(self, profile_id, yesterday, tomorrow):
        """Should accept end_date after start_date."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=yesterday,
            end_date=tomorrow,
            order_index=0,
        )

        assert education.start_date == yesterday
        assert education.end_date == tomorrow

    def test_no_end_date_is_valid(self, profile_id, today):
        """Should accept education with no end_date (ongoing)."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        assert education.end_date is None


# ==========================================
# UPDATE OPERATIONS TESTS
# ==========================================


class TestEducationUpdateOperations:
    """Tests for Education update operations."""

    def test_update_institution(self, profile_id, today):
        """Should update institution field."""
        education = Education.create(
            profile_id=profile_id,
            institution="Old Institution",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        education.update_info(institution="New Institution")

        assert education.institution == "New Institution"

    def test_update_degree(self, profile_id, today):
        """Should update degree field."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Old Degree",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        education.update_info(degree="New Degree")

        assert education.degree == "New Degree"

    def test_update_field(self, profile_id, today):
        """Should update field of study."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Old Field",
            start_date=today,
            order_index=0,
        )

        education.update_info(field="New Field")

        assert education.field == "New Field"

    def test_update_description(self, profile_id, today):
        """Should update description."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        education.update_info(description="New description")

        assert education.description == "New description"

    def test_update_dates(self, profile_id, today, yesterday, tomorrow):
        """Should update start and end dates."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        education.update_info(start_date=yesterday, end_date=tomorrow)

        assert education.start_date == yesterday
        assert education.end_date == tomorrow

    def test_update_multiple_fields(self, profile_id, today):
        """Should update multiple fields at once."""
        education = Education.create(
            profile_id=profile_id,
            institution="Old Institution",
            degree="Old Degree",
            field="Old Field",
            start_date=today,
            order_index=0,
        )

        education.update_info(
            institution="New Institution",
            degree="New Degree",
            field="New Field",
            description="New description",
        )

        assert education.institution == "New Institution"
        assert education.degree == "New Degree"
        assert education.field == "New Field"
        assert education.description == "New description"

    def test_update_info_validates_institution(self, profile_id, today):
        """Should validate institution when updating."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        with pytest.raises(InvalidInstitutionError):
            education.update_info(institution="")

    def test_update_info_validates_degree(self, profile_id, today):
        """Should validate degree when updating."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        with pytest.raises(EmptyFieldError):
            education.update_info(degree="")

    def test_update_info_validates_dates(self, profile_id, today, yesterday):
        """Should validate date range when updating."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        with pytest.raises(InvalidDateRangeError):
            education.update_info(start_date=today, end_date=yesterday)

    def test_update_info_marks_as_updated(self, profile_id, today):
        """Should update updated_at timestamp when updating info."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        original_updated_at = education.updated_at

        # Small delay to ensure timestamp changes
        import time

        time.sleep(0.01)

        education.update_info(description="Updated description")

        assert education.updated_at > original_updated_at

    def test_update_order(self, profile_id, today):
        """Should update order_index."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        education.update_order(5)

        assert education.order_index == 5

    def test_update_order_validates_index(self, profile_id, today):
        """Should validate order_index when updating."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        with pytest.raises(InvalidOrderIndexError):
            education.update_order(-1)

    def test_update_order_marks_as_updated(self, profile_id, today):
        """Should update updated_at timestamp when updating order."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        original_updated_at = education.updated_at

        # Small delay to ensure timestamp changes
        import time

        time.sleep(0.01)

        education.update_order(1)

        assert education.updated_at > original_updated_at


# ==========================================
# QUERY METHODS TESTS
# ==========================================


class TestEducationQueryMethods:
    """Tests for Education query methods."""

    def test_is_ongoing_returns_true_when_no_end_date(self, profile_id, today):
        """Should return True for is_ongoing when end_date is None."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        assert education.is_ongoing() is True

    def test_is_ongoing_returns_false_when_has_end_date(
        self, profile_id, yesterday, tomorrow
    ):
        """Should return False for is_ongoing when end_date exists."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=yesterday,
            end_date=tomorrow,
            order_index=0,
        )

        assert education.is_ongoing() is False


# ==========================================
# ENTITY REPRESENTATION TESTS
# ==========================================


class TestEducationRepresentation:
    """Tests for Education entity representation."""

    def test_repr_contains_key_information(self, profile_id, today):
        """Should include key fields in __repr__."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        repr_str = repr(education)

        assert "Education" in repr_str
        assert education.id in repr_str
        assert "Bachelor of Science" in repr_str
        assert "Universidad Complutense de Madrid" in repr_str


# ==========================================
# EDGE CASES TESTS
# ==========================================


class TestEducationEdgeCases:
    """Tests for Education edge cases."""

    def test_create_with_exact_max_lengths(self, profile_id, today):
        """Should accept all fields at exact max length."""
        education = Education.create(
            profile_id=profile_id,
            institution="A" * 100,
            degree="B" * 100,
            field="C" * 100,
            description="D" * 1000,
            start_date=today,
            order_index=0,
        )

        assert len(education.institution) == 100
        assert len(education.degree) == 100
        assert len(education.field) == 100
        assert len(education.description) == 1000

    def test_update_description_to_whitespace_becomes_none(self, profile_id, today):
        """Should convert description to None when updated to whitespace."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
            description="Original description",
        )

        education.update_info(description="   ")

        assert education.description is None

    def test_created_at_and_updated_at_initially_same(self, profile_id, today):
        """Should have same created_at and updated_at on creation."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense de Madrid",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=today,
            order_index=0,
        )

        # They should be very close (within a second)
        time_diff = abs((education.updated_at - education.created_at).total_seconds())
        assert time_diff < 1
