"""
Fixtures for E2E tests.

E2E tests exercise the FULL stack without mocks:
    API → Use Cases → Repositories → MongoDB (real)

Requirements:
    - MONGODB_URL environment variable must be set
    - A running MongoDB instance (Docker or CI service)

Unlike integration tests, NO dependency_overrides are applied here.
Every request goes through the real DI chain.
"""

import os

from motor.motor_asyncio import AsyncIOMotorClient
import pytest
import pytest_asyncio

pytestmark = pytest.mark.e2e

# =====================================================================
# SKIP E2E IF MONGODB IS NOT AVAILABLE
# =====================================================================

requires_mongodb = pytest.mark.skipif(
    not os.getenv("MONGODB_URL"),
    reason="MONGODB_URL not set — E2E tests require a running MongoDB instance",
)


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
# DATABASE CLEANUP
# =====================================================================

TEST_DB_NAME = "portfolio_test_db"


async def _clean_database(db):
    """Delete all documents from every collection in the test database."""
    collections = await db.list_collection_names()
    for collection in collections:
        await db[collection].delete_many({})


@pytest_asyncio.fixture(autouse=True)
async def _clean_db_for_e2e(test_settings):
    """
    Ensure a clean database for every E2E test.

    Runs automatically before and after each test.
    Uses a separate motor client to avoid interfering with the app's connection.
    """
    if not os.getenv("MONGODB_URL"):
        yield
        return

    motor_client = AsyncIOMotorClient(test_settings.MONGODB_URL)
    db = motor_client[TEST_DB_NAME]

    await _clean_database(db)
    yield
    await _clean_database(db)

    motor_client.close()
