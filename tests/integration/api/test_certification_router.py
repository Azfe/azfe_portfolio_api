"""Integration tests for the certification router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/certifications"


class TestListCertifications:
    async def test_list_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_certification_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        cert = response.json()[0]
        assert "id" in cert
        assert "title" in cert
        assert "issuer" in cert
        assert "issue_date" in cert
        assert "order_index" in cert

    async def test_certifications_sorted_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [c["order_index"] for c in data]
        assert indices == sorted(indices)

    async def test_filter_active_only(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?active_only=true")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestGetCertification:
    async def test_get_certification_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/cert_001")
        assert response.status_code == 200

    async def test_get_certification_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/cert_001")
        data = response.json()
        assert data["id"] == "cert_001"
        assert "title" in data
        assert "issuer" in data

    async def test_get_nonexistent_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateCertification:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {
            "title": "Test Certification",
            "issuer": "Test Issuer",
            "issue_date": "2024-01-01T00:00:00",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_with_all_fields(self, client: AsyncClient):
        payload = {
            "title": "Test Certification",
            "issuer": "Test Issuer",
            "issue_date": "2024-01-01T00:00:00",
            "expiry_date": "2027-01-01T00:00:00",
            "credential_id": "CERT-123",
            "credential_url": "https://example.com/cert",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_error_missing_title(self, client: AsyncClient):
        payload = {
            "issuer": "Test Issuer",
            "issue_date": "2024-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_missing_issuer(self, client: AsyncClient):
        payload = {
            "title": "Test",
            "issue_date": "2024-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateCertification:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"title": "Updated Cert"}
        response = await client.put(f"{PREFIX}/cert_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        payload = {"title": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteCertification:
    async def test_delete_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/cert_001")
        assert response.status_code == 200

    async def test_delete_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/cert_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestReorderCertifications:
    async def test_reorder_returns_200(self, client: AsyncClient):
        payload = [{"id": "cert_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200

    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "cert_001", "orderIndex": 0}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        data = response.json()
        assert isinstance(data, list)


class TestByIssuer:
    async def test_by_issuer_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-issuer/Amazon")
        assert response.status_code == 200

    async def test_by_issuer_filters_correctly(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-issuer/Amazon")
        data = response.json()
        assert isinstance(data, list)
        for cert in data:
            assert "amazon" in cert["issuer"].lower()

    async def test_by_issuer_nonexistent_returns_empty(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/by-issuer/NonexistentIssuer")
        assert response.status_code == 200
        assert response.json() == []


class TestExpiredCertifications:
    async def test_expired_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expired")
        assert response.status_code == 200

    async def test_expired_returns_list(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expired")
        data = response.json()
        assert isinstance(data, list)


class TestExpiringSoon:
    async def test_expiring_soon_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expiring-soon")
        assert response.status_code == 200

    async def test_expiring_soon_with_custom_days(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/status/expiring-soon?days=365")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
