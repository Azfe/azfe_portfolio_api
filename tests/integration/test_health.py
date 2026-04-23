# tests/integration/test_health.py
"""
Tests de integración para el endpoint de health check.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test: Health check endpoint retorna 200"""
    response = await client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "version" in data
    assert "environment" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test: Root endpoint retorna información básica"""
    response = await client.get("/")

    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
