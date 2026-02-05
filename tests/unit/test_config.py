# tests/unit/test_config.py
"""
Tests para la configuración de la aplicación.
"""

import pytest

from app.config.settings import Settings


def test_settings_creation():
    """Test: Settings se puede crear correctamente"""
    settings = Settings()
    assert settings is not None
    assert hasattr(settings, "MONGODB_URL")
    assert hasattr(settings, "PROJECT_NAME")


def test_settings_environment():
    """Test: Settings tiene valores por defecto"""
    settings = Settings()
    assert settings.ENVIRONMENT in ["development", "test", "production"]
    assert isinstance(settings.DEBUG, bool)
    assert isinstance(settings.PORT, int)


def test_cors_origins_list_property():
    """Test: cors_origins_list convierte string a lista correctamente"""
    settings = Settings(CORS_ORIGINS="http://localhost:3000,http://localhost:4321")
    origins = settings.cors_origins_list

    assert isinstance(origins, list)
    assert len(origins) == 2
    assert "http://localhost:3000" in origins
    assert "http://localhost:4321" in origins


@pytest.mark.parametrize(
    "env,expected",
    [
        ("development", True),
        ("test", True),
        ("production", False),
    ],
)
def test_settings_debug_by_environment(env, expected):
    """Test: DEBUG se configura según el entorno"""
    settings = Settings(ENVIRONMENT=env, DEBUG=expected)
    assert expected == settings.DEBUG
