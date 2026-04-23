"""Integration tests for the health check endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration


class TestHealthCheck:
    async def test_health_returns_200(self, client: AsyncClient):
        response = await client.get("/api/v1/health")
        assert response.status_code == 200

    async def test_health_response_schema(self, client: AsyncClient):
        response = await client.get("/api/v1/health")
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data
        assert "version" in data
        assert "environment" in data
        assert "timestamp" in data

    async def test_health_environment_is_set(self, client: AsyncClient):
        response = await client.get("/api/v1/health")
        data = response.json()
        assert data["environment"] in ("test", "development")


class TestRootEndpoint:
    async def test_root_returns_200(self, client: AsyncClient):
        response = await client.get("/")
        assert response.status_code == 200

    async def test_root_response_has_required_fields(self, client: AsyncClient):
        response = await client.get("/")
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data
