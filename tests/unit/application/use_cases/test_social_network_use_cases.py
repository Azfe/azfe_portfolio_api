"""Tests for SocialNetwork use cases."""

from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    AddSocialNetworkRequest,
    DeleteSocialNetworkRequest,
    EditSocialNetworkRequest,
    ListSocialNetworksRequest,
)
from app.application.use_cases.social_network.add_social_network import (
    AddSocialNetworkUseCase,
)
from app.application.use_cases.social_network.delete_social_network import (
    DeleteSocialNetworkUseCase,
)
from app.application.use_cases.social_network.edit_social_network import (
    EditSocialNetworkUseCase,
)
from app.application.use_cases.social_network.list_social_networks import (
    ListSocialNetworksUseCase,
)
from app.domain.entities.social_network import SocialNetwork
from app.shared.shared_exceptions import DuplicateException, NotFoundException

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"


def _make_social_network(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "platform": "LinkedIn",
        "url": "https://linkedin.com/in/azfe",
        "order_index": 0,
        "username": "azfe",
    }
    defaults.update(overrides)
    return SocialNetwork.create(**defaults)


class TestAddSocialNetworkUseCase:
    @pytest.mark.unit
    async def test_add_social_network_success(self):
        repo = AsyncMock()
        social_network = _make_social_network()
        repo.exists_by_platform.return_value = False
        repo.add.return_value = social_network

        uc = AddSocialNetworkUseCase(repo)
        request = AddSocialNetworkRequest(
            profile_id=PROFILE_ID,
            platform="LinkedIn",
            url="https://linkedin.com/in/azfe",
            order_index=0,
            username="azfe",
        )
        result = await uc.execute(request)

        assert result.platform == "LinkedIn"
        assert result.url == "https://linkedin.com/in/azfe"
        assert result.profile_id == PROFILE_ID
        repo.exists_by_platform.assert_awaited_once_with(PROFILE_ID, "LinkedIn")
        repo.add.assert_awaited_once()

    @pytest.mark.unit
    async def test_add_social_network_duplicate_platform_raises(self):
        repo = AsyncMock()
        repo.exists_by_platform.return_value = True

        uc = AddSocialNetworkUseCase(repo)
        request = AddSocialNetworkRequest(
            profile_id=PROFILE_ID,
            platform="LinkedIn",
            url="https://linkedin.com/in/azfe",
            order_index=0,
        )
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.add.assert_not_awaited()


class TestDeleteSocialNetworkUseCase:
    @pytest.mark.unit
    async def test_delete_social_network_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteSocialNetworkUseCase(repo)
        result = await uc.execute(
            DeleteSocialNetworkRequest(social_network_id="sn-001")
        )

        assert result.success is True
        repo.delete.assert_awaited_once_with("sn-001")

    @pytest.mark.unit
    async def test_delete_social_network_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteSocialNetworkUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(
                DeleteSocialNetworkRequest(social_network_id="nonexistent")
            )


class TestEditSocialNetworkUseCase:
    @pytest.mark.unit
    async def test_edit_social_network_success(self):
        repo = AsyncMock()
        social_network = _make_social_network()
        repo.get_by_id.return_value = social_network
        repo.exists_by_platform.return_value = False
        repo.update.return_value = social_network

        uc = EditSocialNetworkUseCase(repo)
        request = EditSocialNetworkRequest(
            social_network_id="sn-001",
            platform="GitHub",
            url="https://github.com/azfe",
        )
        result = await uc.execute(request)

        assert result.platform == "GitHub"
        repo.get_by_id.assert_awaited_once_with("sn-001")
        repo.update.assert_awaited_once()

    @pytest.mark.unit
    async def test_edit_social_network_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditSocialNetworkUseCase(repo)
        request = EditSocialNetworkRequest(
            social_network_id="nonexistent",
            platform="GitHub",
        )
        with pytest.raises(NotFoundException):
            await uc.execute(request)

    @pytest.mark.unit
    async def test_edit_social_network_duplicate_platform_raises(self):
        repo = AsyncMock()
        social_network = _make_social_network()
        repo.get_by_id.return_value = social_network
        repo.exists_by_platform.return_value = True

        uc = EditSocialNetworkUseCase(repo)
        request = EditSocialNetworkRequest(
            social_network_id="sn-001",
            platform="GitHub",
        )
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    @pytest.mark.unit
    async def test_edit_social_network_same_platform_no_duplicate_check(self):
        repo = AsyncMock()
        social_network = _make_social_network()
        repo.get_by_id.return_value = social_network
        repo.update.return_value = social_network

        uc = EditSocialNetworkUseCase(repo)
        # Same platform as the existing entity — should not trigger uniqueness check
        request = EditSocialNetworkRequest(
            social_network_id="sn-001",
            platform="LinkedIn",
            url="https://linkedin.com/in/azfe-updated",
        )
        await uc.execute(request)

        repo.exists_by_platform.assert_not_awaited()
        repo.update.assert_awaited_once()


class TestListSocialNetworksUseCase:
    @pytest.mark.unit
    async def test_list_social_networks_returns_all(self):
        repo = AsyncMock()
        social_networks = [
            _make_social_network(order_index=0),
            _make_social_network(
                platform="GitHub", url="https://github.com/azfe", order_index=1
            ),
        ]
        repo.find_by.return_value = social_networks

        uc = ListSocialNetworksUseCase(repo)
        request = ListSocialNetworksRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 2
        assert len(result.social_networks) == 2
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    @pytest.mark.unit
    async def test_list_social_networks_empty(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = ListSocialNetworksUseCase(repo)
        request = ListSocialNetworksRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 0
        assert result.social_networks == []

    @pytest.mark.unit
    async def test_list_social_networks_ascending_order(self):
        repo = AsyncMock()
        social_networks = [
            _make_social_network(
                platform="Twitter", url="https://twitter.com/azfe", order_index=2
            ),
            _make_social_network(
                platform="GitHub", url="https://github.com/azfe", order_index=0
            ),
            _make_social_network(order_index=1),
        ]
        repo.find_by.return_value = social_networks

        uc = ListSocialNetworksUseCase(repo)
        result = await uc.execute(
            ListSocialNetworksRequest(profile_id=PROFILE_ID, ascending=True)
        )

        order_indexes = [sn.order_index for sn in result.social_networks]
        assert order_indexes == sorted(order_indexes)

    @pytest.mark.unit
    async def test_list_social_networks_descending_order(self):
        repo = AsyncMock()
        social_networks = [
            _make_social_network(
                platform="Twitter", url="https://twitter.com/azfe", order_index=0
            ),
            _make_social_network(
                platform="GitHub", url="https://github.com/azfe", order_index=2
            ),
            _make_social_network(order_index=1),
        ]
        repo.find_by.return_value = social_networks

        uc = ListSocialNetworksUseCase(repo)
        result = await uc.execute(
            ListSocialNetworksRequest(profile_id=PROFILE_ID, ascending=False)
        )

        order_indexes = [sn.order_index for sn in result.social_networks]
        assert order_indexes == sorted(order_indexes, reverse=True)
