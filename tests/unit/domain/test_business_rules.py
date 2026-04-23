"""
Unit tests for Business Rules Validation.

This test suite validates that all business rules defined in the domain
layer are properly implemented and enforced.

Business Rules Covered:
- Profile rules (RB-P01 to RB-P05)
- WorkExperience rules (RB-W01 to RB-W05)
- Skill rules (RB-S01 to RB-S04)
- Education rules (RB-E01 to RB-E05)
- ContactMessage rules (RB-CM01 to RB-CM03)
- Value Object rules (VR-E01, VR-P01, VR-SL01, VR-DR02)
- Immutability constraints
"""

from datetime import datetime, timedelta

import pytest

from app.domain.entities.contact_message import ContactMessage
from app.domain.entities.education import Education
from app.domain.entities.profile import Profile
from app.domain.entities.skill import Skill
from app.domain.entities.work_experience import WorkExperience
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidCategoryError,
    InvalidCompanyError,
    InvalidDateRangeError,
    InvalidEmailError,
    InvalidInstitutionError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
    InvalidPhoneError,
    InvalidRoleError,
    InvalidSkillLevelError,
    InvalidURLError,
)
from app.domain.value_objects.date_range import DateRange
from app.domain.value_objects.email import Email
from app.domain.value_objects.phone import Phone
from app.domain.value_objects.skill_level import SkillLevel

# ==========================================
# PROFILE BUSINESS RULES TESTS
# ==========================================


class TestProfileBusinessRules:
    """Tests for Profile entity business rules."""

    def test_rb_p01_name_is_required(self):
        """RB-P01: Profile name is required."""
        with pytest.raises(EmptyFieldError):
            Profile.create(name="", headline="Test Headline")

    def test_rb_p01_name_not_whitespace_only(self):
        """RB-P01: Profile name cannot be whitespace only."""
        with pytest.raises(EmptyFieldError):
            Profile.create(name="   ", headline="Test Headline")

    def test_rb_p02_headline_is_required(self):
        """RB-P02: Profile headline is required."""
        with pytest.raises(EmptyFieldError):
            Profile.create(name="John Doe", headline="")

    def test_rb_p02_headline_not_whitespace_only(self):
        """RB-P02: Profile headline cannot be whitespace only."""
        with pytest.raises(EmptyFieldError):
            Profile.create(name="John Doe", headline="   ")

    def test_rb_p03_bio_max_length_enforced(self):
        """RB-P03: Profile bio has maximum length of 1000 characters."""
        long_bio = "x" * 1001

        with pytest.raises(InvalidLengthError):
            Profile.create(name="John Doe", headline="Test Headline", bio=long_bio)

    def test_rb_p03_bio_max_length_accepted(self):
        """RB-P03: Profile bio at exactly max length is accepted."""
        max_bio = "x" * 1000

        profile = Profile.create(name="John Doe", headline="Test Headline", bio=max_bio)

        assert len(profile.bio) == 1000

    def test_rb_p05_avatar_url_must_be_valid(self):
        """RB-P05: Avatar URL must be valid format."""
        with pytest.raises(InvalidURLError):
            Profile.create(
                name="John Doe", headline="Test Headline", avatar_url="not-a-url"
            )

    def test_rb_p05_avatar_url_valid_accepted(self):
        """RB-P05: Valid avatar URL is accepted."""
        profile = Profile.create(
            name="John Doe",
            headline="Test Headline",
            avatar_url="https://example.com/avatar.jpg",
        )

        assert profile.avatar_url == "https://example.com/avatar.jpg"


# ==========================================
# WORK EXPERIENCE BUSINESS RULES TESTS
# ==========================================


class TestWorkExperienceBusinessRules:
    """Tests for WorkExperience entity business rules."""

    def test_rb_w01_role_is_required(self, profile_id, today):
        """RB-W01: Work experience role is required."""
        with pytest.raises((EmptyFieldError, InvalidRoleError)):
            WorkExperience.create(
                profile_id=profile_id,
                role="",
                company="Test Company",
                start_date=today,
                order_index=0,
            )

    def test_rb_w01_role_not_whitespace_only(self, profile_id, today):
        """RB-W01: Work experience role cannot be whitespace only."""
        with pytest.raises((EmptyFieldError, InvalidRoleError)):
            WorkExperience.create(
                profile_id=profile_id,
                role="   ",
                company="Test Company",
                start_date=today,
                order_index=0,
            )

    def test_rb_w02_company_is_required(self, profile_id, today):
        """RB-W02: Company name is required."""
        with pytest.raises((EmptyFieldError, InvalidCompanyError)):
            WorkExperience.create(
                profile_id=profile_id,
                role="Software Engineer",
                company="",
                start_date=today,
                order_index=0,
            )

    def test_rb_w05_end_date_must_be_after_start_date(
        self, profile_id, yesterday, today
    ):
        """RB-W05: End date must be after start date."""
        with pytest.raises(InvalidDateRangeError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Software Engineer",
                company="Test Company",
                start_date=today,
                end_date=yesterday,
                order_index=0,
            )

    def test_rb_w05_end_date_cannot_equal_start_date(self, profile_id, today):
        """RB-W05: End date cannot equal start date."""
        with pytest.raises(InvalidDateRangeError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Software Engineer",
                company="Test Company",
                start_date=today,
                end_date=today,
                order_index=0,
            )

    def test_rb_w05_valid_date_range_accepted(self, profile_id, yesterday, tomorrow):
        """RB-W05: Valid date range is accepted."""
        experience = WorkExperience.create(
            profile_id=profile_id,
            role="Software Engineer",
            company="Test Company",
            start_date=yesterday,
            end_date=tomorrow,
            order_index=0,
        )

        assert experience.start_date == yesterday
        assert experience.end_date == tomorrow


# ==========================================
# SKILL BUSINESS RULES TESTS
# ==========================================


class TestSkillBusinessRules:
    """Tests for Skill entity business rules."""

    def test_rb_s01_name_is_required(self, profile_id):
        """RB-S01: Skill name is required."""
        with pytest.raises((EmptyFieldError, InvalidNameError)):
            Skill.create(
                profile_id=profile_id, name="", category="backend", order_index=0
            )

    def test_rb_s01_name_not_whitespace_only(self, profile_id):
        """RB-S01: Skill name cannot be whitespace only."""
        with pytest.raises((EmptyFieldError, InvalidNameError)):
            Skill.create(
                profile_id=profile_id, name="   ", category="backend", order_index=0
            )

    def test_rb_s02_category_is_required(self, profile_id):
        """RB-S02: Skill category is required."""
        with pytest.raises((EmptyFieldError, InvalidCategoryError)):
            Skill.create(
                profile_id=profile_id, name="Python", category="", order_index=0
            )

    def test_rb_s04_level_must_be_valid(self, profile_id):
        """RB-S04: Skill level must be one of: basic, intermediate, advanced, expert."""
        with pytest.raises(InvalidSkillLevelError):
            Skill.create(
                profile_id=profile_id,
                name="Python",
                category="backend",
                level="invalid_level",
                order_index=0,
            )

    def test_rb_s04_valid_levels_accepted(self, profile_id):
        """RB-S04: All valid skill levels are accepted."""
        valid_levels = ["basic", "intermediate", "advanced", "expert"]

        for level in valid_levels:
            skill = Skill.create(
                profile_id=profile_id,
                name=f"Python-{level}",
                category="backend",
                level=level,
                order_index=0,
            )
            # Skill stores level as string directly
            assert skill.level == level


# ==========================================
# EDUCATION BUSINESS RULES TESTS
# ==========================================


class TestEducationBusinessRules:
    """Tests for Education entity business rules."""

    def test_rb_e01_institution_is_required(self, profile_id, today):
        """RB-E01: Institution name is required."""
        with pytest.raises((EmptyFieldError, InvalidInstitutionError)):
            Education.create(
                profile_id=profile_id,
                institution="",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

    def test_rb_e01_institution_not_whitespace_only(self, profile_id, today):
        """RB-E01: Institution name cannot be whitespace only."""
        with pytest.raises((EmptyFieldError, InvalidInstitutionError)):
            Education.create(
                profile_id=profile_id,
                institution="   ",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

    def test_rb_e02_degree_is_required(self, profile_id, today):
        """RB-E02: Degree is required."""
        with pytest.raises(EmptyFieldError):
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense",
                degree="",
                field="Computer Science",
                start_date=today,
                order_index=0,
            )

    def test_rb_e03_field_is_required(self, profile_id, today):
        """RB-E03: Field of study is required."""
        with pytest.raises(EmptyFieldError):
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense",
                degree="Bachelor of Science",
                field="",
                start_date=today,
                order_index=0,
            )

    def test_rb_e05_end_date_must_be_after_start_date(
        self, profile_id, yesterday, today
    ):
        """RB-E05: End date must be after start date."""
        with pytest.raises(InvalidDateRangeError):
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                end_date=yesterday,
                order_index=0,
            )

    def test_rb_e05_end_date_cannot_equal_start_date(self, profile_id, today):
        """RB-E05: End date cannot equal start date."""
        with pytest.raises(InvalidDateRangeError):
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                end_date=today,
                order_index=0,
            )

    def test_rb_e05_valid_date_range_accepted(self, profile_id, yesterday, tomorrow):
        """RB-E05: Valid date range is accepted."""
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=yesterday,
            end_date=tomorrow,
            order_index=0,
        )

        assert education.start_date == yesterday
        assert education.end_date == tomorrow


# ==========================================
# CONTACT MESSAGE BUSINESS RULES TESTS
# ==========================================


class TestContactMessageBusinessRules:
    """Tests for ContactMessage entity business rules."""

    def test_rb_cm01_name_is_required(self, valid_email):
        """RB-CM01: Contact message name is required."""
        with pytest.raises((EmptyFieldError, InvalidNameError)):
            ContactMessage.create(
                name="",
                email=valid_email,
                message="This is a test message with enough characters",
            )

    def test_rb_cm01_name_not_whitespace_only(self, valid_email):
        """RB-CM01: Contact message name cannot be whitespace only."""
        with pytest.raises((EmptyFieldError, InvalidNameError)):
            ContactMessage.create(
                name="   ",
                email=valid_email,
                message="This is a test message with enough characters",
            )

    def test_rb_cm02_email_is_required(self):
        """RB-CM02: Contact message email is required."""
        with pytest.raises(EmptyFieldError):
            ContactMessage.create(
                name="John Doe",
                email="",
                message="This is a test message with enough characters",
            )

    def test_rb_cm02_email_must_be_valid_format(self):
        """RB-CM02: Contact message email must be valid format."""
        with pytest.raises(InvalidEmailError):
            ContactMessage.create(
                name="John Doe",
                email="invalid-email",
                message="This is a test message with enough characters",
            )

    def test_rb_cm02_valid_email_accepted(self):
        """RB-CM02: Valid email is accepted."""
        message = ContactMessage.create(
            name="John Doe",
            email="test@example.com",
            message="This is a test message with enough characters",
        )

        assert message.email == "test@example.com"

    def test_rb_cm03_message_is_required(self, valid_email):
        """RB-CM03: Contact message content is required."""
        with pytest.raises(EmptyFieldError):
            ContactMessage.create(name="John Doe", email=valid_email, message="")

    def test_rb_cm03_message_min_length_enforced(self, valid_email):
        """RB-CM03: Contact message has minimum length of 10 characters."""
        with pytest.raises(InvalidLengthError):
            ContactMessage.create(name="John Doe", email=valid_email, message="Short")

    def test_rb_cm03_message_max_length_enforced(self, valid_email):
        """RB-CM03: Contact message has maximum length of 2000 characters."""
        long_message = "x" * 2001

        with pytest.raises(InvalidLengthError):
            ContactMessage.create(
                name="John Doe", email=valid_email, message=long_message
            )

    def test_rb_cm03_valid_message_length_accepted(self, valid_email):
        """RB-CM03: Message within valid length range is accepted."""
        message = ContactMessage.create(
            name="John Doe",
            email=valid_email,
            message="This is a valid message with enough characters to pass validation",
        )

        assert len(message.message) >= 10
        assert len(message.message) <= 2000


# ==========================================
# VALUE OBJECT BUSINESS RULES TESTS
# ==========================================


class TestValueObjectBusinessRules:
    """Tests for Value Object business rules."""

    def test_vr_e01_email_format_validated(self):
        """VR-E01: Email value object validates format."""
        with pytest.raises(InvalidEmailError):
            Email.create("invalid-email")

    def test_vr_e01_valid_email_accepted(self):
        """VR-E01: Valid email format is accepted."""
        email = Email.create("test@example.com")

        assert email.value == "test@example.com"

    def test_vr_e01_email_variations_accepted(self):
        """VR-E01: Various valid email formats are accepted."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user123@subdomain.example.com",
        ]

        for email_str in valid_emails:
            email = Email.create(email_str)
            assert email.value == email_str

    def test_vr_p01_phone_format_validated(self):
        """VR-P01: Phone value object validates E.164 format."""
        with pytest.raises(InvalidPhoneError):
            Phone.create("abc")

    def test_vr_p01_phone_without_plus_rejected(self):
        """VR-P01: Phone without + prefix is rejected."""
        with pytest.raises(InvalidPhoneError):
            Phone.create("34612345678")

    def test_vr_p01_valid_phone_accepted(self):
        """VR-P01: Valid E.164 phone format is accepted."""
        phone = Phone.create("+34612345678")

        assert phone.value == "+34612345678"

    def test_vr_sl01_skill_level_validated(self):
        """VR-SL01: SkillLevel validates against allowed values."""
        with pytest.raises(InvalidSkillLevelError):
            SkillLevel.create("invalid")

    def test_vr_sl01_valid_skill_levels_accepted(self):
        """VR-SL01: All valid skill levels are accepted."""
        valid_levels = ["basic", "intermediate", "advanced", "expert"]

        for level_str in valid_levels:
            level = SkillLevel.create(level_str)
            assert level.to_string() == level_str

    def test_vr_dr01_start_date_required(self):
        """VR-DR01: DateRange requires start date."""
        # DateRange.ongoing always needs a start date
        start = datetime.now()
        date_range = DateRange.ongoing(start)

        assert date_range.start_date == start

    def test_vr_dr02_end_date_must_be_after_start(self):
        """VR-DR02: DateRange end date must be after start date."""
        start = datetime(2023, 1, 1)
        end = datetime(2022, 1, 1)

        with pytest.raises(InvalidDateRangeError):
            DateRange.completed(start_date=start, end_date=end)

    def test_vr_dr02_end_date_cannot_equal_start(self):
        """VR-DR02: DateRange end date cannot equal start date."""
        same_date = datetime(2023, 1, 1)

        with pytest.raises(InvalidDateRangeError):
            DateRange.completed(start_date=same_date, end_date=same_date)

    def test_vr_dr02_valid_date_range_accepted(self):
        """VR-DR02: Valid date range is accepted."""
        start = datetime(2022, 1, 1)
        end = datetime(2023, 1, 1)

        date_range = DateRange.completed(start_date=start, end_date=end)

        assert date_range.start_date == start
        assert date_range.end_date == end


# ==========================================
# IMMUTABILITY CONSTRAINTS TESTS
# ==========================================


class TestImmutabilityConstraints:
    """Tests for immutability constraints on value objects."""

    def test_email_is_immutable(self):
        """Email value object should be immutable."""
        email = Email.create("test@example.com")

        with pytest.raises(AttributeError):
            email.value = "new@example.com"

    def test_phone_is_immutable(self):
        """Phone value object should be immutable."""
        phone = Phone.create("+34612345678")

        with pytest.raises(AttributeError):
            phone.value = "+15551234567"

    def test_skill_level_is_immutable(self):
        """SkillLevel value object should be immutable."""
        level = SkillLevel.create("basic")

        with pytest.raises(AttributeError):
            level.level = SkillLevel.create("expert").level

    def test_date_range_is_immutable(self):
        """DateRange value object should be immutable."""
        date_range = DateRange.ongoing(datetime.now())

        with pytest.raises(AttributeError):
            date_range.start_date = datetime.now()

    def test_date_range_end_date_immutable(self):
        """DateRange end_date should be immutable."""
        start = datetime(2022, 1, 1)
        end = datetime(2023, 1, 1)
        date_range = DateRange.completed(start_date=start, end_date=end)

        with pytest.raises(AttributeError):
            date_range.end_date = datetime(2024, 1, 1)


# ==========================================
# CROSS-CUTTING CONCERNS TESTS
# ==========================================


class TestCrossCuttingBusinessRules:
    """Tests for cross-cutting business rules."""

    def test_order_index_cannot_be_negative_skill(self, profile_id):
        """Order index must be non-negative for Skill."""
        with pytest.raises(InvalidOrderIndexError):
            Skill.create(
                profile_id=profile_id, name="Python", category="backend", order_index=-1
            )

    def test_order_index_cannot_be_negative_education(self, profile_id, today):
        """Order index must be non-negative for Education."""
        with pytest.raises(InvalidOrderIndexError):
            Education.create(
                profile_id=profile_id,
                institution="Universidad Complutense",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date=today,
                order_index=-1,
            )

    def test_order_index_cannot_be_negative_work_experience(self, profile_id, today):
        """Order index must be non-negative for WorkExperience."""
        with pytest.raises(InvalidOrderIndexError):
            WorkExperience.create(
                profile_id=profile_id,
                role="Software Engineer",
                company="Test Company",
                start_date=today,
                order_index=-1,
            )

    def test_order_index_zero_is_valid(self, profile_id):
        """Order index of 0 should be valid (first position)."""
        skill = Skill.create(
            profile_id=profile_id, name="Python", category="backend", order_index=0
        )

        assert skill.order_index == 0


# ==========================================
# INTEGRATION TESTS
# ==========================================


class TestBusinessRulesIntegration:
    """Integration tests for business rules working together."""

    def test_profile_with_all_valid_fields(self):
        """Should create profile with all valid fields."""
        profile = Profile.create(
            name="John Doe",
            headline="Senior Software Engineer",
            bio="Experienced developer",
            location="Madrid, Spain",
            avatar_url="https://example.com/avatar.jpg",
        )

        assert profile.name == "John Doe"
        assert profile.headline == "Senior Software Engineer"
        assert profile.bio == "Experienced developer"
        assert profile.location == "Madrid, Spain"
        assert profile.avatar_url == "https://example.com/avatar.jpg"

    def test_complete_work_experience_lifecycle(self, profile_id):
        """Should create and update work experience following all rules."""
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        # Create
        experience = WorkExperience.create(
            profile_id=profile_id,
            role="Software Engineer",
            company="Tech Corp",
            start_date=yesterday,
            end_date=tomorrow,
            order_index=0,
        )

        assert experience.role == "Software Engineer"
        assert experience.company == "Tech Corp"

        # Update
        experience.update_info(role="Senior Software Engineer")
        assert experience.role == "Senior Software Engineer"

    def test_complete_education_lifecycle(self, profile_id):
        """Should create and update education following all rules."""
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        # Create
        education = Education.create(
            profile_id=profile_id,
            institution="Universidad Complutense",
            degree="Bachelor of Science",
            field="Computer Science",
            start_date=yesterday,
            end_date=tomorrow,
            order_index=0,
        )

        assert education.institution == "Universidad Complutense"
        assert education.degree == "Bachelor of Science"

        # Update
        education.update_info(degree="Master of Science")
        assert education.degree == "Master of Science"

    def test_contact_message_complete_flow(self):
        """Should create and manage contact message following all rules."""
        message = ContactMessage.create(
            name="John Doe",
            email="john@example.com",
            message="This is a valid message with enough characters to pass all validation",
        )

        assert message.status == "pending"
        assert message.is_pending()

        message.mark_as_read()
        assert message.status == "read"
        assert message.is_read()

        message.mark_as_replied()
        assert message.status == "replied"
        assert message.is_replied()
