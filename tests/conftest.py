# tests/conftest.py
"""
Configuración global de pytest.
Este archivo se ejecuta antes de todos los tests.
"""
import pytest
from typing import Generator
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient

from app.main import app
from app.config.settings import Settings


# ==================== FIXTURES DE CONFIGURACIÓN ====================

@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """
    Settings de prueba.
    Usa variables de entorno específicas para testing.
    """
    return Settings(
        ENVIRONMENT="test",
        DEBUG=True,
        MONGODB_URL="mongodb://localhost:27017",
        MONGODB_DB_NAME="portfolio_test_db",
        SECRET_KEY="test-secret-key-never-use-in-production"
    )


# ==================== FIXTURES DE CLIENTE HTTP ====================

@pytest.fixture
async def client() -> Generator:
    """
    Cliente HTTP asíncrono para testear endpoints de FastAPI.
    
    Ejemplo de uso:
        async def test_endpoint(client):
            response = await client.get("/api/v1/health")
            assert response.status_code == 200
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ==================== FIXTURES DE BASE DE DATOS ====================

@pytest.fixture(scope="session")
async def mongodb_client(test_settings) -> AsyncIOMotorClient:
    """
    Cliente de MongoDB para tests.
    Se crea una vez por sesión de tests.
    """
    client = AsyncIOMotorClient(test_settings.MONGODB_URL)
    yield client
    client.close()


@pytest.fixture
async def test_db(mongodb_client, test_settings):
    """
    Base de datos de test limpia.
    Se limpia antes y después de cada test.
    """
    db = mongodb_client[test_settings.MONGODB_DB_NAME]
    
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
        "location": "Test City"
    }


@pytest.fixture
def sample_skill_data():
    """Datos de ejemplo para Skill"""
    return {
        "name": "Python",
        "level": "expert",
        "category": "backend",
        "order_index": 0
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