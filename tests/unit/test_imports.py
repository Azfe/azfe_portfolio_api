# tests/unit/test_imports.py
"""
Tests básicos de importación para verificar que no hay dependencias circulares.
"""
import pytest


def test_import_main():
    """Test: Se puede importar main sin errores"""
    from app.main import app
    assert app is not None


def test_import_settings():
    """Test: Se puede importar settings sin errores"""
    from app.config.settings import settings
    assert settings is not None


def test_import_all_routers():
    """Test: Se pueden importar todos los routers"""
    from app.api.v1.routers import (
        health_router,
        profile_router,
        skill_router,
        cv_router
    )
    
    assert health_router.router is not None
    assert profile_router.router is not None
    assert skill_router.router is not None
    assert cv_router.router is not None


def test_import_all_schemas():
    """Test: Se pueden importar todos los schemas principales"""
    from app.api.schemas import (
        ProfileResponse,
        SkillResponse,
        CVCompleteResponse
    )
    
    assert ProfileResponse is not None
    assert SkillResponse is not None
    assert CVCompleteResponse is not None