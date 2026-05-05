"""
Extended tests for LanguageProficiency Value Object.

Covers uncovered comparison operator lines (returning NotImplemented for wrong types)
and ProgrammingLanguageLevel equivalent gap-filling.
"""

import pytest

from app.domain.value_objects.language_proficiency import (
    LanguageProficiency,
    LanguageProficiencyEnum,
)
from app.domain.value_objects.programming_language_level import (
    ProgrammingLanguageLevel,
    ProgrammingLanguageLevelEnum,
)


@pytest.mark.value_object
class TestLanguageProficiencyComparisonWithWrongType:
    """Test that comparison operators return NotImplemented for non-LanguageProficiency."""

    def test_lt_returns_not_implemented_for_wrong_type(self):
        """__lt__ should return NotImplemented for non-LanguageProficiency."""
        result = LanguageProficiency.a1().__lt__("a1")
        assert result is NotImplemented

    def test_le_returns_not_implemented_for_wrong_type(self):
        """__le__ should return NotImplemented for non-LanguageProficiency."""
        result = LanguageProficiency.b1().__le__(42)
        assert result is NotImplemented

    def test_gt_returns_not_implemented_for_wrong_type(self):
        """__gt__ should return NotImplemented for non-LanguageProficiency."""
        result = LanguageProficiency.c2().__gt__("c2")
        assert result is NotImplemented

    def test_ge_returns_not_implemented_for_wrong_type(self):
        """__ge__ should return NotImplemented for non-LanguageProficiency."""
        result = LanguageProficiency.b2().__ge__(None)
        assert result is NotImplemented


@pytest.mark.value_object
class TestLanguageProficiencyEnumOrdering:
    """Test LanguageProficiencyEnum comparison operators."""

    def test_enum_lt_returns_not_implemented_for_wrong_type(self):
        """LanguageProficiencyEnum.__lt__() should return NotImplemented for non-enum."""
        result = LanguageProficiencyEnum.A1.__lt__("a1")
        assert result is NotImplemented

    def test_enum_str(self):
        """LanguageProficiencyEnum.__str__() should return the level value."""
        assert str(LanguageProficiencyEnum.A1) == "a1"
        assert str(LanguageProficiencyEnum.C2) == "c2"


@pytest.mark.value_object
class TestProgrammingLanguageLevelComparisonWithWrongType:
    """Test that comparison operators return NotImplemented for wrong types."""

    def test_lt_returns_not_implemented_for_wrong_type(self):
        """__lt__ should return NotImplemented for non-ProgrammingLanguageLevel."""
        result = ProgrammingLanguageLevel.basic().__lt__("basic")
        assert result is NotImplemented

    def test_le_returns_not_implemented_for_wrong_type(self):
        """__le__ should return NotImplemented for non-ProgrammingLanguageLevel."""
        result = ProgrammingLanguageLevel.intermediate().__le__(42)
        assert result is NotImplemented

    def test_gt_returns_not_implemented_for_wrong_type(self):
        """__gt__ should return NotImplemented for non-ProgrammingLanguageLevel."""
        result = ProgrammingLanguageLevel.advanced().__gt__("advanced")
        assert result is NotImplemented

    def test_ge_returns_not_implemented_for_wrong_type(self):
        """__ge__ should return NotImplemented for non-ProgrammingLanguageLevel."""
        result = ProgrammingLanguageLevel.expert().__ge__(None)
        assert result is NotImplemented


@pytest.mark.value_object
class TestProgrammingLanguageLevelEnumOrdering:
    """Test ProgrammingLanguageLevelEnum comparison operators."""

    def test_enum_lt_returns_not_implemented_for_wrong_type(self):
        """ProgrammingLanguageLevelEnum.__lt__() should return NotImplemented for non-enum."""
        result = ProgrammingLanguageLevelEnum.BASIC.__lt__("basic")
        assert result is NotImplemented

    def test_enum_str(self):
        """ProgrammingLanguageLevelEnum.__str__() should return the value."""
        assert str(ProgrammingLanguageLevelEnum.BASIC) == "basic"
        assert str(ProgrammingLanguageLevelEnum.EXPERT) == "expert"
