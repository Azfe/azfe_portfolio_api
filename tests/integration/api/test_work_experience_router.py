"""Integration tests for the work experience router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/work-experiences"


class TestListWorkExperiences:
    async def test_list_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_experience_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        exp = response.json()[0]
        assert "id" in exp
        assert "role" in exp
        assert "company" in exp
        assert "start_date" in exp
        assert "order_index" in exp
        assert "responsibilities" in exp

    async def test_experiences_sorted_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [e["order_index"] for e in data]
        assert indices == sorted(indices)


class TestGetWorkExperience:
    async def test_get_experience_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/exp_001")
        assert response.status_code == 200

    async def test_get_experience_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/exp_001")
        data = response.json()
        assert data["id"] == "exp_001"
        assert "role" in data
        assert "company" in data

    async def test_get_nonexistent_experience_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateWorkExperience:
    async def test_create_experience_returns_201(self, client: AsyncClient):
        payload = {
            "role": "Test Developer",
            "company": "Test Corp",
            "start_date": "2023-01-01T00:00:00",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_with_end_date(self, client: AsyncClient):
        payload = {
            "role": "Test Developer",
            "company": "Test Corp",
            "start_date": "2023-01-01T00:00:00",
            "end_date": "2024-01-01T00:00:00",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_error_missing_role(self, client: AsyncClient):
        payload = {
            "company": "Test Corp",
            "start_date": "2023-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_empty_company(self, client: AsyncClient):
        payload = {
            "role": "Dev",
            "company": "",
            "start_date": "2023-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateWorkExperience:
    async def test_update_experience_returns_200(self, client: AsyncClient):
        payload = {"role": "Updated Role"}
        response = await client.put(f"{PREFIX}/exp_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        payload = {"role": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteWorkExperience:
    async def test_delete_experience_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/exp_001")
        assert response.status_code == 200

    async def test_delete_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/exp_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestReorderWorkExperiences:
    async def test_reorder_returns_200(self, client: AsyncClient):
        payload = [{"id": "exp_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200

    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "exp_001", "orderIndex": 0}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        data = response.json()
        assert isinstance(data, list)


class TestCurrentWorkExperiences:
    async def test_current_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/current/active")
        assert response.status_code == 200

    async def test_current_returns_only_active(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/current/active")
        data = response.json()
        assert isinstance(data, list)
        for exp in data:
            assert exp["end_date"] is None


class TestByCompany:
    async def test_by_company_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-company/Tech")
        assert response.status_code == 200

    async def test_by_company_filters_correctly(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-company/Tech")
        data = response.json()
        assert isinstance(data, list)
        for exp in data:
            assert "tech" in exp["company"].lower()

    async def test_by_company_nonexistent_returns_empty(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-company/NonexistentCompany")
        assert response.status_code == 200
        data = response.json()
        assert data == []
