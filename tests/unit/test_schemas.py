# tests/unit/test_schemas.py
"""
Tests unitarios para los schemas de Pydantic.
"""

from pydantic import ValidationError
import pytest

from app.api.schemas.profile_schema import ProfileCreate
from app.api.schemas.skill_schema import SkillCreate


class TestProfileSchema:
    """Tests para Profile schemas"""

    def test_profile_create_valid(self):
        """Test: ProfileCreate se crea con datos válidos"""
        data = {
            "name": "John Doe",
            "headline": "Software Engineer",
            "bio": "Experienced developer",
            "location": "New York",
        }
        profile = ProfileCreate(**data)

        assert profile.name == "John Doe"
        assert profile.headline == "Software Engineer"

    def test_profile_create_missing_required_field(self):
        """Test: ProfileCreate falla sin campos requeridos"""
        data = {
            "name": "John Doe"
            # Falta 'headline' que es requerido
        }

        with pytest.raises(ValidationError) as exc_info:
            ProfileCreate(**data)

        assert "headline" in str(exc_info.value)

    def test_profile_create_empty_name(self):
        """Test: ProfileCreate falla con nombre vacío"""
        data = {"name": "", "headline": "Developer"}  # Vacío, debería fallar

        with pytest.raises(ValidationError):
            ProfileCreate(**data)


class TestSkillSchema:
    """Tests para Skill schemas"""

    def test_skill_create_valid(self):
        """Test: SkillCreate se crea con datos válidos"""
        data = {
            "name": "Python",
            "level": "expert",
            "category": "backend",
            "order_index": 0,
        }
        skill = SkillCreate(**data)

        assert skill.name == "Python"
        assert skill.level == "expert"
        assert skill.category == "backend"

    def test_skill_create_invalid_level(self):
        """Test: SkillCreate falla con nivel inválido"""
        data = {
            "name": "Python",
            "level": "master",  # No es un nivel válido
            "category": "backend",
            "order_index": 0,
        }

        with pytest.raises(ValidationError) as exc_info:
            SkillCreate(**data)

        assert "level" in str(exc_info.value)

    def test_skill_create_free_category(self):
        """Test: SkillCreate acepta cualquier string como categoría"""
        data = {
            "name": "Python",
            "level": "expert",
            "category": "programming",
            "order_index": 0,
        }
        skill = SkillCreate(**data)
        assert skill.category == "programming"

    @pytest.mark.parametrize("level", ["basic", "intermediate", "advanced", "expert"])
    def test_skill_all_valid_levels(self, level):
        """Test: SkillCreate acepta todos los niveles válidos"""
        data = {
            "name": "Python",
            "level": level,
            "category": "backend",
            "order_index": 0,
        }
        skill = SkillCreate(**data)
        assert skill.level == level
