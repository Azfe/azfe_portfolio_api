"""
Fixtures for API integration tests.

These tests exercise the full HTTP stack (middleware → exception handlers →
routers) using httpx.AsyncClient against the real FastAPI application.

Currently the routers use in-memory mock data, so no database is required.
When routers are connected to real use cases via DI, these fixtures will
be extended to provide a test database via dependency_overrides.
"""

import pytest

# Mark all tests in this package as integration tests
pytestmark = pytest.mark.integration
