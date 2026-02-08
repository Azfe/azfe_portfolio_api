"""Unit tests for ordered repositories: Education, Certification, AdditionalTraining, Project.

These all share the same IOrderedRepository pattern, so we test them together
using parametrize to avoid duplication.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.infrastructure.repositories.additional_training_repository import (
    AdditionalTrainingRepository,
)
from app.infrastructure.repositories.certification_repository import (
    CertificationRepository,
)
from app.infrastructure.repositories.education_repository import EducationRepository
from app.infrastructure.repositories.project_repository import ProjectRepository

from .conftest import (
    make_additional_training_doc,
    make_certification_doc,
    make_education_doc,
    make_project_doc,
)

# Parametrize: (RepositoryClass, doc_factory, entity_name_field, expected_value)
ORDERED_REPOS = [
    pytest.param(
        (EducationRepository, make_education_doc, "institution", "MIT"),
        id="education",
    ),
    pytest.param(
        (CertificationRepository, make_certification_doc, "title", "AWS SAA"),
        id="certification",
    ),
    pytest.param(
        (AdditionalTrainingRepository, make_additional_training_doc, "title", "Clean Architecture"),
        id="additional_training",
    ),
    pytest.param(
        (ProjectRepository, make_project_doc, "title", "My Project"),
        id="project",
    ),
]


@pytest.fixture(params=ORDERED_REPOS)
def repo_setup(request, mock_db):
    """Provides (repo, collection, doc_factory, field, expected_value) for each ordered repo."""
    repo_class, doc_factory, field, expected_value = request.param
    repo = repo_class(mock_db)
    return repo, repo._collection, doc_factory, field, expected_value


class TestOrderedRepositoryAdd:
    @pytest.mark.asyncio
    async def test_add_returns_entity(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        entity = MagicMock()
        entity.id = "test-1"

        result = await repo.add(entity)

        collection.insert_one.assert_called_once()
        assert result is entity


class TestOrderedRepositoryGetById:
    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo_setup):
        repo, collection, doc_factory, field, expected_value = repo_setup
        doc = doc_factory()
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_id(doc["_id"])

        assert result is not None
        assert getattr(result, field) == expected_value

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.find_one = AsyncMock(return_value=None)

        assert await repo.get_by_id("nonexistent") is None


class TestOrderedRepositoryUpdate:
    @pytest.mark.asyncio
    async def test_update(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        entity = MagicMock()
        entity.id = "test-1"

        result = await repo.update(entity)

        collection.replace_one.assert_called_once()
        assert result is entity


class TestOrderedRepositoryDelete:
    @pytest.mark.asyncio
    async def test_delete_found(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

        assert await repo.delete("test-1") is True

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))

        assert await repo.delete("nope") is False


class TestOrderedRepositoryListAll:
    @pytest.mark.asyncio
    async def test_list_all_empty(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=[])

        result = await repo.list_all()

        assert result == []

    @pytest.mark.asyncio
    async def test_list_all_with_docs(self, repo_setup):
        repo, collection, doc_factory, _, _ = repo_setup
        docs = [doc_factory(_id="a"), doc_factory(_id="b")]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.list_all()

        assert len(result) == 2


class TestOrderedRepositoryOrderMethods:
    @pytest.mark.asyncio
    async def test_get_by_order_index_found(self, repo_setup):
        repo, collection, doc_factory, _, _ = repo_setup
        doc = doc_factory(order_index=2)
        collection.find_one = AsyncMock(return_value=doc)

        result = await repo.get_by_order_index("profile-123", 2)

        collection.find_one.assert_called_once_with(
            {"profile_id": "profile-123", "order_index": 2}
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_get_by_order_index_not_found(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.find_one = AsyncMock(return_value=None)

        assert await repo.get_by_order_index("profile-123", 99) is None

    @pytest.mark.asyncio
    async def test_get_all_ordered(self, repo_setup):
        repo, collection, doc_factory, _, _ = repo_setup
        docs = [doc_factory(_id="a", order_index=0), doc_factory(_id="b", order_index=1)]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.get_all_ordered("profile-123")

        collection.find.assert_called_with({"profile_id": "profile-123"})
        cursor.sort.assert_called_once_with("order_index", 1)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_reorder_noop_on_same_index(self, repo_setup):
        repo, collection, doc_factory, _, _ = repo_setup
        doc = doc_factory(order_index=3)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", doc["_id"], 3)

        collection.update_many.assert_not_called()
        collection.update_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_reorder_noop_on_missing_entity(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.find_one = AsyncMock(return_value=None)

        await repo.reorder("profile-123", "nonexistent", 1)

        collection.update_many.assert_not_called()
        collection.update_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_reorder_move_down(self, repo_setup):
        repo, collection, doc_factory, _, _ = repo_setup
        doc = doc_factory(_id="item-1", order_index=1)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "item-1", 4)

        collection.update_many.assert_called_once_with(
            {"profile_id": "profile-123", "order_index": {"$gt": 1, "$lte": 4}},
            {"$inc": {"order_index": -1}},
        )
        collection.update_one.assert_called_once_with(
            {"_id": "item-1"}, {"$set": {"order_index": 4}}
        )

    @pytest.mark.asyncio
    async def test_reorder_move_up(self, repo_setup):
        repo, collection, doc_factory, _, _ = repo_setup
        doc = doc_factory(_id="item-1", order_index=4)
        collection.find_one = AsyncMock(return_value=doc)

        await repo.reorder("profile-123", "item-1", 1)

        collection.update_many.assert_called_once_with(
            {"profile_id": "profile-123", "order_index": {"$gte": 1, "$lt": 4}},
            {"$inc": {"order_index": 1}},
        )
        collection.update_one.assert_called_once_with(
            {"_id": "item-1"}, {"$set": {"order_index": 1}}
        )


class TestOrderedRepositoryCountExists:
    @pytest.mark.asyncio
    async def test_count(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.count_documents = AsyncMock(return_value=7)

        assert await repo.count() == 7

    @pytest.mark.asyncio
    async def test_count_with_filters(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.count_documents = AsyncMock(return_value=2)

        result = await repo.count({"profile_id": "p-1"})

        collection.count_documents.assert_called_once_with({"profile_id": "p-1"})
        assert result == 2

    @pytest.mark.asyncio
    async def test_exists_true(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.count_documents = AsyncMock(return_value=1)

        assert await repo.exists("id-1") is True

    @pytest.mark.asyncio
    async def test_exists_false(self, repo_setup):
        repo, collection, _, _, _ = repo_setup
        collection.count_documents = AsyncMock(return_value=0)

        assert await repo.exists("nope") is False

    @pytest.mark.asyncio
    async def test_find_by(self, repo_setup):
        repo, collection, doc_factory, _, _ = repo_setup
        docs = [doc_factory()]
        cursor = collection.find.return_value
        cursor.to_list = AsyncMock(return_value=docs)

        result = await repo.find_by(profile_id="profile-123")

        collection.find.assert_called_with({"profile_id": "profile-123"})
        assert len(result) == 1
