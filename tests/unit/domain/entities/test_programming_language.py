"""
Tests for ProgrammingLanguage Entity.
"""

import pytest

from app.domain.entities.programming_language import ProgrammingLanguage
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
    InvalidProgrammingLanguageLevelError,
)


@pytest.mark.entity
class TestProgrammingLanguageCreation:
    """Test ProgrammingLanguage creation."""

    def test_create_with_required_fields(self, profile_id):
        """Should create programming language with required fields."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0
        )

        assert pl.name == "Python"
        assert pl.order_index == 0
        assert pl.level is None
        assert pl.profile_id == profile_id
        assert pl.id is not None

    def test_create_with_level(self, profile_id):
        """Should create with level."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id,
            name="TypeScript",
            order_index=1,
            level="advanced",
        )

        assert pl.level == "advanced"

    def test_create_normalizes_level_to_lowercase(self, profile_id):
        """Should normalize level to lowercase."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id,
            name="Rust",
            order_index=0,
            level="EXPERT",
        )

        assert pl.level == "expert"

    def test_create_sets_timestamps(self, profile_id):
        """Should set created_at and updated_at."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Go", order_index=0
        )

        assert pl.created_at is not None
        assert pl.updated_at is not None

    def test_create_generates_unique_ids(self, profile_id):
        """Should generate unique IDs."""
        pl1 = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0
        )
        pl2 = ProgrammingLanguage.create(
            profile_id=profile_id, name="Java", order_index=1
        )

        assert pl1.id != pl2.id


@pytest.mark.entity
@pytest.mark.business_rule
class TestProgrammingLanguageValidation:
    """Test ProgrammingLanguage validation rules."""

    def test_empty_name_raises_error(self, profile_id):
        """Should raise error for empty name."""
        with pytest.raises((InvalidNameError, InvalidLengthError)):
            ProgrammingLanguage.create(
                profile_id=profile_id, name="", order_index=0
            )

    def test_whitespace_name_raises_error(self, profile_id):
        """Should raise error for whitespace-only name."""
        with pytest.raises((InvalidNameError, InvalidLengthError)):
            ProgrammingLanguage.create(
                profile_id=profile_id, name="   ", order_index=0
            )

    def test_name_too_long_raises_error(self, profile_id):
        """Should raise error for name > 50 chars."""
        with pytest.raises(InvalidLengthError):
            ProgrammingLanguage.create(
                profile_id=profile_id, name="x" * 51, order_index=0
            )

    def test_empty_profile_id_raises_error(self):
        """Should raise error for empty profile_id."""
        with pytest.raises(EmptyFieldError):
            ProgrammingLanguage.create(
                profile_id="", name="Python", order_index=0
            )

    def test_invalid_level_raises_error(self, profile_id):
        """Should raise error for invalid level."""
        with pytest.raises(InvalidProgrammingLanguageLevelError):
            ProgrammingLanguage.create(
                profile_id=profile_id,
                name="Python",
                order_index=0,
                level="master",
            )

    def test_negative_order_index_raises_error(self, profile_id):
        """Should raise error for negative order index."""
        with pytest.raises(InvalidOrderIndexError):
            ProgrammingLanguage.create(
                profile_id=profile_id, name="Python", order_index=-1
            )

    def test_empty_level_string_becomes_none(self, profile_id):
        """Should treat empty string level as None."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0, level="  "
        )

        assert pl.level is None

    @pytest.mark.parametrize(
        "valid_level", ["basic", "intermediate", "advanced", "expert"]
    )
    def test_all_valid_levels_accepted(self, profile_id, valid_level):
        """Should accept all valid levels."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id,
            name="Python",
            order_index=0,
            level=valid_level,
        )

        assert pl.level == valid_level


@pytest.mark.entity
class TestProgrammingLanguageUpdate:
    """Test ProgrammingLanguage updates."""

    def test_update_info_name(self, profile_id):
        """Should update name."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0
        )
        old_updated = pl.updated_at

        pl.update_info(name="Python 3")

        assert pl.name == "Python 3"
        assert pl.updated_at >= old_updated

    def test_update_info_level(self, profile_id):
        """Should update level."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0
        )

        pl.update_info(level="expert")

        assert pl.level == "expert"

    def test_update_info_both(self, profile_id):
        """Should update name and level together."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="JS", order_index=0, level="basic"
        )

        pl.update_info(name="TypeScript", level="intermediate")

        assert pl.name == "TypeScript"
        assert pl.level == "intermediate"

    def test_update_order(self, profile_id):
        """Should update order index."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0
        )

        pl.update_order(5)

        assert pl.order_index == 5

    def test_remove_level(self, profile_id):
        """Should remove level."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0, level="expert"
        )

        pl.remove_level()

        assert pl.level is None

    def test_update_with_invalid_name_raises_error(self, profile_id):
        """Should raise error when updating to invalid name."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0
        )

        with pytest.raises((InvalidNameError, InvalidLengthError)):
            pl.update_info(name="")

    def test_update_with_invalid_level_raises_error(self, profile_id):
        """Should raise error when updating to invalid level."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id, name="Python", order_index=0
        )

        with pytest.raises(InvalidProgrammingLanguageLevelError):
            pl.update_info(level="godlike")


@pytest.mark.entity
class TestProgrammingLanguageRepr:
    """Test ProgrammingLanguage string representation."""

    def test_repr(self, profile_id):
        """Should return readable repr."""
        pl = ProgrammingLanguage.create(
            profile_id=profile_id,
            name="Python",
            order_index=0,
            level="expert",
        )

        result = repr(pl)

        assert "Python" in result
        assert "expert" in result
