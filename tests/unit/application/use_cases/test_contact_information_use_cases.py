"""Tests for ContactInformation use cases."""

from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    ContactInformationResponse,
    CreateContactInformationRequest,
    DeleteContactInformationRequest,
    GetContactInformationRequest,
    UpdateContactInformationRequest,
)
from app.application.use_cases.contact_information.create_contact_information import (
    CreateContactInformationUseCase,
)
from app.application.use_cases.contact_information.delete_contact_information import (
    DeleteContactInformationUseCase,
)
from app.application.use_cases.contact_information.get_contact_information import (
    GetContactInformationUseCase,
)
from app.application.use_cases.contact_information.update_contact_information import (
    UpdateContactInformationUseCase,
)
from app.domain.entities.contact_information import ContactInformation
from app.domain.exceptions import InvalidEmailError, InvalidPhoneError, InvalidURLError
from app.shared.shared_exceptions import DuplicateException, NotFoundException

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"


def _make_contact_info(**overrides) -> ContactInformation:
    defaults = {
        "profile_id": PROFILE_ID,
        "email": "alex@example.com",
        "phone": None,
        "linkedin": None,
        "github": None,
        "website": None,
    }
    defaults.update(overrides)
    return ContactInformation.create(**defaults)


# ---------------------------------------------------------------------------
# CreateContactInformationUseCase
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCreateContactInformationUseCase:
    async def test_create_success(self):
        repo = AsyncMock()
        contact_info = _make_contact_info()
        repo.find_by.return_value = []
        repo.add.return_value = contact_info

        uc = CreateContactInformationUseCase(repo)
        request = CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="alex@example.com",
        )
        result = await uc.execute(request)

        assert isinstance(result, ContactInformationResponse)
        assert result.email == "alex@example.com"
        assert result.profile_id == PROFILE_ID
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)
        repo.add.assert_awaited_once()

    async def test_create_with_all_optional_fields(self):
        repo = AsyncMock()
        contact_info = _make_contact_info(
            phone="+34600000000",
            linkedin="https://linkedin.com/in/alex",
            github="https://github.com/alex",
            website="https://azfe.dev",
        )
        repo.find_by.return_value = []
        repo.add.return_value = contact_info

        uc = CreateContactInformationUseCase(repo)
        request = CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="alex@example.com",
            phone="+34600000000",
            linkedin="https://linkedin.com/in/alex",
            github="https://github.com/alex",
            website="https://azfe.dev",
        )
        result = await uc.execute(request)

        assert result.phone == "+34600000000"
        assert result.linkedin == "https://linkedin.com/in/alex"
        assert result.github == "https://github.com/alex"
        assert result.website == "https://azfe.dev"
        repo.add.assert_awaited_once()

    async def test_create_returns_full_response_dto(self):
        repo = AsyncMock()
        contact_info = _make_contact_info()
        repo.find_by.return_value = []
        repo.add.return_value = contact_info

        uc = CreateContactInformationUseCase(repo)
        request = CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="alex@example.com",
        )
        result = await uc.execute(request)

        assert result.id == contact_info.id
        assert result.created_at == contact_info.created_at
        assert result.updated_at == contact_info.updated_at
        assert result.phone is None
        assert result.linkedin is None
        assert result.github is None
        assert result.website is None

    async def test_create_duplicate_raises(self):
        repo = AsyncMock()
        existing = _make_contact_info()
        repo.find_by.return_value = [existing]

        uc = CreateContactInformationUseCase(repo)
        request = CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="alex@example.com",
        )
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    async def test_create_checks_existence_before_add(self):
        repo = AsyncMock()
        existing = _make_contact_info()
        repo.find_by.return_value = [existing]

        uc = CreateContactInformationUseCase(repo)
        request = CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="alex@example.com",
        )
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    async def test_create_invalid_email_raises_domain_error(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = CreateContactInformationUseCase(repo)
        request = CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="not-an-email",
        )
        with pytest.raises(InvalidEmailError):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    async def test_create_invalid_phone_raises_domain_error(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = CreateContactInformationUseCase(repo)
        request = CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="alex@example.com",
            phone="not-a-phone",
        )
        with pytest.raises(InvalidPhoneError):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    async def test_create_invalid_linkedin_url_raises_domain_error(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = CreateContactInformationUseCase(repo)
        request = CreateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="alex@example.com",
            linkedin="not-a-url",
        )
        with pytest.raises(InvalidURLError):
            await uc.execute(request)

        repo.add.assert_not_awaited()


# ---------------------------------------------------------------------------
# GetContactInformationUseCase
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetContactInformationUseCase:
    async def test_get_success(self):
        repo = AsyncMock()
        contact_info = _make_contact_info()
        repo.find_by.return_value = [contact_info]

        uc = GetContactInformationUseCase(repo)
        request = GetContactInformationRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert isinstance(result, ContactInformationResponse)
        assert result.email == "alex@example.com"
        assert result.profile_id == PROFILE_ID
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    async def test_get_returns_full_response_dto(self):
        repo = AsyncMock()
        contact_info = _make_contact_info(
            phone="+34600000000",
            linkedin="https://linkedin.com/in/alex",
            github="https://github.com/alex",
            website="https://azfe.dev",
        )
        repo.find_by.return_value = [contact_info]

        uc = GetContactInformationUseCase(repo)
        request = GetContactInformationRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.id == contact_info.id
        assert result.phone == "+34600000000"
        assert result.linkedin == "https://linkedin.com/in/alex"
        assert result.github == "https://github.com/alex"
        assert result.website == "https://azfe.dev"
        assert result.created_at == contact_info.created_at
        assert result.updated_at == contact_info.updated_at

    async def test_get_not_found_raises(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = GetContactInformationUseCase(repo)
        request = GetContactInformationRequest(profile_id=PROFILE_ID)
        with pytest.raises(NotFoundException):
            await uc.execute(request)

    async def test_get_calls_repo_find_by_profile_id(self):
        repo = AsyncMock()
        repo.find_by.return_value = [_make_contact_info()]

        uc = GetContactInformationUseCase(repo)
        await uc.execute(GetContactInformationRequest(profile_id=PROFILE_ID))

        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)


# ---------------------------------------------------------------------------
# UpdateContactInformationUseCase
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestUpdateContactInformationUseCase:
    async def test_update_all_fields(self):
        repo = AsyncMock()
        original = _make_contact_info()
        updated = _make_contact_info(
            email="new@example.com",
            phone="+34600000001",
            linkedin="https://linkedin.com/in/alexnew",
            github="https://github.com/alexnew",
            website="https://new.azfe.dev",
        )
        repo.find_by.return_value = [original]
        repo.update.return_value = updated

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="new@example.com",
            phone="+34600000001",
            linkedin="https://linkedin.com/in/alexnew",
            github="https://github.com/alexnew",
            website="https://new.azfe.dev",
        )
        result = await uc.execute(request)

        assert result.email == "new@example.com"
        assert result.phone == "+34600000001"
        assert result.linkedin == "https://linkedin.com/in/alexnew"
        assert result.github == "https://github.com/alexnew"
        assert result.website == "https://new.azfe.dev"
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)
        repo.update.assert_awaited_once()

    async def test_update_only_email(self):
        """Partial update: only email is changed; phone and links remain unchanged."""
        repo = AsyncMock()
        original = _make_contact_info(
            phone="+34600000000",
            linkedin="https://linkedin.com/in/alex",
        )
        # After partial update the entity returned by the repo reflects new email
        updated = _make_contact_info(
            email="updated@example.com",
            phone="+34600000000",
            linkedin="https://linkedin.com/in/alex",
        )
        repo.find_by.return_value = [original]
        repo.update.return_value = updated

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="updated@example.com",
        )
        result = await uc.execute(request)

        assert result.email == "updated@example.com"
        # Unchanged fields preserved from mock return value
        assert result.phone == "+34600000000"
        assert result.linkedin == "https://linkedin.com/in/alex"
        repo.update.assert_awaited_once()

    async def test_update_only_phone(self):
        """Partial update: only phone is changed; email and links remain unchanged."""
        repo = AsyncMock()
        original = _make_contact_info(linkedin="https://linkedin.com/in/alex")
        updated = _make_contact_info(
            phone="+34699999999",
            linkedin="https://linkedin.com/in/alex",
        )
        repo.find_by.return_value = [original]
        repo.update.return_value = updated

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            phone="+34699999999",
        )
        result = await uc.execute(request)

        assert result.phone == "+34699999999"
        assert result.email == "alex@example.com"
        assert result.linkedin == "https://linkedin.com/in/alex"
        repo.update.assert_awaited_once()

    async def test_update_only_social_links(self):
        """Partial update: only social links are changed; email and phone remain unchanged."""
        repo = AsyncMock()
        original = _make_contact_info(phone="+34600000000")
        updated = _make_contact_info(
            phone="+34600000000",
            linkedin="https://linkedin.com/in/alexnew",
            github="https://github.com/alexnew",
            website="https://azfe.dev",
        )
        repo.find_by.return_value = [original]
        repo.update.return_value = updated

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            linkedin="https://linkedin.com/in/alexnew",
            github="https://github.com/alexnew",
            website="https://azfe.dev",
        )
        result = await uc.execute(request)

        assert result.linkedin == "https://linkedin.com/in/alexnew"
        assert result.github == "https://github.com/alexnew"
        assert result.website == "https://azfe.dev"
        assert result.email == "alex@example.com"
        assert result.phone == "+34600000000"
        repo.update.assert_awaited_once()

    async def test_update_only_linkedin(self):
        """Partial update: only linkedin is provided; github and website remain None."""
        repo = AsyncMock()
        original = _make_contact_info()
        updated = _make_contact_info(linkedin="https://linkedin.com/in/alex")
        repo.find_by.return_value = [original]
        repo.update.return_value = updated

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            linkedin="https://linkedin.com/in/alex",
        )
        result = await uc.execute(request)

        assert result.linkedin == "https://linkedin.com/in/alex"
        assert result.github is None
        assert result.website is None
        repo.update.assert_awaited_once()

    async def test_update_not_found_raises(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="new@example.com",
        )
        with pytest.raises(NotFoundException):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    async def test_update_no_fields_still_persists(self):
        """When no fields are provided the entity is still persisted unchanged."""
        repo = AsyncMock()
        original = _make_contact_info()
        repo.find_by.return_value = [original]
        repo.update.return_value = original

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.email == "alex@example.com"
        repo.update.assert_awaited_once()

    async def test_update_invalid_email_raises_domain_error(self):
        repo = AsyncMock()
        repo.find_by.return_value = [_make_contact_info()]

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            email="not-an-email",
        )
        with pytest.raises(InvalidEmailError):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    async def test_update_invalid_phone_raises_domain_error(self):
        repo = AsyncMock()
        repo.find_by.return_value = [_make_contact_info()]

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            phone="not-a-phone",
        )
        with pytest.raises(InvalidPhoneError):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    async def test_update_invalid_github_url_raises_domain_error(self):
        repo = AsyncMock()
        repo.find_by.return_value = [_make_contact_info()]

        uc = UpdateContactInformationUseCase(repo)
        request = UpdateContactInformationRequest(
            profile_id=PROFILE_ID,
            github="ftp://not-allowed",
        )
        with pytest.raises(InvalidURLError):
            await uc.execute(request)

        repo.update.assert_not_awaited()


# ---------------------------------------------------------------------------
# DeleteContactInformationUseCase
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestDeleteContactInformationUseCase:
    async def test_delete_success(self):
        repo = AsyncMock()
        contact_info = _make_contact_info()
        repo.find_by.return_value = [contact_info]

        uc = DeleteContactInformationUseCase(repo)
        request = DeleteContactInformationRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.message == "Contact information deleted successfully"
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)
        repo.delete.assert_awaited_once_with(contact_info.id)

    async def test_delete_not_found_raises(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = DeleteContactInformationUseCase(repo)
        request = DeleteContactInformationRequest(profile_id=PROFILE_ID)
        with pytest.raises(NotFoundException):
            await uc.execute(request)

        repo.delete.assert_not_awaited()

    async def test_delete_checks_existence_before_deleting(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = DeleteContactInformationUseCase(repo)
        request = DeleteContactInformationRequest(profile_id=PROFILE_ID)
        with pytest.raises(NotFoundException):
            await uc.execute(request)

        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    async def test_delete_calls_repo_delete_with_entity_id(self):
        repo = AsyncMock()
        contact_info = _make_contact_info()
        repo.find_by.return_value = [contact_info]

        uc = DeleteContactInformationUseCase(repo)
        request = DeleteContactInformationRequest(profile_id=PROFILE_ID)
        await uc.execute(request)

        repo.delete.assert_awaited_once_with(contact_info.id)
