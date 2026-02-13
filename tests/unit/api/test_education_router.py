"""Tests for the education router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/education"


class TestListEducation:
    async def test_list_education_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_list_education_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "institution" in first
        assert "degree" in first
        assert "order_index" in first


class TestGetEducation:
    async def test_get_education_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/edu_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "edu_001"

    async def test_get_education_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateEducation:
    async def test_create_education_returns_201(self, client: AsyncClient):
        payload = {
            "institution": "MIT",
            "degree": "MSc Computer Science",
            "field": "AI",
            "start_date": "2020-09-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_education_validation_missing_fields(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestUpdateEducation:
    async def test_update_education_not_found(self, client: AsyncClient):
        payload = {"institution": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteEducation:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/edu_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
