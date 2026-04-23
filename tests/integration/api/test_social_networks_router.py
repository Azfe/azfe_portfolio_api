"""Integration tests for the social networks router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/social-networks"


class TestListSocialNetworks:
    async def test_list_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_social_network_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        social = response.json()[0]
        assert "id" in social
        assert "platform" in social
        assert "url" in social
        assert "order_index" in social

    async def test_sorted_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [s["order_index"] for s in data]
        assert indices == sorted(indices)


class TestGetSocialNetwork:
    async def test_get_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/social_001")
        assert response.status_code == 200

    async def test_get_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/social_001")
        data = response.json()
        assert data["id"] == "social_001"
        assert "platform" in data
        assert "url" in data

    async def test_get_nonexistent_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateSocialNetwork:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {
            "platform": "github",
            "url": "https://github.com/testuser",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_with_username(self, client: AsyncClient):
        payload = {
            "platform": "github",
            "url": "https://github.com/testuser",
            "username": "testuser",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_error_missing_platform(self, client: AsyncClient):
        payload = {
            "url": "https://github.com/test",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_missing_url(self, client: AsyncClient):
        payload = {
            "platform": "github",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateSocialNetwork:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"url": "https://github.com/updated"}
        response = await client.put(f"{PREFIX}/social_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        payload = {"url": "https://github.com/updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteSocialNetwork:
    async def test_delete_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/social_001")
        assert response.status_code == 200

    async def test_delete_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/social_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestReorderSocialNetworks:
    async def test_reorder_returns_200(self, client: AsyncClient):
        payload = [{"id": "social_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200

    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "social_001", "orderIndex": 0}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        data = response.json()
        assert isinstance(data, list)


class TestByPlatform:
    async def test_by_platform_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-platform/github")
        assert response.status_code == 200

    async def test_by_platform_filters_correctly(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-platform/github")
        data = response.json()
        assert isinstance(data, list)
        for social in data:
            assert social["platform"] == "github"

    async def test_by_platform_nonexistent_returns_empty(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-platform/tiktok")
        assert response.status_code == 200
        assert response.json() == []


class TestGroupedByPlatform:
    async def test_grouped_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-platform")
        assert response.status_code == 200

    async def test_grouped_is_dict(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-platform")
        data = response.json()
        assert isinstance(data, dict)
        assert "github" in data
