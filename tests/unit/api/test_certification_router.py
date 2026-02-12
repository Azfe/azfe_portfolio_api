"""Tests for the certification router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/certifications"


class TestListCertifications:
    async def test_list_certifications_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_list_certifications_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "title" in first
        assert "issuer" in first


class TestGetCertification:
    async def test_get_certification_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/cert_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "cert_001"

    async def test_get_certification_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateCertification:
    async def test_create_certification_returns_201(self, client: AsyncClient):
        payload = {
            "title": "AWS Certified",
            "issuer": "Amazon",
            "issue_date": "2024-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_certification_validation_empty(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestDeleteCertification:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/cert_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestCertificationFilters:
    async def test_expired_certifications(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expired")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_expiring_soon_certifications(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expiring-soon")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
