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

from collections.abc import AsyncGenerator
import os

from httpx import AsyncClient
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
# DATABASE CLEANUP — USES THE APP'S OWN DB REFERENCE
# =====================================================================


async def _drop_all_collections(db) -> None:
    """Drop every collection in the database."""
    for name in await db.list_collection_names():
        await db.drop_collection(name)


@pytest_asyncio.fixture(autouse=True)
async def _ensure_clean_db(client: AsyncClient) -> AsyncGenerator[None, None]:
    """
    Ensure a completely clean database for every E2E test.

    Depends on ``client`` so it runs AFTER MongoDBClient.connect() has
    been called by the global client fixture.  Uses the app's own DB
    reference (MongoDBClient.db) to guarantee we clean the exact same
    database the app writes to.
    """
    from app.infrastructure.database.mongo_client import MongoDBClient

    if MongoDBClient.db is not None:
        await _drop_all_collections(MongoDBClient.db)

    yield

    if MongoDBClient.db is not None:
        await _drop_all_collections(MongoDBClient.db)
