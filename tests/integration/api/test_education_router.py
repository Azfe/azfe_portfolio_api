"""Integration tests for the education router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/education"


class TestListEducation:
    async def test_list_education_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_education_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_education_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        edu = response.json()[0]
        assert "id" in edu
        assert "institution" in edu
        assert "degree" in edu
        assert "field" in edu
        assert "start_date" in edu
        assert "order_index" in edu

    async def test_education_sorted_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [e["order_index"] for e in data]
        assert indices == sorted(indices)


class TestGetEducation:
    async def test_get_education_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/edu_001")
        assert response.status_code == 200

    async def test_get_education_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/edu_001")
        data = response.json()
        assert data["id"] == "edu_001"
        assert "institution" in data

    async def test_get_nonexistent_education_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateEducation:
    async def test_create_education_returns_201(self, client: AsyncClient):
        payload = {
            "institution": "Test University",
            "degree": "BSc",
            "field": "Computer Science",
            "start_date": "2020-09-01T00:00:00",
            "order_index": 10,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_education_with_end_date(self, client: AsyncClient):
        payload = {
            "institution": "Test University",
            "degree": "BSc",
            "field": "Computer Science",
            "start_date": "2020-09-01T00:00:00",
            "end_date": "2024-06-30T00:00:00",
            "order_index": 10,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_education_validation_error_missing_institution(
        self, client: AsyncClient
    ):
        payload = {
            "degree": "BSc",
            "field": "CS",
            "start_date": "2020-09-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_education_validation_error_empty_fields(
        self, client: AsyncClient
    ):
        payload = {
            "institution": "",
            "degree": "",
            "field": "",
            "start_date": "2020-09-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateEducation:
    async def test_update_education_returns_200(self, client: AsyncClient):
        payload = {"institution": "Updated University"}
        response = await client.put(f"{PREFIX}/edu_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_education_returns_404(self, client: AsyncClient):
        payload = {"institution": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteEducation:
    async def test_delete_education_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/edu_001")
        assert response.status_code == 200

    async def test_delete_education_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/edu_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestReorderEducation:
    async def test_reorder_education_returns_200(self, client: AsyncClient):
        payload = [
            {"id": "edu_001", "orderIndex": 1},
            {"id": "edu_002", "orderIndex": 0},
        ]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200

    async def test_reorder_education_returns_list(self, client: AsyncClient):
        payload = [{"id": "edu_001", "orderIndex": 0}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        data = response.json()
        assert isinstance(data, list)
