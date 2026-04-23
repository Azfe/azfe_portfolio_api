"""
Tests for ProgrammingLanguageLevel Value Object.
"""

import pytest

from app.domain.exceptions import InvalidProgrammingLanguageLevelError
from app.domain.value_objects.programming_language_level import ProgrammingLanguageLevel


@pytest.mark.value_object
class TestProgrammingLanguageLevelCreation:
    """Test ProgrammingLanguageLevel creation."""

    @pytest.mark.parametrize("level", ["basic", "intermediate", "advanced", "expert"])
    def test_create_valid_levels(self, level):
        """Should create valid levels."""
        pl_level = ProgrammingLanguageLevel.create(level)

        assert pl_level.to_string() == level

    def test_create_case_insensitive(self):
        """Should accept levels in any case."""
        pl_level = ProgrammingLanguageLevel.create("ADVANCED")

        assert pl_level.to_string() == "advanced"

    def test_create_with_whitespace(self):
        """Should trim whitespace."""
        pl_level = ProgrammingLanguageLevel.create("  expert  ")

        assert pl_level.to_string() == "expert"

    def test_try_create_valid(self):
        """Should return instance for valid level."""
        result = ProgrammingLanguageLevel.try_create("basic")

        assert result is not None
        assert result.to_string() == "basic"

    def test_try_create_invalid(self):
        """Should return None for invalid level."""
        result = ProgrammingLanguageLevel.try_create("master")

        assert result is None

    def test_factory_basic(self):
        """Should create basic level via factory."""
        assert ProgrammingLanguageLevel.basic().is_basic()

    def test_factory_intermediate(self):
        """Should create intermediate level via factory."""
        assert ProgrammingLanguageLevel.intermediate().is_intermediate()

    def test_factory_advanced(self):
        """Should create advanced level via factory."""
        assert ProgrammingLanguageLevel.advanced().is_advanced()

    def test_factory_expert(self):
        """Should create expert level via factory."""
        assert ProgrammingLanguageLevel.expert().is_expert()

    def test_all_levels_returns_four(self):
        """Should return all 4 levels in order."""
        levels = ProgrammingLanguageLevel.all_levels()

        assert len(levels) == 4
        assert levels[0].is_basic()
        assert levels[3].is_expert()


@pytest.mark.value_object
class TestProgrammingLanguageLevelValidation:
    """Test ProgrammingLanguageLevel validation."""

    def test_invalid_level_raises_error(self):
        """Should raise error for invalid level."""
        with pytest.raises(InvalidProgrammingLanguageLevelError):
            ProgrammingLanguageLevel.create("master")

    @pytest.mark.parametrize("invalid", ["beginner", "pro", "novice", ""])
    def test_various_invalid_levels(self, invalid):
        """Should reject invalid levels."""
        with pytest.raises(InvalidProgrammingLanguageLevelError):
            ProgrammingLanguageLevel.create(invalid)


@pytest.mark.value_object
class TestProgrammingLanguageLevelComparison:
    """Test ProgrammingLanguageLevel comparison."""

    def test_levels_ordered(self):
        """Should maintain order."""
        basic = ProgrammingLanguageLevel.basic()
        intermediate = ProgrammingLanguageLevel.intermediate()
        advanced = ProgrammingLanguageLevel.advanced()
        expert = ProgrammingLanguageLevel.expert()

        assert basic < intermediate < advanced < expert

    def test_less_than_or_equal(self):
        """Should support <= comparison."""
        basic = ProgrammingLanguageLevel.basic()
        also_basic = ProgrammingLanguageLevel.basic()

        assert basic <= also_basic
        assert basic <= ProgrammingLanguageLevel.intermediate()

    def test_greater_than(self):
        """Should support > comparison."""
        assert ProgrammingLanguageLevel.expert() > ProgrammingLanguageLevel.basic()

    def test_greater_than_or_equal(self):
        """Should support >= comparison."""
        expert = ProgrammingLanguageLevel.expert()

        assert expert >= ProgrammingLanguageLevel.expert()
        assert expert >= ProgrammingLanguageLevel.advanced()

    def test_is_at_least(self):
        """Should check minimum level."""
        advanced = ProgrammingLanguageLevel.advanced()

        assert advanced.is_at_least(ProgrammingLanguageLevel.basic())
        assert advanced.is_at_least(ProgrammingLanguageLevel.advanced())
        assert not ProgrammingLanguageLevel.basic().is_at_least(advanced)


@pytest.mark.value_object
class TestProgrammingLanguageLevelEquality:
    """Test ProgrammingLanguageLevel equality."""

    def test_same_level_equals(self):
        """Should be equal for same level."""
        level1 = ProgrammingLanguageLevel.create("intermediate")
        level2 = ProgrammingLanguageLevel.create("intermediate")

        assert level1 == level2

    def test_different_level_not_equals(self):
        """Should not be equal for different levels."""
        assert ProgrammingLanguageLevel.basic() != ProgrammingLanguageLevel.expert()

    def test_not_equal_to_other_type(self):
        """Should not be equal to non-ProgrammingLanguageLevel."""
        assert ProgrammingLanguageLevel.basic() != "basic"

    def test_hash_same_for_equal(self):
        """Should have same hash for equal instances."""
        level1 = ProgrammingLanguageLevel.create("expert")
        level2 = ProgrammingLanguageLevel.create("expert")

        assert hash(level1) == hash(level2)
        assert len({level1, level2}) == 1


@pytest.mark.value_object
class TestProgrammingLanguageLevelImmutability:
    """Test ProgrammingLanguageLevel immutability."""

    def test_immutable(self):
        """Should not allow modification."""
        level = ProgrammingLanguageLevel.create("basic")

        with pytest.raises(AttributeError):
            level.level = ProgrammingLanguageLevel.create("expert").level


@pytest.mark.value_object
class TestProgrammingLanguageLevelDisplay:
    """Test ProgrammingLanguageLevel string representations."""

    def test_str(self):
        """Should return level value as string."""
        assert str(ProgrammingLanguageLevel.basic()) == "basic"

    def test_repr(self):
        """Should return debug representation."""
        assert (
            repr(ProgrammingLanguageLevel.basic()) == "ProgrammingLanguageLevel.basic()"
        )

    def test_display_name(self):
        """Should return capitalized name."""
        assert ProgrammingLanguageLevel.advanced().display_name() == "Advanced"
