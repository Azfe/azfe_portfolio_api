"""Tests for the social networks router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/social-networks"


class TestListSocialNetworks:
    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "platform" in first
        assert "url" in first


class TestGetSocialNetwork:
    async def test_get_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/social_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "social_001"

    async def test_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateSocialNetwork:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {
            "platform": "twitter",
            "url": "https://twitter.com/test",
            "username": "test",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_validation_empty(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestDeleteSocialNetwork:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/social_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestGroupedByPlatform:
    async def test_grouped_returns_dict(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-platform")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
