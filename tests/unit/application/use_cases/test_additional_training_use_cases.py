"""Tests for AdditionalTraining use cases."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    AddAdditionalTrainingRequest,
    DeleteAdditionalTrainingRequest,
    EditAdditionalTrainingRequest,
    ListAdditionalTrainingsRequest,
)
from app.application.use_cases.additional_training.add_additional_training import (
    AddAdditionalTrainingUseCase,
)
from app.application.use_cases.additional_training.delete_additional_training import (
    DeleteAdditionalTrainingUseCase,
)
from app.application.use_cases.additional_training.edit_additional_training import (
    EditAdditionalTrainingUseCase,
)
from app.application.use_cases.additional_training.list_additional_trainings import (
    ListAdditionalTrainingsUseCase,
)
from app.domain.entities.additional_training import AdditionalTraining
from app.shared.shared_exceptions import (
    BusinessRuleViolationException,
    NotFoundException,
)

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"
COMPLETION_DATE = datetime(2023, 6, 15)


def _make_training(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "title": "Python Advanced Course",
        "provider": "Udemy",
        "completion_date": COMPLETION_DATE,
        "order_index": 0,
    }
    defaults.update(overrides)
    return AdditionalTraining.create(**defaults)


class TestAddAdditionalTrainingUseCase:
    @pytest.mark.unit
    async def test_add_training_success(self):
        repo = AsyncMock()
        training = _make_training()
        repo.get_by_order_index.return_value = None
        repo.add.return_value = training

        uc = AddAdditionalTrainingUseCase(repo)
        request = AddAdditionalTrainingRequest(
            profile_id=PROFILE_ID,
            title="Python Advanced Course",
            provider="Udemy",
            completion_date=COMPLETION_DATE,
            order_index=0,
        )
        result = await uc.execute(request)

        assert result.title == "Python Advanced Course"
        assert result.provider == "Udemy"
        assert result.order_index == 0
        repo.get_by_order_index.assert_awaited_once_with(PROFILE_ID, 0)
        repo.add.assert_awaited_once()

    @pytest.mark.unit
    async def test_add_training_with_optional_fields(self):
        repo = AsyncMock()
        training = _make_training(
            duration="40 hours",
            certificate_url="https://example.com/cert",
            description="Advanced Python topics",
        )
        repo.get_by_order_index.return_value = None
        repo.add.return_value = training

        uc = AddAdditionalTrainingUseCase(repo)
        request = AddAdditionalTrainingRequest(
            profile_id=PROFILE_ID,
            title="Python Advanced Course",
            provider="Udemy",
            completion_date=COMPLETION_DATE,
            order_index=0,
            duration="40 hours",
            certificate_url="https://example.com/cert",
            description="Advanced Python topics",
        )
        result = await uc.execute(request)

        assert result.duration == "40 hours"
        assert result.certificate_url == "https://example.com/cert"
        assert result.description == "Advanced Python topics"

    @pytest.mark.unit
    @pytest.mark.business_rule
    async def test_add_training_duplicate_order_index_raises(self):
        repo = AsyncMock()
        repo.get_by_order_index.return_value = _make_training()

        uc = AddAdditionalTrainingUseCase(repo)
        request = AddAdditionalTrainingRequest(
            profile_id=PROFILE_ID,
            title="Another Course",
            provider="Coursera",
            completion_date=COMPLETION_DATE,
            order_index=0,
        )
        with pytest.raises(BusinessRuleViolationException):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    @pytest.mark.unit
    async def test_add_training_checks_order_index_for_correct_profile(self):
        repo = AsyncMock()
        repo.get_by_order_index.return_value = None
        repo.add.return_value = _make_training(order_index=3)

        uc = AddAdditionalTrainingUseCase(repo)
        request = AddAdditionalTrainingRequest(
            profile_id=PROFILE_ID,
            title="FastAPI Course",
            provider="Real Python",
            completion_date=COMPLETION_DATE,
            order_index=3,
        )
        await uc.execute(request)

        repo.get_by_order_index.assert_awaited_once_with(PROFILE_ID, 3)


class TestDeleteAdditionalTrainingUseCase:
    @pytest.mark.unit
    async def test_delete_training_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteAdditionalTrainingUseCase(repo)
        result = await uc.execute(
            DeleteAdditionalTrainingRequest(training_id="training-001")
        )

        assert result.success is True
        repo.delete.assert_awaited_once_with("training-001")

    @pytest.mark.unit
    async def test_delete_training_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteAdditionalTrainingUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(
                DeleteAdditionalTrainingRequest(training_id="nonexistent")
            )


class TestEditAdditionalTrainingUseCase:
    @pytest.mark.unit
    async def test_edit_training_success(self):
        repo = AsyncMock()
        training = _make_training()
        repo.get_by_id.return_value = training
        repo.update.return_value = training

        uc = EditAdditionalTrainingUseCase(repo)
        request = EditAdditionalTrainingRequest(
            training_id="training-001",
            title="Updated Course Title",
        )
        result = await uc.execute(request)

        assert result.title == "Updated Course Title"
        repo.get_by_id.assert_awaited_once_with("training-001")
        repo.update.assert_awaited_once()

    @pytest.mark.unit
    async def test_edit_training_updates_multiple_fields(self):
        repo = AsyncMock()
        training = _make_training()
        repo.get_by_id.return_value = training
        repo.update.return_value = training

        uc = EditAdditionalTrainingUseCase(repo)
        request = EditAdditionalTrainingRequest(
            training_id="training-001",
            title="New Title",
            provider="New Provider",
            duration="20 hours",
        )
        result = await uc.execute(request)

        assert result.title == "New Title"
        assert result.provider == "New Provider"
        assert result.duration == "20 hours"

    @pytest.mark.unit
    async def test_edit_training_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditAdditionalTrainingUseCase(repo)
        request = EditAdditionalTrainingRequest(
            training_id="nonexistent",
            title="Updated Title",
        )
        with pytest.raises(NotFoundException):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    @pytest.mark.unit
    async def test_edit_training_partial_update_preserves_existing_fields(self):
        repo = AsyncMock()
        training = _make_training(
            title="Original Title",
            provider="Original Provider",
            duration="30 hours",
        )
        repo.get_by_id.return_value = training
        repo.update.return_value = training

        uc = EditAdditionalTrainingUseCase(repo)
        request = EditAdditionalTrainingRequest(
            training_id="training-001",
            title="New Title",
        )
        result = await uc.execute(request)

        assert result.title == "New Title"
        assert result.provider == "Original Provider"
        assert result.duration == "30 hours"


class TestListAdditionalTrainingsUseCase:
    @pytest.mark.unit
    async def test_list_trainings_returns_empty_list(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = ListAdditionalTrainingsUseCase(repo)
        result = await uc.execute(
            ListAdditionalTrainingsRequest(profile_id=PROFILE_ID)
        )

        assert result.trainings == []
        assert result.total == 0
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    @pytest.mark.unit
    async def test_list_trainings_returns_all_items(self):
        repo = AsyncMock()
        trainings = [
            _make_training(title="Course A", order_index=0),
            _make_training(title="Course B", order_index=1),
            _make_training(title="Course C", order_index=2),
        ]
        repo.find_by.return_value = trainings

        uc = ListAdditionalTrainingsUseCase(repo)
        result = await uc.execute(
            ListAdditionalTrainingsRequest(profile_id=PROFILE_ID)
        )

        assert result.total == 3
        assert len(result.trainings) == 3

    @pytest.mark.unit
    async def test_list_trainings_sorted_ascending_by_default(self):
        repo = AsyncMock()
        trainings = [
            _make_training(title="Course C", order_index=2),
            _make_training(title="Course A", order_index=0),
            _make_training(title="Course B", order_index=1),
        ]
        repo.find_by.return_value = trainings

        uc = ListAdditionalTrainingsUseCase(repo)
        result = await uc.execute(
            ListAdditionalTrainingsRequest(profile_id=PROFILE_ID, ascending=True)
        )

        order_indices = [t.order_index for t in result.trainings]
        assert order_indices == sorted(order_indices)

    @pytest.mark.unit
    async def test_list_trainings_sorted_descending_when_requested(self):
        repo = AsyncMock()
        trainings = [
            _make_training(title="Course A", order_index=0),
            _make_training(title="Course B", order_index=1),
            _make_training(title="Course C", order_index=2),
        ]
        repo.find_by.return_value = trainings

        uc = ListAdditionalTrainingsUseCase(repo)
        result = await uc.execute(
            ListAdditionalTrainingsRequest(profile_id=PROFILE_ID, ascending=False)
        )

        order_indices = [t.order_index for t in result.trainings]
        assert order_indices == sorted(order_indices, reverse=True)
