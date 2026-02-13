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
from app.shared.shared_exceptions import DuplicateException, NotFoundException

pytestmark = pytest.mark.asyncio


def _make_profile(**overrides):
    defaults = {"name": "Alex", "headline": "Developer"}
    defaults.update(overrides)
    return Profile.create(**defaults)


class TestCreateProfileUseCase:
    async def test_create_profile_success(self):
        repo = AsyncMock()
        profile = _make_profile()
        repo.profile_exists.return_value = False
        repo.add.return_value = profile

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(name="Alex", headline="Developer")
        result = await uc.execute(request)

        assert result.name == "Alex"
        assert result.headline == "Developer"
        repo.profile_exists.assert_awaited_once()
        repo.add.assert_awaited_once()

    async def test_create_profile_duplicate_raises(self):
        repo = AsyncMock()
        repo.profile_exists.return_value = True

        uc = CreateProfileUseCase(repo)
        request = CreateProfileRequest(name="Alex", headline="Developer")
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.add.assert_not_awaited()


class TestGetProfileUseCase:
    async def test_get_profile_success(self):
        repo = AsyncMock()
        profile = _make_profile()
        repo.get_profile.return_value = profile

        uc = GetProfileUseCase(repo)
        result = await uc.execute(GetProfileRequest())

        assert result.name == "Alex"
        repo.get_profile.assert_awaited_once()

    async def test_get_profile_not_found_raises(self):
        repo = AsyncMock()
        repo.get_profile.return_value = None

        uc = GetProfileUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(GetProfileRequest())


class TestUpdateProfileUseCase:
    async def test_update_profile_success(self):
        repo = AsyncMock()
        profile = _make_profile()
        repo.get_profile.return_value = profile
        repo.update.return_value = profile

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(name="Updated Alex")
        result = await uc.execute(request)

        assert result.name == "Updated Alex"
        repo.update.assert_awaited_once()

    async def test_update_profile_not_found_raises(self):
        repo = AsyncMock()
        repo.get_profile.return_value = None

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(name="Updated")
        with pytest.raises(NotFoundException):
            await uc.execute(request)

    async def test_update_profile_avatar(self):
        repo = AsyncMock()
        profile = _make_profile()
        repo.get_profile.return_value = profile
        repo.update.return_value = profile

        uc = UpdateProfileUseCase(repo)
        request = UpdateProfileRequest(avatar_url="https://example.com/avatar.png")
        await uc.execute(request)

        repo.update.assert_awaited_once()
