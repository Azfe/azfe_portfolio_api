"""Integration tests for the tools router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/tools"


class TestListTools:
    async def test_list_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_tool_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        tool = response.json()[0]
        assert "id" in tool
        assert "name" in tool
        assert "category" in tool
        assert "order_index" in tool

    async def test_tools_sorted_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [t["order_index"] for t in data]
        assert indices == sorted(indices)

    async def test_filter_tools_by_category(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?category=ide")
        assert response.status_code == 200
        data = response.json()
        assert all(t["category"] == "ide" for t in data)

    async def test_filter_nonexistent_category_returns_empty(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?category=nonexistent")
        assert response.status_code == 200
        assert response.json() == []


class TestGetTool:
    async def test_get_tool_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/tool_001")
        assert response.status_code == 200

    async def test_get_tool_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/tool_001")
        data = response.json()
        assert data["id"] == "tool_001"
        assert "name" in data
        assert "category" in data

    async def test_get_nonexistent_tool_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateTool:
    async def test_create_tool_returns_201(self, client: AsyncClient):
        payload = {
            "name": "New Tool",
            "category": "ide",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_error_missing_name(self, client: AsyncClient):
        payload = {
            "category": "ide",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_empty_name(self, client: AsyncClient):
        payload = {
            "name": "",
            "category": "ide",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_negative_order(self, client: AsyncClient):
        payload = {
            "name": "Tool",
            "category": "ide",
            "order_index": -1,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateTool:
    async def test_update_tool_returns_200(self, client: AsyncClient):
        payload = {"name": "Updated Tool"}
        response = await client.put(f"{PREFIX}/tool_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        payload = {"name": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteTool:
    async def test_delete_tool_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/tool_001")
        assert response.status_code == 200

    async def test_delete_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/tool_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestReorderTools:
    async def test_reorder_returns_200(self, client: AsyncClient):
        payload = [{"id": "tool_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200

    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "tool_001", "orderIndex": 0}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        data = response.json()
        assert isinstance(data, list)


class TestToolsGroupedByCategory:
    async def test_grouped_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        assert response.status_code == 200

    async def test_grouped_is_dict(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    async def test_grouped_has_ide_category(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        data = response.json()
        assert "ide" in data
        assert isinstance(data["ide"], list)


class TestToolsStats:
    async def test_stats_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        assert response.status_code == 200

    async def test_stats_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        data = response.json()
        assert "total" in data
        assert "by_category" in data
        assert isinstance(data["total"], int)
        assert data["total"] > 0
