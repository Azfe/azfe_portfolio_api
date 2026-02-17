"""
Fixtures for E2E tests.

E2E tests exercise the FULL stack without mocks:
    API → Use Cases → Repositories → MongoDB (real)

Requirements:
    - MONGODB_URL environment variable must be set
    - A running MongoDB instance (Docker or CI service)

Unlike integration tests, NO dependency_overrides are applied here.
Every request goes through the real DI chain.

This conftest OVERRIDES the global `client` fixture to integrate
database cleanup directly, guaranteeing execution order.
"""

from collections.abc import AsyncGenerator
import os

from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
import pytest
import pytest_asyncio

pytestmark = pytest.mark.e2e

TEST_DB_NAME = "portfolio_test_db"

# =====================================================================
# SKIP E2E IF MONGODB IS NOT AVAILABLE
# =====================================================================


def pytest_collection_modifyitems(items):
    """Auto-skip all E2E tests when MongoDB is not available."""
    if os.getenv("MONGODB_URL"):
        return
    skip_marker = pytest.mark.skip(
        reason="MONGODB_URL not set — E2E tests require a running MongoDB instance"
    )
    for item in items:
        item.add_marker(skip_marker)


# =====================================================================
# CLIENT FIXTURE WITH INTEGRATED DB CLEANUP
# =====================================================================


@pytest_asyncio.fixture
async def client(test_settings, monkeypatch) -> AsyncGenerator[AsyncClient, None]:
    """
    HTTP client for E2E tests with integrated database cleanup.

    Overrides the global client fixture to ensure the database is
    completely clean BEFORE each test and cleaned up AFTER.
    All operations happen in a single fixture to guarantee order:
        1. Drop database (clean slate)
        2. Monkeypatch settings
        3. Connect MongoDBClient
        4. Yield AsyncClient for the test
        5. Disconnect MongoDBClient
        6. Drop database (cleanup)
    """
    from app.config import settings as settings_module
    from app.infrastructure.database import mongo_client as mongo_module
    from app.infrastructure.database.mongo_client import MongoDBClient
    from app.main import app

    # 1. Drop the test database for a clean slate
    cleanup_client = AsyncIOMotorClient(test_settings.MONGODB_URL)
    await cleanup_client.drop_database(TEST_DB_NAME)

    # 2. Reset MongoDBClient singleton
    MongoDBClient.client = None
    MongoDBClient.db = None

    # 3. Monkeypatch settings to use test config
    monkeypatch.setattr(settings_module, "settings", test_settings)
    monkeypatch.setattr(mongo_module, "settings", test_settings)

    # 4. Connect MongoDBClient to the clean database
    await MongoDBClient.connect()

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac
    finally:
        # 5. Disconnect the app
        await MongoDBClient.disconnect()

        # 6. Drop database again for cleanup
        await cleanup_client.drop_database(TEST_DB_NAME)
        cleanup_client.close()
