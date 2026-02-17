"""Tests for the health router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1"


class TestHealthCheck:
    async def test_health_check_returns_ok(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data
        assert "version" in data
        assert "environment" in data
        assert "timestamp" in data

    async def test_health_check_has_environment(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/health")
        data = response.json()
        assert isinstance(data["environment"], str)
        assert len(data["environment"]) > 0


class TestHealthCheckDB:
    async def test_health_db_returns_status(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/health/db")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert data["database"] in ("connected", "disconnected")
