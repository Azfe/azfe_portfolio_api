"""
Tests for SkillLevel Value Object.
"""

import pytest

from app.domain.exceptions import InvalidSkillLevelError
from app.domain.value_objects.skill_level import SkillLevel


@pytest.mark.value_object
class TestSkillLevelCreation:
    """Test SkillLevel creation."""

    @pytest.mark.parametrize("level", ["basic", "intermediate", "advanced", "expert"])
    def test_create_valid_levels(self, level):
        """Should create valid levels."""
        skill_level = SkillLevel.create(level)

        assert skill_level.to_string() == level


@pytest.mark.value_object
class TestSkillLevelValidation:
    """Test SkillLevel validation."""

    def test_invalid_level_raises_error(self):
        """Should raise error for invalid level."""
        with pytest.raises(InvalidSkillLevelError):
            SkillLevel.create("master")

    @pytest.mark.parametrize("invalid", ["beginner", "pro", "novice", ""])
    def test_various_invalid_levels(self, invalid):
        """Should reject invalid levels."""
        with pytest.raises(InvalidSkillLevelError):
            SkillLevel.create(invalid)


@pytest.mark.value_object
class TestSkillLevelComparison:
    """Test SkillLevel comparison."""

    def test_levels_ordered(self):
        """Should maintain order."""
        basic = SkillLevel.create("basic")
        intermediate = SkillLevel.create("intermediate")
        advanced = SkillLevel.create("advanced")
        expert = SkillLevel.create("expert")

        assert basic < intermediate < advanced < expert

    # --- __lt__ ---

    @pytest.mark.unit
    def test_lt_lower_level_is_less_than_higher(self):
        """Lower level should be less than a higher level."""
        assert SkillLevel.basic() < SkillLevel.intermediate()
        assert SkillLevel.intermediate() < SkillLevel.advanced()
        assert SkillLevel.advanced() < SkillLevel.expert()

    @pytest.mark.unit
    def test_lt_equal_levels_are_not_less_than(self):
        """Equal levels should not satisfy __lt__."""
        assert not (SkillLevel.basic() < SkillLevel.basic())
        assert not (SkillLevel.expert() < SkillLevel.expert())

    @pytest.mark.unit
    def test_lt_higher_level_is_not_less_than_lower(self):
        """Higher level should not be less than a lower level."""
        assert not (SkillLevel.expert() < SkillLevel.basic())
        assert not (SkillLevel.advanced() < SkillLevel.intermediate())

    @pytest.mark.unit
    def test_lt_transitive(self):
        """__lt__ should be transitive: A < B and B < C implies A < C."""
        basic = SkillLevel.basic()
        intermediate = SkillLevel.intermediate()
        expert = SkillLevel.expert()

        assert basic < intermediate
        assert intermediate < expert
        assert basic < expert

    # --- __le__ ---

    @pytest.mark.unit
    def test_le_lower_level_is_less_than_or_equal_to_higher(self):
        """Lower level should satisfy __le__ against a higher level."""
        assert SkillLevel.basic() <= SkillLevel.intermediate()
        assert SkillLevel.intermediate() <= SkillLevel.advanced()
        assert SkillLevel.advanced() <= SkillLevel.expert()

    @pytest.mark.unit
    def test_le_equal_levels_satisfy_le(self):
        """Equal levels should satisfy __le__."""
        assert SkillLevel.basic() <= SkillLevel.basic()
        assert SkillLevel.intermediate() <= SkillLevel.intermediate()
        assert SkillLevel.expert() <= SkillLevel.expert()

    @pytest.mark.unit
    def test_le_higher_level_does_not_satisfy_le_against_lower(self):
        """Higher level should not satisfy __le__ against a lower level."""
        assert not (SkillLevel.expert() <= SkillLevel.basic())
        assert not (SkillLevel.advanced() <= SkillLevel.intermediate())

    # --- __gt__ ---

    @pytest.mark.unit
    def test_gt_higher_level_is_greater_than_lower(self):
        """Higher level should be greater than a lower level."""
        assert SkillLevel.intermediate() > SkillLevel.basic()
        assert SkillLevel.advanced() > SkillLevel.intermediate()
        assert SkillLevel.expert() > SkillLevel.advanced()

    @pytest.mark.unit
    def test_gt_equal_levels_are_not_greater_than(self):
        """Equal levels should not satisfy __gt__."""
        assert not (SkillLevel.basic() > SkillLevel.basic())
        assert not (SkillLevel.expert() > SkillLevel.expert())

    @pytest.mark.unit
    def test_gt_lower_level_is_not_greater_than_higher(self):
        """Lower level should not be greater than a higher level."""
        assert not (SkillLevel.basic() > SkillLevel.expert())
        assert not (SkillLevel.intermediate() > SkillLevel.advanced())

    @pytest.mark.unit
    def test_gt_transitive(self):
        """__gt__ should be transitive: A > B and B > C implies A > C."""
        expert = SkillLevel.expert()
        intermediate = SkillLevel.intermediate()
        basic = SkillLevel.basic()

        assert expert > intermediate
        assert intermediate > basic
        assert expert > basic

    # --- __ge__ ---

    @pytest.mark.unit
    def test_ge_higher_level_is_greater_than_or_equal_to_lower(self):
        """Higher level should satisfy __ge__ against a lower level."""
        assert SkillLevel.intermediate() >= SkillLevel.basic()
        assert SkillLevel.advanced() >= SkillLevel.intermediate()
        assert SkillLevel.expert() >= SkillLevel.advanced()

    @pytest.mark.unit
    def test_ge_equal_levels_satisfy_ge(self):
        """Equal levels should satisfy __ge__."""
        assert SkillLevel.basic() >= SkillLevel.basic()
        assert SkillLevel.intermediate() >= SkillLevel.intermediate()
        assert SkillLevel.expert() >= SkillLevel.expert()

    @pytest.mark.unit
    def test_ge_lower_level_does_not_satisfy_ge_against_higher(self):
        """Lower level should not satisfy __ge__ against a higher level."""
        assert not (SkillLevel.basic() >= SkillLevel.expert())
        assert not (SkillLevel.intermediate() >= SkillLevel.advanced())


@pytest.mark.value_object
class TestSkillLevelEquality:
    """Test SkillLevel equality."""

    def test_same_level_equals(self):
        """Should be equal for same level."""
        level1 = SkillLevel.create("intermediate")
        level2 = SkillLevel.create("intermediate")

        assert level1 == level2


@pytest.mark.value_object
class TestSkillLevelImmutability:
    """Test SkillLevel immutability."""

    def test_immutable(self):
        """Should not allow modification."""
        level = SkillLevel.create("basic")

        with pytest.raises(AttributeError):
            level.level = SkillLevel.create("expert").level
