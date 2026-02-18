"""Tests for ContactInfo Value Object."""

import pytest

from app.domain.exceptions import InvalidEmailError, InvalidPhoneError
from app.domain.value_objects.contact_info import ContactInfo
from app.domain.value_objects.email import Email
from app.domain.value_objects.phone import Phone


@pytest.mark.value_object
class TestContactInfoCreation:
    """Test ContactInfo creation."""

    def test_create_with_email_only(self):
        info = ContactInfo.create(email="test@example.com")

        assert info.get_email_value() == "test@example.com"
        assert info.phone is None

    def test_create_with_email_and_phone(self):
        info = ContactInfo.create(email="test@example.com", phone="+34612345678")

        assert info.get_email_value() == "test@example.com"
        assert info.get_phone_value() == "+34612345678"

    def test_email_only_factory(self):
        info = ContactInfo.email_only("test@example.com")

        assert info.get_email_value() == "test@example.com"
        assert info.phone is None

    def test_from_value_objects(self):
        email_vo = Email.create("test@example.com")
        phone_vo = Phone.create("+34612345678")
        info = ContactInfo.from_value_objects(email=email_vo, phone=phone_vo)

        assert info.email == email_vo
        assert info.phone == phone_vo

    def test_from_value_objects_without_phone(self):
        email_vo = Email.create("test@example.com")
        info = ContactInfo.from_value_objects(email=email_vo)

        assert info.email == email_vo
        assert info.phone is None


@pytest.mark.value_object
class TestContactInfoValidation:
    """Test ContactInfo validation."""

    def test_invalid_email_raises_error(self):
        with pytest.raises(InvalidEmailError):
            ContactInfo.create(email="not-an-email")

    def test_invalid_phone_raises_error(self):
        with pytest.raises(InvalidPhoneError):
            ContactInfo.create(email="test@example.com", phone="invalid")


@pytest.mark.value_object
class TestContactInfoQueries:
    """Test ContactInfo query methods."""

    def test_has_phone_true(self):
        info = ContactInfo.create(email="test@example.com", phone="+34612345678")
        assert info.has_phone() is True

    def test_has_phone_false(self):
        info = ContactInfo.create(email="test@example.com")
        assert info.has_phone() is False

    def test_get_email_value(self):
        info = ContactInfo.create(email="TEST@example.com")
        assert info.get_email_value() == "test@example.com"

    def test_get_phone_value_present(self):
        info = ContactInfo.create(email="test@example.com", phone="+34612345678")
        assert info.get_phone_value() == "+34612345678"

    def test_get_phone_value_none(self):
        info = ContactInfo.create(email="test@example.com")
        assert info.get_phone_value() is None


@pytest.mark.value_object
class TestContactInfoTransformations:
    """Test ContactInfo transformation methods (immutable copies)."""

    def test_with_phone(self):
        info = ContactInfo.create(email="test@example.com")
        new_info = info.with_phone("+34612345678")

        assert info.has_phone() is False
        assert new_info.has_phone() is True
        assert new_info.get_phone_value() == "+34612345678"
        assert new_info.get_email_value() == "test@example.com"

    def test_without_phone(self):
        info = ContactInfo.create(email="test@example.com", phone="+34612345678")
        new_info = info.without_phone()

        assert info.has_phone() is True
        assert new_info.has_phone() is False
        assert new_info.get_email_value() == "test@example.com"

    def test_with_email(self):
        info = ContactInfo.create(email="old@example.com", phone="+34612345678")
        new_info = info.with_email("new@example.com")

        assert info.get_email_value() == "old@example.com"
        assert new_info.get_email_value() == "new@example.com"
        assert new_info.get_phone_value() == "+34612345678"

    def test_with_phone_invalid_raises(self):
        info = ContactInfo.create(email="test@example.com")
        with pytest.raises(InvalidPhoneError):
            info.with_phone("invalid")

    def test_with_email_invalid_raises(self):
        info = ContactInfo.create(email="test@example.com")
        with pytest.raises(InvalidEmailError):
            info.with_email("not-an-email")


@pytest.mark.value_object
class TestContactInfoEquality:
    """Test ContactInfo equality and hash."""

    def test_equal_with_same_email_and_phone(self):
        info1 = ContactInfo.create(email="test@example.com", phone="+34612345678")
        info2 = ContactInfo.create(email="test@example.com", phone="+34612345678")
        assert info1 == info2

    def test_equal_email_only(self):
        info1 = ContactInfo.create(email="test@example.com")
        info2 = ContactInfo.create(email="test@example.com")
        assert info1 == info2

    def test_not_equal_different_email(self):
        info1 = ContactInfo.create(email="a@example.com")
        info2 = ContactInfo.create(email="b@example.com")
        assert info1 != info2

    def test_not_equal_different_phone(self):
        info1 = ContactInfo.create(email="test@example.com", phone="+34612345678")
        info2 = ContactInfo.create(email="test@example.com", phone="+15551234567")
        assert info1 != info2

    def test_not_equal_to_other_type(self):
        info = ContactInfo.create(email="test@example.com")
        assert info != "test@example.com"

    def test_hash_same_for_equal(self):
        info1 = ContactInfo.create(email="test@example.com", phone="+34612345678")
        info2 = ContactInfo.create(email="test@example.com", phone="+34612345678")
        assert hash(info1) == hash(info2)

    def test_usable_in_set(self):
        info1 = ContactInfo.create(email="test@example.com")
        info2 = ContactInfo.create(email="test@example.com")
        info3 = ContactInfo.create(email="other@example.com")
        assert len({info1, info2, info3}) == 2


@pytest.mark.value_object
class TestContactInfoStringRepresentations:
    """Test ContactInfo string representations."""

    def test_str_with_phone(self):
        info = ContactInfo.create(email="test@example.com", phone="+34612345678")
        result = str(info)
        assert "Email:" in result
        assert "Phone:" in result

    def test_str_without_phone(self):
        info = ContactInfo.create(email="test@example.com")
        result = str(info)
        assert "Email:" in result
        assert "Phone:" not in result

    def test_repr(self):
        info = ContactInfo.create(email="test@example.com")
        result = repr(info)
        assert "ContactInfo" in result
