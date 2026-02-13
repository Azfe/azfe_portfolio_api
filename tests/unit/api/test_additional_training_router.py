"""Tests for the additional training router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/additional-training"


class TestListTraining:
    async def test_list_training_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_list_training_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "title" in first
        assert "provider" in first


class TestGetTraining:
    async def test_get_training_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/train_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "train_001"

    async def test_get_training_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateTraining:
    async def test_create_training_returns_201(self, client: AsyncClient):
        payload = {
            "title": "Advanced Python",
            "provider": "Udemy",
            "completion_date": "2024-01-15T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_training_validation_empty(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422
