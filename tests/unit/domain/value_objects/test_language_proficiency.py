"""
Tests for LanguageProficiency Value Object.
"""

import pytest

from app.domain.exceptions import InvalidLanguageProficiencyError
from app.domain.value_objects.language_proficiency import LanguageProficiency


@pytest.mark.value_object
class TestLanguageProficiencyCreation:
    """Test LanguageProficiency creation."""

    @pytest.mark.parametrize("level", ["a1", "a2", "b1", "b2", "c1", "c2"])
    def test_create_valid_levels(self, level):
        """Should create valid CEFR levels."""
        proficiency = LanguageProficiency.create(level)

        assert proficiency.to_string() == level

    def test_create_case_insensitive(self):
        """Should accept levels in any case."""
        proficiency = LanguageProficiency.create("B2")

        assert proficiency.to_string() == "b2"

    def test_create_with_whitespace(self):
        """Should trim whitespace."""
        proficiency = LanguageProficiency.create("  c1  ")

        assert proficiency.to_string() == "c1"

    def test_try_create_valid(self):
        """Should return instance for valid level."""
        result = LanguageProficiency.try_create("a1")

        assert result is not None
        assert result.to_string() == "a1"

    def test_try_create_invalid(self):
        """Should return None for invalid level."""
        result = LanguageProficiency.try_create("d1")

        assert result is None

    def test_factory_a1(self):
        """Should create A1 level via factory."""
        assert LanguageProficiency.a1().is_a1()

    def test_factory_a2(self):
        """Should create A2 level via factory."""
        assert LanguageProficiency.a2().is_a2()

    def test_factory_b1(self):
        """Should create B1 level via factory."""
        assert LanguageProficiency.b1().is_b1()

    def test_factory_b2(self):
        """Should create B2 level via factory."""
        assert LanguageProficiency.b2().is_b2()

    def test_factory_c1(self):
        """Should create C1 level via factory."""
        assert LanguageProficiency.c1().is_c1()

    def test_factory_c2(self):
        """Should create C2 level via factory."""
        assert LanguageProficiency.c2().is_c2()

    def test_all_levels_returns_six(self):
        """Should return all 6 CEFR levels in order."""
        levels = LanguageProficiency.all_levels()

        assert len(levels) == 6
        assert levels[0].is_a1()
        assert levels[5].is_c2()


@pytest.mark.value_object
class TestLanguageProficiencyValidation:
    """Test LanguageProficiency validation."""

    def test_invalid_level_raises_error(self):
        """Should raise error for invalid level."""
        with pytest.raises(InvalidLanguageProficiencyError):
            LanguageProficiency.create("d1")

    @pytest.mark.parametrize("invalid", ["native", "fluent", "beginner", ""])
    def test_various_invalid_levels(self, invalid):
        """Should reject invalid levels."""
        with pytest.raises(InvalidLanguageProficiencyError):
            LanguageProficiency.create(invalid)


@pytest.mark.value_object
class TestLanguageProficiencyComparison:
    """Test LanguageProficiency comparison."""

    def test_levels_ordered(self):
        """Should maintain CEFR order A1 < A2 < B1 < B2 < C1 < C2."""
        a1 = LanguageProficiency.a1()
        a2 = LanguageProficiency.a2()
        b1 = LanguageProficiency.b1()
        b2 = LanguageProficiency.b2()
        c1 = LanguageProficiency.c1()
        c2 = LanguageProficiency.c2()

        assert a1 < a2 < b1 < b2 < c1 < c2

    def test_less_than_or_equal(self):
        """Should support <= comparison."""
        b1 = LanguageProficiency.b1()
        also_b1 = LanguageProficiency.b1()

        assert b1 <= also_b1
        assert b1 <= LanguageProficiency.b2()

    def test_greater_than(self):
        """Should support > comparison."""
        assert LanguageProficiency.c2() > LanguageProficiency.a1()

    def test_greater_than_or_equal(self):
        """Should support >= comparison."""
        c2 = LanguageProficiency.c2()

        assert c2 >= LanguageProficiency.c2()
        assert c2 >= LanguageProficiency.c1()

    def test_is_at_least(self):
        """Should check minimum proficiency."""
        b2 = LanguageProficiency.b2()

        assert b2.is_at_least(LanguageProficiency.a1())
        assert b2.is_at_least(LanguageProficiency.b2())
        assert not LanguageProficiency.a1().is_at_least(b2)


@pytest.mark.value_object
class TestLanguageProficiencyEquality:
    """Test LanguageProficiency equality."""

    def test_same_level_equals(self):
        """Should be equal for same level."""
        level1 = LanguageProficiency.create("b2")
        level2 = LanguageProficiency.create("b2")

        assert level1 == level2

    def test_different_level_not_equals(self):
        """Should not be equal for different levels."""
        assert LanguageProficiency.a1() != LanguageProficiency.c2()

    def test_not_equal_to_other_type(self):
        """Should not be equal to non-LanguageProficiency."""
        assert LanguageProficiency.a1() != "a1"

    def test_hash_same_for_equal(self):
        """Should have same hash for equal instances."""
        level1 = LanguageProficiency.create("c1")
        level2 = LanguageProficiency.create("c1")

        assert hash(level1) == hash(level2)
        assert len({level1, level2}) == 1


@pytest.mark.value_object
class TestLanguageProficiencyImmutability:
    """Test LanguageProficiency immutability."""

    def test_immutable(self):
        """Should not allow modification."""
        level = LanguageProficiency.create("a1")

        with pytest.raises(AttributeError):
            level.level = LanguageProficiency.create("c2").level


@pytest.mark.value_object
class TestLanguageProficiencyDisplay:
    """Test LanguageProficiency string representations."""

    def test_str(self):
        """Should return level value as string."""
        assert str(LanguageProficiency.b1()) == "b1"

    def test_repr(self):
        """Should return debug representation."""
        assert repr(LanguageProficiency.b1()) == "LanguageProficiency.b1()"

    def test_display_name(self):
        """Should return CEFR display name."""
        assert LanguageProficiency.b2().display_name() == "B2 - Upper Intermediate"

    @pytest.mark.parametrize(
        ("level", "expected"),
        [
            ("a1", "A1 - Beginner"),
            ("a2", "A2 - Elementary"),
            ("b1", "B1 - Intermediate"),
            ("b2", "B2 - Upper Intermediate"),
            ("c1", "C1 - Advanced"),
            ("c2", "C2 - Proficient"),
        ],
    )
    def test_all_display_names(self, level, expected):
        """Should return correct display name for each level."""
        assert LanguageProficiency.create(level).display_name() == expected
