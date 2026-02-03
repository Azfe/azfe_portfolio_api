#!/usr/bin/env python3
"""
Business Rules Validation Script.

Validates that all business rules are properly implemented in the domain layer.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# =========================================================
# ADD PROJECT ROOT TO PYTHONPATH
# =========================================================
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# =========================================================
# IMPORT DOMAIN MODULES
# =========================================================
from app.domain.entities import (
    Profile, WorkExperience, Skill, Education, Project,
    Certification, AdditionalTraining, ContactInformation,
    ContactMessage, SocialNetwork, Tool
)
from app.domain.value_objects import (
    DateRange, Email, Phone, SkillLevel, ContactInfo
)
from app.domain.exceptions import (
    EmptyFieldError, InvalidLengthError, InvalidEmailError,
    InvalidPhoneError, InvalidURLError, InvalidDateRangeError,
    InvalidSkillLevelError, DuplicateValueError,
    InvalidRoleError, InvalidNameError, InvalidInstitutionError
)

# =========================================================
# TESTS
# =========================================================

def test_profile_rules():
    print("Testing Profile rules...")

    try:
        Profile.create(name="", headline="Test")
        print("  ❌ RB-P01 FAILED: Empty name accepted")
        return False
    except EmptyFieldError:
        print("  ✅ RB-P01: Name required")

    try:
        Profile.create(name="Test", headline="")
        print("  ❌ RB-P02 FAILED: Empty headline accepted")
        return False
    except EmptyFieldError:
        print("  ✅ RB-P02: Headline required")

    try:
        Profile.create(name="Test", headline="Test", bio="x" * 1001)
        print("  ❌ RB-P03 FAILED: Bio over limit accepted")
        return False
    except InvalidLengthError:
        print("  ✅ RB-P03: Bio max length enforced")

    try:
        Profile.create(name="Test", headline="Test", avatar_url="not-a-url")
        print("  ❌ RB-P05 FAILED: Invalid URL accepted")
        return False
    except InvalidURLError:
        print("  ✅ RB-P05: Avatar URL validated")

    return True


def test_work_experience_rules():
    print("\nTesting WorkExperience rules...")
    profile_id = "test-profile-id"

    try:
        WorkExperience.create(
            profile_id=profile_id,
            role="",
            company="Test",
            start_date=datetime.now(),
            order_index=0
        )
        print("  ❌ RB-W01 FAILED: Empty role accepted")
        return False
    except (EmptyFieldError, InvalidRoleError):
        print("  ✅ RB-W01: Role required")

    try:
        WorkExperience.create(
            profile_id=profile_id,
            role="Test",
            company="Test",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2022, 1, 1),
            order_index=0
        )
        print("  ❌ RB-W05 FAILED: Invalid date range accepted")
        return False
    except InvalidDateRangeError:
        print("  ✅ RB-W05: Date range validated")

    return True


def test_skill_rules():
    print("\nTesting Skill rules...")
    profile_id = "test-profile-id"

    try:
        Skill.create(
            profile_id=profile_id,
            name="",
            category="Test",
            order_index=0
        )
        print("  ❌ RB-S01 FAILED: Empty name accepted")
        return False
    except (EmptyFieldError, InvalidNameError):
        print("  ✅ RB-S01: Name required")

    try:
        Skill.create(
            profile_id=profile_id,
            name="Test",
            category="Test",
            level="invalid",
            order_index=0
        )
        print("  ❌ RB-S04 FAILED: Invalid level accepted")
        return False
    except InvalidSkillLevelError:
        print("  ✅ RB-S04: Level validated")

    return True


def test_education_rules():
    print("\nTesting Education rules...")
    profile_id = "test-profile-id"

    try:
        Education.create(
            profile_id=profile_id,
            institution="",
            degree="Test",
            field="Test",
            start_date=datetime.now(),
            order_index=0
        )
        print("  ❌ RB-E01 FAILED: Empty institution accepted")
        return False
    except (EmptyFieldError, InvalidInstitutionError):
        print("  ✅ RB-E01: Institution required")

    try:
        Education.create(
            profile_id=profile_id,
            institution="Test",
            degree="Test",
            field="Test",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2022, 1, 1),
            order_index=0
        )
        print("  ❌ RB-E05 FAILED: Invalid date range accepted")
        return False
    except InvalidDateRangeError:
        print("  ✅ RB-E05: Date range validated")

    return True


def test_contact_message_rules():
    print("\nTesting ContactMessage rules...")

    try:
        ContactMessage.create(
            name="",
            email="test@example.com",
            message="Test message here"
        )
        print("  ❌ RB-CM01 FAILED: Empty name accepted")
        return False
    except (EmptyFieldError, InvalidNameError):
        print("  ✅ RB-CM01: Name required")

    try:
        ContactMessage.create(
            name="Test",
            email="invalid-email",
            message="Test message here"
        )
        print("  ❌ RB-CM02 FAILED: Invalid email accepted")
        return False
    except InvalidEmailError:
        print("  ✅ RB-CM02: Email validated")

    try:
        ContactMessage.create(
            name="Test",
            email="test@example.com",
            message="Short"
        )
        print("  ❌ RB-CM03 FAILED: Short message accepted")
        return False
    except InvalidLengthError:
        print("  ✅ RB-CM03: Message length validated")

    return True


def test_value_object_rules():
    print("\nTesting Value Object rules...")

    try:
        Email.create("invalid-email")
        print("  ❌ VR-E01 FAILED: Invalid email accepted")
        return False
    except InvalidEmailError:
        print("  ✅ VR-E01: Email format validated")

    try:
        Phone.create("abc")
        print("  ❌ VR-P01 FAILED: Invalid phone accepted")
        return False
    except InvalidPhoneError:
        print("  ✅ VR-P01: Phone validated")

    try:
        SkillLevel.create("invalid")
        print("  ❌ VR-SL01 FAILED: Invalid level accepted")
        return False
    except InvalidSkillLevelError:
        print("  ✅ VR-SL01: SkillLevel validated")

    try:
        DateRange.completed(
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2022, 1, 1)
        )
        print("  ❌ VR-DR02 FAILED: Invalid date range accepted")
        return False
    except InvalidDateRangeError:
        print("  ✅ VR-DR02: DateRange validated")

    return True


def test_immutability():
    print("\nTesting immutability...")

    email = Email.create("test@example.com")
    try:
        email.value = "new@example.com"
        print("  ❌ Email not immutable")
        return False
    except AttributeError:
        print("  ✅ Email is immutable")

    dr = DateRange.ongoing(datetime.now())
    try:
        dr.start_date = datetime.now()
        print("  ❌ DateRange not immutable")
        return False
    except AttributeError:
        print("  ✅ DateRange is immutable")

    return True


def main():
    print("=" * 60)
    print("BUSINESS RULES VALIDATION")
    print("=" * 60)

    tests = [
        test_profile_rules,
        test_work_experience_rules,
        test_skill_rules,
        test_education_rules,
        test_contact_message_rules,
        test_value_object_rules,
        test_immutability,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("✅ ALL BUSINESS RULES VALIDATED SUCCESSFULLY")
        return 0
    else:
        print("❌ SOME BUSINESS RULES FAILED VALIDATION")
        return 1


if __name__ == "__main__":
    sys.exit(main())
