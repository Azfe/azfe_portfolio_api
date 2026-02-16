"""Tests for the work experience router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/work-experiences"


class TestListExperiences:
    async def test_list_experiences_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_list_experiences_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "role" in first
        assert "company" in first
        assert "start_date" in first


class TestGetExperience:
    async def test_get_experience_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/exp_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "exp_001"

    async def test_get_experience_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateExperience:
    async def test_create_experience_returns_201(self, client: AsyncClient):
        payload = {
            "role": "Developer",
            "company": "ACME",
            "start_date": "2023-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_experience_validation_empty(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestUpdateExperience:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"role": "Updated Role"}
        response = await client.put(f"{PREFIX}/exp_001", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "exp_001"

    async def test_update_experience_not_found(self, client: AsyncClient):
        payload = {"role": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteExperience:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/exp_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestReorderExperiences:
    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "exp_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestCurrentActive:
    async def test_current_active_returns_list(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/current/active")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_current_active_have_no_end_date(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/current/active")
        data = response.json()
        for exp in data:
            assert exp["end_date"] is None

    async def test_current_active_fewer_than_total(self, client: AsyncClient):
        all_response = await client.get(PREFIX)
        active_response = await client.get(f"{PREFIX}/current/active")
        assert len(active_response.json()) < len(all_response.json())

    async def test_current_active_contains_exp_001(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/current/active")
        data = response.json()
        ids = [e["id"] for e in data]
        assert "exp_001" in ids


class TestFilterByCompany:
    async def test_by_company_returns_list(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-company/Tech")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all("tech" in e["company"].lower() for e in data)

    async def test_by_company_case_insensitive(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-company/tech")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_by_company_no_results(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-company/NonexistentCompany")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
