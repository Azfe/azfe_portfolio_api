"""Integration tests for middleware behavior.

Tests that middlewares (ProcessTime, Logging, CORS) work correctly
through the full HTTP stack.
"""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.integration


class TestProcessTimeMiddleware:
    """Tests that X-Process-Time header is present in all responses."""

    async def test_health_has_process_time_header(self, client: AsyncClient):
        response = await client.get("/api/v1/health")
        assert "x-process-time" in response.headers
        process_time = float(response.headers["x-process-time"])
        assert process_time >= 0

    async def test_profile_has_process_time_header(self, client: AsyncClient):
        response = await client.get("/api/v1/profile")
        assert "x-process-time" in response.headers

    async def test_skills_has_process_time_header(self, client: AsyncClient):
        response = await client.get("/api/v1/skills")
        assert "x-process-time" in response.headers

    async def test_process_time_on_404(self, client: AsyncClient):
        response = await client.get("/api/v1/skills/nonexistent")
        assert "x-process-time" in response.headers

    async def test_process_time_on_422(self, client: AsyncClient):
        response = await client.post("/api/v1/skills", json={})
        assert "x-process-time" in response.headers

    async def test_root_has_process_time_header(self, client: AsyncClient):
        response = await client.get("/")
        assert "x-process-time" in response.headers


class TestResponseHeaders:
    """Tests that responses have expected headers."""

    async def test_content_type_is_json(self, client: AsyncClient):
        response = await client.get("/api/v1/health")
        assert "application/json" in response.headers["content-type"]

    async def test_content_type_on_error(self, client: AsyncClient):
        response = await client.post("/api/v1/skills", json={})
        assert "application/json" in response.headers["content-type"]

    async def test_content_type_on_list_endpoint(self, client: AsyncClient):
        response = await client.get("/api/v1/skills")
        assert "application/json" in response.headers["content-type"]
