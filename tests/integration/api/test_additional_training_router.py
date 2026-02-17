"""Integration tests for the additional training router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/additional-training"


class TestListAdditionalTrainings:
    async def test_list_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_training_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        training = response.json()[0]
        assert "id" in training
        assert "title" in training
        assert "provider" in training
        assert "order_index" in training

    async def test_trainings_sorted_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [t["order_index"] for t in data]
        assert indices == sorted(indices)


class TestGetAdditionalTraining:
    async def test_get_training_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/train_001")
        assert response.status_code == 200

    async def test_get_training_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/train_001")
        data = response.json()
        assert data["id"] == "train_001"
        assert "title" in data

    async def test_get_nonexistent_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateAdditionalTraining:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {
            "title": "Test Training",
            "provider": "Test Provider",
            "completion_date": "2024-01-01T00:00:00",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_with_all_fields(self, client: AsyncClient):
        payload = {
            "title": "Test Training",
            "provider": "Test Provider",
            "completion_date": "2024-01-01T00:00:00",
            "duration": "20 hours",
            "description": "A test training course",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_error_missing_title(self, client: AsyncClient):
        payload = {
            "provider": "Test Provider",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_empty_provider(self, client: AsyncClient):
        payload = {
            "title": "Test",
            "provider": "",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateAdditionalTraining:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"title": "Updated Training"}
        response = await client.put(f"{PREFIX}/train_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        payload = {"title": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteAdditionalTraining:
    async def test_delete_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/train_001")
        assert response.status_code == 200

    async def test_delete_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/train_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestReorderAdditionalTrainings:
    async def test_reorder_returns_200(self, client: AsyncClient):
        payload = [{"id": "train_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200

    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "train_001", "orderIndex": 0}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        data = response.json()
        assert isinstance(data, list)
