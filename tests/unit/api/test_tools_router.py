"""Tests for the tools router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/tools"


class TestListTools:
    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_filter_by_category(self, client: AsyncClient):
        response = await client.get(PREFIX, params={"category": "ide"})
        assert response.status_code == 200
        data = response.json()
        assert all(t["category"] == "ide" for t in data)

    async def test_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "name" in first
        assert "category" in first


class TestGetTool:
    async def test_get_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/tool_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "tool_001"

    async def test_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateTool:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {"name": "Vim", "category": "ide", "order_index": 99}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_validation_empty(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestUpdateTool:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"name": "Updated Tool"}
        response = await client.put(f"{PREFIX}/tool_001", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "tool_001"

    async def test_update_not_found(self, client: AsyncClient):
        payload = {"name": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteTool:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/tool_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestReorderTools:
    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "tool_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestToolGrouped:
    async def test_grouped_by_category(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "ide" in data
        assert "version_control" in data

    async def test_grouped_by_category_sorted(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        data = response.json()
        for category, tools in data.items():
            indices = [t["order_index"] for t in tools]
            assert indices == sorted(indices), f"{category} not sorted"


class TestToolStats:
    async def test_stats_summary(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "by_category" in data
        assert data["total"] > 0

    async def test_stats_total_matches_list(self, client: AsyncClient):
        list_response = await client.get(PREFIX)
        stats_response = await client.get(f"{PREFIX}/stats/summary")
        total_list = len(list_response.json())
        total_stats = stats_response.json()["total"]
        assert total_list == total_stats

    async def test_stats_by_category_sums_to_total(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        data = response.json()
        category_sum = sum(data["by_category"].values())
        assert category_sum == data["total"]
