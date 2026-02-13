"""Shared fixtures for DTO unit tests."""

from datetime import datetime
from unittest.mock import MagicMock

DT = datetime(2025, 1, 1, 12, 0, 0)
DT2 = datetime(2025, 6, 15, 10, 30, 0)
DT_START = datetime(2024, 1, 1)
DT_END = datetime(2024, 12, 31)


def make_entity(**overrides):
    """Create a generic mock entity with common timestamp fields."""
    entity = MagicMock()
    entity.created_at = overrides.pop("created_at", DT)
    entity.updated_at = overrides.pop("updated_at", DT2)
    for key, value in overrides.items():
        setattr(entity, key, value)
    return entity
