"""Tests for the certification router endpoints."""

from httpx import AsyncClient
import pytest

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


class TestUpdateCertification:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"title": "Updated Cert"}
        response = await client.put(f"{PREFIX}/cert_001", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "cert_001"

    async def test_update_not_found(self, client: AsyncClient):
        payload = {"title": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestCertificationFilters:
    async def test_expired_certifications(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expired")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # cert_005 (Docker DCA) is the only expired one (2023-09-12)
        expired_ids = [c["id"] for c in data]
        assert "cert_005" in expired_ids

    async def test_expired_excludes_no_expiry(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expired")
        data = response.json()
        ids = [c["id"] for c in data]
        # cert_002, cert_003, cert_004 have no expiry
        assert "cert_002" not in ids
        assert "cert_003" not in ids

    async def test_expiring_soon_certifications(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expiring-soon")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_expiring_soon_with_custom_days(self, client: AsyncClient):
        response = await client.get(
            f"{PREFIX}/status/expiring-soon", params={"days": 3650}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_active_only_excludes_expired(self, client: AsyncClient):
        all_response = await client.get(PREFIX)
        active_response = await client.get(PREFIX, params={"active_only": "true"})
        all_data = all_response.json()
        active_data = active_response.json()
        assert len(active_data) <= len(all_data)
        # cert_005 (expired) should not be in active list
        active_ids = [c["id"] for c in active_data]
        assert "cert_005" not in active_ids

    async def test_active_only_includes_no_expiry(self, client: AsyncClient):
        response = await client.get(PREFIX, params={"active_only": "true"})
        data = response.json()
        active_ids = [c["id"] for c in data]
        # cert_002 has no expiry, should be included
        assert "cert_002" in active_ids

    async def test_by_issuer_case_insensitive(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-issuer/amazon")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(c["id"] == "cert_001" for c in data)

    async def test_by_issuer_no_results(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-issuer/NonexistentIssuer")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0


class TestReorderCertifications:
    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "cert_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
