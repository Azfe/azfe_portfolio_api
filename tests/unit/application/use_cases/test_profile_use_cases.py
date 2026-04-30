"""Tests for Profile use cases."""

from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    CreateProfileRequest,
    GetProfileRequest,
    UpdateProfileRequest,
)
from app.application.use_cases.profile.create_profile import CreateProfileUseCase
from app.application.use_cases.profile.get_profile import GetProfileUseCase
from app.application.use_cases.profile.update_profile import UpdateProfileUseCase
from app.domain.entities.profile import Profile
from app.domain.exceptions import EmptyFieldError, InvalidLengthError, InvalidURLError
from app.shared.shared_exceptions import DuplicateException, NotFoundException

pytestmark = pytest.mark.asyncio


def _make_profile(**overrides):
    defaults = {"name": "Alex Zapata", "headline": "Backend Developer"}
    defaults.update(overrides)
    return Profile.create(**defaults)


# ---------------------------------------------------------------------------
# CreateProfileUseCase
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCreateProfileUseCase:
    async def test_create_profile_success(self):
        repo = AsyncMock()
        profile = _make_profile()
        repo.profile_exists.return_value = False
        repo.add.return_value = profile

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(name="Alex Zapata", headline="Backend Developer")
        result = await uc.execute(request)

        assert result.name == "Alex Zapata"
        assert result.headline == "Backend Developer"
        repo.profile_exists.assert_awaited_once()
        repo.add.assert_awaited_once()

    async def test_create_profile_with_all_optional_fields(self):
        repo = AsyncMock()
        profile = _make_profile(
            bio="Python dev with 10 years of experience.",
            location="Barcelona, Spain",
            avatar_url="https://example.com/avatar.png",
        )
        repo.profile_exists.return_value = False
        repo.add.return_value = profile

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(
            name="Alex Zapata",
            headline="Backend Developer",
            bio="Python dev with 10 years of experience.",
            location="Barcelona, Spain",
            avatar_url="https://example.com/avatar.png",
        )
        result = await uc.execute(request)

        assert result.bio == "Python dev with 10 years of experience."
        assert result.location == "Barcelona, Spain"
        assert result.avatar_url == "https://example.com/avatar.png"
        repo.add.assert_awaited_once()

    async def test_create_profile_returns_full_response_dto(self):
        repo = AsyncMock()
        profile = _make_profile()
        repo.profile_exists.return_value = False
        repo.add.return_value = profile

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(name="Alex Zapata", headline="Backend Developer")
        result = await uc.execute(request)

        assert result.id == profile.id
        assert result.created_at == profile.created_at
        assert result.updated_at == profile.updated_at
        assert result.bio is None
        assert result.location is None
        assert result.avatar_url is None

    async def test_create_profile_duplicate_raises(self):
        repo = AsyncMock()
        repo.profile_exists.return_value = True

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(name="Alex Zapata", headline="Backend Developer")
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    async def test_create_profile_checks_existence_before_add(self):
        repo = AsyncMock()
        repo.profile_exists.return_value = True

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(name="Alex Zapata", headline="Backend Developer")
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.profile_exists.assert_awaited_once()

    async def test_create_profile_empty_name_raises_domain_error(self):
        repo = AsyncMock()
        repo.profile_exists.return_value = False

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(name="", headline="Backend Developer")
        with pytest.raises(EmptyFieldError):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    async def test_create_profile_empty_headline_raises_domain_error(self):
        repo = AsyncMock()
        repo.profile_exists.return_value = False

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(name="Alex Zapata", headline="")
        with pytest.raises(EmptyFieldError):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    async def test_create_profile_name_too_long_raises_domain_error(self):
        repo = AsyncMock()
        repo.profile_exists.return_value = False

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(
            name="A" * (Profile.MAX_NAME_LENGTH + 1),
            headline="Backend Developer",
        )
        with pytest.raises(InvalidLengthError):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    async def test_create_profile_headline_too_long_raises_domain_error(self):
        repo = AsyncMock()
        repo.profile_exists.return_value = False

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(
            name="Alex Zapata",
            headline="H" * (Profile.MAX_HEADLINE_LENGTH + 1),
        )
        with pytest.raises(InvalidLengthError):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    async def test_create_profile_invalid_avatar_url_raises_domain_error(self):
        repo = AsyncMock()
        repo.profile_exists.return_value = False

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(
            name="Alex Zapata",
            headline="Backend Developer",
            avatar_url="not-a-valid-url",
        )
        with pytest.raises(InvalidURLError):
            await uc.execute(request)

        repo.add.assert_not_awaited()


# ---------------------------------------------------------------------------
# GetProfileUseCase
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetProfileUseCase:
    async def test_get_profile_success(self):
        repo = AsyncMock()
        profile = _make_profile()
        repo.get_profile.return_value = profile

        uc = GetProfileUseCase(repo)
        result = await uc.execute(GetProfileRequest())

        assert result.name == "Alex Zapata"
        assert result.headline == "Backend Developer"
        repo.get_profile.assert_awaited_once()

    async def test_get_profile_returns_full_response_dto(self):
        repo = AsyncMock()
        profile = _make_profile(
            bio="Experienced dev",
            location="Barcelona",
            avatar_url="https://example.com/pic.jpg",
        )
        repo.get_profile.return_value = profile

        uc = GetProfileUseCase(repo)
        result = await uc.execute(GetProfileRequest())

        assert result.id == profile.id
        assert result.bio == "Experienced dev"
        assert result.location == "Barcelona"
        assert result.avatar_url == "https://example.com/pic.jpg"
        assert result.created_at == profile.created_at
        assert result.updated_at == profile.updated_at

    async def test_get_profile_not_found_raises(self):
        repo = AsyncMock()
        repo.get_profile.return_value = None

        uc = GetProfileUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(GetProfileRequest())

    async def test_get_profile_calls_repo_get_profile(self):
        repo = AsyncMock()
        repo.get_profile.return_value = _make_profile()

        uc = GetProfileUseCase(repo)
        await uc.execute(GetProfileRequest())

        repo.get_profile.assert_awaited_once()


# ---------------------------------------------------------------------------
# UpdateProfileUseCase
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestUpdateProfileUseCase:
    async def test_update_profile_name_success(self):
        repo = AsyncMock()
        original = _make_profile()
        updated = _make_profile(name="Updated Alex")
        repo.get_profile.return_value = original
        repo.update.return_value = updated

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(name="Updated Alex")
        result = await uc.execute(request)

        assert result.name == "Updated Alex"
        repo.get_profile.assert_awaited_once()
        repo.update.assert_awaited_once()

    async def test_update_profile_headline_success(self):
        repo = AsyncMock()
        original = _make_profile()
        updated = _make_profile(headline="Senior Backend Developer")
        repo.get_profile.return_value = original
        repo.update.return_value = updated

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(headline="Senior Backend Developer")
        result = await uc.execute(request)

        assert result.headline == "Senior Backend Developer"
        repo.update.assert_awaited_once()

    async def test_update_profile_bio_success(self):
        repo = AsyncMock()
        original = _make_profile()
        updated = _make_profile(bio="Updated bio text.")
        repo.get_profile.return_value = original
        repo.update.return_value = updated

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(bio="Updated bio text.")
        result = await uc.execute(request)

        assert result.bio == "Updated bio text."
        repo.update.assert_awaited_once()

    async def test_update_profile_location_success(self):
        repo = AsyncMock()
        original = _make_profile()
        updated = _make_profile(location="Madrid, Spain")
        repo.get_profile.return_value = original
        repo.update.return_value = updated

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(location="Madrid, Spain")
        result = await uc.execute(request)

        assert result.location == "Madrid, Spain"
        repo.update.assert_awaited_once()

    async def test_update_profile_avatar_success(self):
        repo = AsyncMock()
        original = _make_profile()
        updated = _make_profile(avatar_url="https://example.com/avatar.png")
        repo.get_profile.return_value = original
        repo.update.return_value = updated

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(avatar_url="https://example.com/avatar.png")
        result = await uc.execute(request)

        assert result.avatar_url == "https://example.com/avatar.png"
        repo.update.assert_awaited_once()

    async def test_update_profile_avatar_none_skips_avatar_update(self):
        """avatar_url=None in the request means 'do not change the avatar'."""
        repo = AsyncMock()
        original = _make_profile(avatar_url="https://example.com/old.png")
        repo.get_profile.return_value = original
        repo.update.return_value = original

        uc = UpdateProfileUseCase(repo)
        # Explicitly passing None means no avatar update — use case guards on
        # `if request.avatar_url is not None`, so the entity is not mutated.
        request = UpdateProfileRequest(avatar_url=None)
        result = await uc.execute(request)

        # The profile is still persisted (update is always called)
        repo.update.assert_awaited_once()
        # The original avatar is preserved because update_avatar was never called
        assert result.avatar_url == "https://example.com/old.png"

    async def test_update_profile_all_fields(self):
        repo = AsyncMock()
        original = _make_profile()
        updated = _make_profile(
            name="Alex Z.",
            headline="Full Stack Dev",
            bio="New bio.",
            location="Remote",
            avatar_url="https://example.com/new.png",
        )
        repo.get_profile.return_value = original
        repo.update.return_value = updated

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(
            name="Alex Z.",
            headline="Full Stack Dev",
            bio="New bio.",
            location="Remote",
            avatar_url="https://example.com/new.png",
        )
        result = await uc.execute(request)

        assert result.name == "Alex Z."
        assert result.headline == "Full Stack Dev"
        assert result.bio == "New bio."
        assert result.location == "Remote"
        assert result.avatar_url == "https://example.com/new.png"
        repo.update.assert_awaited_once()

    async def test_update_profile_not_found_raises(self):
        repo = AsyncMock()
        repo.get_profile.return_value = None

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(name="Updated")
        with pytest.raises(NotFoundException):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    async def test_update_profile_no_fields_still_persists(self):
        repo = AsyncMock()
        original = _make_profile()
        repo.get_profile.return_value = original
        repo.update.return_value = original

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest()
        result = await uc.execute(request)

        assert result.name == "Alex Zapata"
        repo.update.assert_awaited_once()

    async def test_update_profile_empty_name_raises_domain_error(self):
        repo = AsyncMock()
        repo.get_profile.return_value = _make_profile()

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(name="")
        with pytest.raises(EmptyFieldError):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    async def test_update_profile_name_too_long_raises_domain_error(self):
        repo = AsyncMock()
        repo.get_profile.return_value = _make_profile()

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(name="N" * (Profile.MAX_NAME_LENGTH + 1))
        with pytest.raises(InvalidLengthError):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    async def test_update_profile_invalid_avatar_url_raises_domain_error(self):
        repo = AsyncMock()
        repo.get_profile.return_value = _make_profile()

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(avatar_url="ftp://not-allowed")
        with pytest.raises(InvalidURLError):
            await uc.execute(request)

        repo.update.assert_not_awaited()
