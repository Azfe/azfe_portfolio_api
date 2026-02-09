"""Shared fixtures for repository unit tests."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_collection():
    """Creates a mock MongoDB collection with async methods."""
    collection = MagicMock()
    collection.insert_one = AsyncMock()
    collection.replace_one = AsyncMock()
    collection.delete_one = AsyncMock()
    collection.find_one = AsyncMock()
    collection.count_documents = AsyncMock()
    collection.update_one = AsyncMock()
    collection.update_many = AsyncMock()

    # find() returns a chainable cursor mock
    cursor = MagicMock()
    cursor.skip = MagicMock(return_value=cursor)
    cursor.limit = MagicMock(return_value=cursor)
    cursor.sort = MagicMock(return_value=cursor)
    cursor.to_list = AsyncMock(return_value=[])
    collection.find = MagicMock(return_value=cursor)

    return collection


@pytest.fixture
def mock_db(mock_collection):
    """Creates a mock AsyncIOMotorDatabase that returns the mock collection."""
    db = MagicMock()
    db.__getitem__ = MagicMock(return_value=mock_collection)
    return db


def make_profile_doc(
    _id="profile-123",
    name="John Doe",
    headline="Developer",
    bio=None,
    location=None,
    avatar_url=None,
):
    """Helper to create a profile MongoDB document."""
    doc = {
        "_id": _id,
        "name": name,
        "headline": headline,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }
    if bio is not None:
        doc["bio"] = bio
    if location is not None:
        doc["location"] = location
    if avatar_url is not None:
        doc["avatar_url"] = avatar_url
    return doc


def make_work_experience_doc(
    _id="exp-123",
    profile_id="profile-123",
    role="Developer",
    company="Acme",
    order_index=0,
):
    """Helper to create a work experience MongoDB document."""
    return {
        "_id": _id,
        "profile_id": profile_id,
        "role": role,
        "company": company,
        "start_date": datetime(2021, 1, 1),
        "order_index": order_index,
        "responsibilities": [],
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }


def make_skill_doc(
    _id="skill-123",
    profile_id="profile-123",
    name="Python",
    category="backend",
    level="expert",
    order_index=0,
):
    """Helper to create a skill MongoDB document."""
    doc = {
        "_id": _id,
        "profile_id": profile_id,
        "name": name,
        "category": category,
        "order_index": order_index,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }
    if level is not None:
        doc["level"] = level
    return doc


def make_contact_info_doc(
    _id="contact-123",
    profile_id="profile-123",
    email="test@example.com",
):
    """Helper to create a contact information MongoDB document."""
    return {
        "_id": _id,
        "profile_id": profile_id,
        "email": email,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }


def make_contact_message_doc(
    _id="msg-123",
    name="Jane Doe",
    email="jane@example.com",
    message="Hello, this is a test message for contact.",
    status="pending",
):
    """Helper to create a contact message MongoDB document."""
    doc = {
        "_id": _id,
        "name": name,
        "email": email,
        "message": message,
        "status": status,
        "created_at": datetime(2025, 1, 15),
    }
    return doc


def make_education_doc(
    _id="edu-123",
    profile_id="profile-123",
    institution="MIT",
    degree="CS",
    field="Computer Science",
    order_index=0,
):
    """Helper to create an education MongoDB document."""
    return {
        "_id": _id,
        "profile_id": profile_id,
        "institution": institution,
        "degree": degree,
        "field": field,
        "start_date": datetime(2015, 9, 1),
        "order_index": order_index,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }


def make_certification_doc(
    _id="cert-123",
    profile_id="profile-123",
    title="AWS SAA",
    issuer="Amazon",
    order_index=0,
):
    """Helper to create a certification MongoDB document."""
    return {
        "_id": _id,
        "profile_id": profile_id,
        "title": title,
        "issuer": issuer,
        "issue_date": datetime(2023, 6, 15),
        "order_index": order_index,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }


def make_additional_training_doc(
    _id="train-123",
    profile_id="profile-123",
    title="Clean Architecture",
    provider="Udemy",
    order_index=0,
):
    """Helper to create an additional training MongoDB document."""
    return {
        "_id": _id,
        "profile_id": profile_id,
        "title": title,
        "provider": provider,
        "completion_date": datetime(2023, 4, 15),
        "order_index": order_index,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }


def make_programming_language_doc(
    _id="pl-123",
    profile_id="profile-123",
    name="Python",
    order_index=0,
):
    """Helper to create a programming language MongoDB document."""
    doc = {
        "_id": _id,
        "profile_id": profile_id,
        "name": name,
        "order_index": order_index,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }
    return doc


def make_language_doc(
    _id="lang-123",
    profile_id="profile-123",
    name="English",
    order_index=0,
):
    """Helper to create a language MongoDB document."""
    doc = {
        "_id": _id,
        "profile_id": profile_id,
        "name": name,
        "order_index": order_index,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }
    return doc


def make_project_doc(
    _id="proj-123",
    profile_id="profile-123",
    title="My Project",
    description="A comprehensive test project description that needs to be at least one hundred characters long for validation to pass correctly.",
    order_index=0,
):
    """Helper to create a project MongoDB document."""
    return {
        "_id": _id,
        "profile_id": profile_id,
        "title": title,
        "description": description,
        "start_date": datetime(2024, 1, 1),
        "technologies": [],
        "order_index": order_index,
        "created_at": datetime(2025, 1, 1),
        "updated_at": datetime(2025, 1, 1),
    }
