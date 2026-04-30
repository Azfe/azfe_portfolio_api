"""Tests for AdditionalTraining DTOs."""

import pytest

from app.application.dto.additional_training_dto import (
    AdditionalTrainingListResponse,
    AdditionalTrainingResponse,
)

from .conftest import DT, DT2, DT_END, DT_START, make_entity


def _make_additional_training_entity(**overrides):
    defaults = {
        "id": "at-1",
        "profile_id": "p-1",
        "title": "Python for Data Science",
        "provider": "Coursera",
        "completion_date": DT_END,
        "order_index": 0,
        "duration": "40 hours",
        "certificate_url": "https://coursera.org/cert/abc123",
        "description": "Comprehensive Python course for data science.",
    }
    defaults.update(overrides)
    return make_entity(**defaults)


class TestAdditionalTrainingResponseFromEntity:
    @pytest.mark.unit
    def test_maps_all_fields(self):
        entity = _make_additional_training_entity()
        resp = AdditionalTrainingResponse.from_entity(entity)

        assert resp.id == "at-1"
        assert resp.profile_id == "p-1"
        assert resp.title == "Python for Data Science"
        assert resp.provider == "Coursera"
        assert resp.completion_date == DT_END
        assert resp.order_index == 0
        assert resp.duration == "40 hours"
        assert resp.certificate_url == "https://coursera.org/cert/abc123"
        assert resp.description == "Comprehensive Python course for data science."
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_none_optional_fields(self):
        entity = _make_additional_training_entity(
            duration=None,
            certificate_url=None,
            description=None,
        )
        resp = AdditionalTrainingResponse.from_entity(entity)

        assert resp.duration is None
        assert resp.certificate_url is None
        assert resp.description is None

    @pytest.mark.unit
    def test_required_fields_always_present(self):
        entity = _make_additional_training_entity(
            duration=None,
            certificate_url=None,
            description=None,
        )
        resp = AdditionalTrainingResponse.from_entity(entity)

        assert resp.id == "at-1"
        assert resp.profile_id == "p-1"
        assert resp.title == "Python for Data Science"
        assert resp.provider == "Coursera"
        assert resp.completion_date == DT_END
        assert resp.order_index == 0

    @pytest.mark.unit
    def test_returns_correct_type(self):
        entity = _make_additional_training_entity()
        resp = AdditionalTrainingResponse.from_entity(entity)

        assert isinstance(resp, AdditionalTrainingResponse)

    @pytest.mark.unit
    def test_timestamps_preserved(self):
        entity = _make_additional_training_entity()
        resp = AdditionalTrainingResponse.from_entity(entity)

        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_different_order_index(self):
        entity = _make_additional_training_entity(order_index=5)
        resp = AdditionalTrainingResponse.from_entity(entity)

        assert resp.order_index == 5

    @pytest.mark.unit
    def test_completion_date_preserved(self):
        entity = _make_additional_training_entity(completion_date=DT_START)
        resp = AdditionalTrainingResponse.from_entity(entity)

        assert resp.completion_date == DT_START


class TestAdditionalTrainingListResponseFromEntities:
    @pytest.mark.unit
    def test_maps_list(self):
        entities = [
            _make_additional_training_entity(id="at-1", title="Python for Data Science"),
            _make_additional_training_entity(id="at-2", title="Machine Learning A-Z"),
        ]
        resp = AdditionalTrainingListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.trainings) == 2

    @pytest.mark.unit
    def test_items_are_correctly_mapped(self):
        entities = [
            _make_additional_training_entity(id="at-1", title="Python for Data Science"),
            _make_additional_training_entity(id="at-2", title="Machine Learning A-Z"),
        ]
        resp = AdditionalTrainingListResponse.from_entities(entities)

        assert resp.trainings[0].title == "Python for Data Science"
        assert resp.trainings[1].title == "Machine Learning A-Z"

    @pytest.mark.unit
    def test_empty_list(self):
        resp = AdditionalTrainingListResponse.from_entities([])

        assert resp.total == 0
        assert resp.trainings == []

    @pytest.mark.unit
    def test_returns_correct_type(self):
        resp = AdditionalTrainingListResponse.from_entities([])

        assert isinstance(resp, AdditionalTrainingListResponse)

    @pytest.mark.unit
    def test_single_item_list(self):
        entities = [_make_additional_training_entity(id="at-1")]
        resp = AdditionalTrainingListResponse.from_entities(entities)

        assert resp.total == 1
        assert len(resp.trainings) == 1
        assert isinstance(resp.trainings[0], AdditionalTrainingResponse)
