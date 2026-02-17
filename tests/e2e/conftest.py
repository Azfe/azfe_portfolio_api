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


@pytest_asyncio.fixture(autouse=True)
async def _clean_db_for_e2e(test_settings):
    """
    Ensure a clean database for every E2E test.

    Drops the entire test database before and after each test to guarantee
    complete isolation. Uses a separate motor client to avoid interfering
    with the app's MongoDBClient singleton.
    """
    if not os.getenv("MONGODB_URL"):
        yield
        return

    from app.infrastructure.database.mongo_client import MongoDBClient

    # Reset the app's MongoDBClient singleton so each test starts fresh
    MongoDBClient.client = None
    MongoDBClient.db = None

    motor_client = AsyncIOMotorClient(test_settings.MONGODB_URL)

    # Drop entire database for complete isolation
    await motor_client.drop_database(TEST_DB_NAME)

    yield

    # Drop again after the test
    await motor_client.drop_database(TEST_DB_NAME)

    motor_client.close()
