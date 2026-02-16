"""Tests for the social networks router endpoints."""

from httpx import AsyncClient
import pytest

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


class TestUpdateSocialNetwork:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"platform": "updated_platform"}
        response = await client.put(f"{PREFIX}/social_001", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "social_001"

    async def test_update_not_found(self, client: AsyncClient):
        payload = {"platform": "updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteSocialNetwork:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/social_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestReorderSocialNetworks:
    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "social_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestFilterByPlatform:
    async def test_by_platform_returns_list(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-platform/github")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(s["platform"] == "github" for s in data)

    async def test_by_platform_no_results(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-platform/nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


class TestGroupedByPlatform:
    async def test_grouped_returns_dict(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-platform")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "github" in data

    async def test_grouped_all_platforms_present(self, client: AsyncClient):
        list_response = await client.get(PREFIX)
        grouped_response = await client.get(f"{PREFIX}/grouped/by-platform")
        platforms_from_list = {s["platform"] for s in list_response.json()}
        grouped_data = grouped_response.json()
        assert set(grouped_data.keys()) == platforms_from_list

    async def test_grouped_total_matches_list(self, client: AsyncClient):
        list_response = await client.get(PREFIX)
        grouped_response = await client.get(f"{PREFIX}/grouped/by-platform")
        total_list = len(list_response.json())
        total_grouped = sum(len(v) for v in grouped_response.json().values())
        assert total_list == total_grouped
