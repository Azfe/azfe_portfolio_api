"""Tests for ContactInformation Entity."""

import pytest

from app.domain.entities.contact_information import ContactInformation
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidEmailError,
    InvalidPhoneError,
    InvalidURLError,
)


@pytest.mark.entity
class TestContactInformationCreation:
    """Test ContactInformation creation."""

    def test_create_with_required_fields(self, profile_id):
        ci = ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
        )
        assert ci.email == "test@example.com"
        assert ci.phone is None
        assert ci.linkedin is None
        assert ci.github is None
        assert ci.website is None

    def test_create_with_all_fields(self, profile_id):
        ci = ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
            phone="+34612345678",
            linkedin="https://linkedin.com/in/user",
            github="https://github.com/user",
            website="https://example.com",
        )
        assert ci.phone == "+34612345678"
        assert ci.linkedin == "https://linkedin.com/in/user"
        assert ci.github == "https://github.com/user"
        assert ci.website == "https://example.com"


@pytest.mark.entity
@pytest.mark.business_rule
class TestContactInformationValidation:
    """Test ContactInformation validation rules."""

    def test_empty_email_raises_error(self, profile_id):
        with pytest.raises(EmptyFieldError):
            ContactInformation.create(
                profile_id=profile_id,
                email="",
            )

    def test_invalid_email_raises_error(self, profile_id):
        with pytest.raises(InvalidEmailError):
            ContactInformation.create(
                profile_id=profile_id,
                email="not-an-email",
            )

    def test_invalid_phone_raises_error(self, profile_id):
        with pytest.raises(InvalidPhoneError):
            ContactInformation.create(
                profile_id=profile_id,
                email="test@example.com",
                phone="abc",
            )

    def test_empty_phone_becomes_none(self, profile_id):
        ci = ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
            phone="   ",
        )
        assert ci.phone is None

    def test_phone_with_separators_is_valid(self, profile_id):
        ci = ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
            phone="+34 612 345 678",
        )
        assert ci.phone == "+34 612 345 678"

    def test_invalid_linkedin_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            ContactInformation.create(
                profile_id=profile_id,
                email="test@example.com",
                linkedin="not-a-url",
            )

    def test_invalid_github_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            ContactInformation.create(
                profile_id=profile_id,
                email="test@example.com",
                github="ftp://github.com",
            )

    def test_invalid_website_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            ContactInformation.create(
                profile_id=profile_id,
                email="test@example.com",
                website="not-valid",
            )

    def test_empty_linkedin_becomes_none(self, profile_id):
        ci = ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
            linkedin="   ",
        )
        assert ci.linkedin is None

    def test_empty_github_becomes_none(self, profile_id):
        ci = ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
            github="   ",
        )
        assert ci.github is None

    def test_empty_website_becomes_none(self, profile_id):
        ci = ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
            website="   ",
        )
        assert ci.website is None

    def test_empty_profile_id_raises_error(self):
        with pytest.raises(EmptyFieldError):
            ContactInformation.create(
                profile_id="",
                email="test@example.com",
            )


@pytest.mark.entity
class TestContactInformationUpdate:
    """Test ContactInformation updates."""

    def _make(self, profile_id):
        return ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
        )

    def test_update_email(self, profile_id):
        ci = self._make(profile_id)
        ci.update_email("new@example.com")
        assert ci.email == "new@example.com"

    def test_update_email_invalid_raises(self, profile_id):
        ci = self._make(profile_id)
        with pytest.raises(InvalidEmailError):
            ci.update_email("bad-email")

    def test_update_phone(self, profile_id):
        ci = self._make(profile_id)
        ci.update_phone("+34612345678")
        assert ci.phone == "+34612345678"

    def test_update_phone_to_none(self, profile_id):
        ci = ContactInformation.create(
            profile_id=profile_id,
            email="test@example.com",
            phone="+34612345678",
        )
        ci.update_phone(None)
        assert ci.phone is None

    def test_update_social_links(self, profile_id):
        ci = self._make(profile_id)
        ci.update_social_links(
            linkedin="https://linkedin.com/in/user",
            github="https://github.com/user",
            website="https://example.com",
        )
        assert ci.linkedin == "https://linkedin.com/in/user"
        assert ci.github == "https://github.com/user"
        assert ci.website == "https://example.com"

    def test_update_social_links_invalid_raises(self, profile_id):
        ci = self._make(profile_id)
        with pytest.raises(InvalidURLError):
            ci.update_social_links(linkedin="bad-url")
