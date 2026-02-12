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


class TestDeleteTool:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/tool_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestToolGrouped:
    async def test_grouped_by_category(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


class TestToolStats:
    async def test_stats_summary(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
