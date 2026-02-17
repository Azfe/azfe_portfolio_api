# tests/conftest.py
"""
Configuración global de pytest.
Este archivo se ejecuta antes de todos los tests.
"""

import os
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import Settings
from app.main import app

# ==================== FIXTURES DE CONFIGURACIÓN ====================


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """
    Settings de prueba.
    Usa la variable de entorno MONGODB_URL si está definida (Docker),
    con fallback a localhost para ejecución local.
    """
    return Settings(
        ENVIRONMENT="test",
        DEBUG=True,
        MONGODB_URL=os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
        MONGODB_DB_NAME="portfolio_test_db",
        SECRET_KEY="test-secret-key-never-use-in-production",
    )


# ==================== FIXTURES DE CLIENTE HTTP ====================


@pytest_asyncio.fixture
async def client(test_settings, monkeypatch) -> AsyncGenerator[AsyncClient, None]:
    """
    Cliente HTTP asíncrono para testear endpoints de FastAPI.
    
    Inicializa MongoDBClient con los settings de test y limpia después.
    El lifespan de la app no se ejecuta con ASGITransport, así que lo hacemos manualmente.

    Ejemplo de uso:
        async def test_endpoint(client):
            response = await client.get("/api/v1/health")
            assert response.status_code == 200
    """
    from app.config import settings as settings_module
    from app.infrastructure.database import mongo_client as mongo_module
    from app.infrastructure.database.mongo_client import MongoDBClient
    
    # Resetear MongoDBClient por si tiene estado anterior
    MongoDBClient.client = None
    MongoDBClient.db = None
    
    # Monkeypatch el singleton global de settings para usar test_settings
    monkeypatch.setattr(settings_module, "settings", test_settings)
    monkeypatch.setattr(mongo_module, "settings", test_settings)
    
    # Inicializar MongoDBClient con los settings de test
    await MongoDBClient.connect()
    
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac
    finally:
        # Asegurar que se desconecta después del test
        await MongoDBClient.disconnect()


# ==================== FIXTURES DE BASE DE DATOS ====================


TEST_DB_NAME = "portfolio_test_db"


@pytest_asyncio.fixture
async def mongodb_client(test_settings) -> AsyncIOMotorClient:
    """
    Cliente de MongoDB para tests.
    Se crea uno por cada test para evitar conflictos de event loop
    entre fixtures session-scoped y function-scoped.
    """
    client = AsyncIOMotorClient(test_settings.MONGODB_URL)
    yield client
    client.close()


@pytest_asyncio.fixture
async def test_db(mongodb_client):
    """
    Base de datos de test limpia.
    Se limpia antes y después de cada test.
    Usa siempre portfolio_test_db, nunca la BD de producción.
    """
    db = mongodb_client[TEST_DB_NAME]

    # Limpiar antes del test
    await _clean_database(db)

    yield db

    # Limpiar después del test
    await _clean_database(db)


async def _clean_database(db):
    """Elimina todas las colecciones de la base de datos de test"""
    collections = await db.list_collection_names()
    for collection in collections:
        await db[collection].delete_many({})


# ==================== FIXTURES DE DATOS DE PRUEBA ====================


# Datetime fixtures
@pytest.fixture
def today() -> datetime:
    """Returns today's date."""
    return datetime.now()


@pytest.fixture
def yesterday(today) -> datetime:
    """Returns yesterday's date."""
    return today - timedelta(days=1)


@pytest.fixture
def tomorrow(today) -> datetime:
    """Returns tomorrow's date."""
    return today + timedelta(days=1)


# ID fixtures
@pytest.fixture
def profile_id() -> str:
    """Returns a sample profile ID."""
    return "profile-123"


# Validation fixtures
@pytest.fixture
def valid_email() -> str:
    """Returns a valid email."""
    return "test@example.com"


@pytest.fixture
def invalid_email() -> str:
    """Returns an invalid email."""
    return "not-an-email"


@pytest.fixture
def valid_url() -> str:
    """Returns a valid URL."""
    return "https://example.com"


@pytest.fixture
def invalid_url() -> str:
    """Returns an invalid URL."""
    return "not-a-url"


# Sample entity data fixtures
@pytest.fixture
def sample_profile_data():
    """Datos de ejemplo para Profile"""
    return {
        "full_name": "Test User",
        "headline": "Test Developer",
        "about": "Test description",
        "location": "Test City",
    }


@pytest.fixture
def sample_skill_data():
    """Datos de ejemplo para Skill"""
    return {
        "name": "Python",
        "level": "expert",
        "category": "backend",
        "order_index": 0,
    }


# ==================== HOOKS DE PYTEST ====================


def pytest_configure(config):
    """
    Hook que se ejecuta al inicio de pytest.
    Aquí puedes configurar variables de entorno, etc.
    """
    import os

    os.environ["ENVIRONMENT"] = "test"


def pytest_collection_modifyitems(items):
    """
    Hook para modificar items de test.
    Aquí puedes añadir marcadores automáticos, etc.
    """
    for item in items:
        # Añadir marcador 'asyncio' automáticamente a tests async
        if "asyncio" in item.keywords:
            item.add_marker(pytest.mark.asyncio)
