"""Integration tests for AdditionalTrainingRepository against real MongoDB."""

from app.infrastructure.repositories import AdditionalTrainingRepository

from .conftest import PROFILE_ID, make_additional_training


class TestAdditionalTrainingRepositoryCRUD:
    async def test_add_and_retrieve(
        self, additional_training_repo: AdditionalTrainingRepository
    ):
        training = make_additional_training()
        await additional_training_repo.add(training)

        fetched = await additional_training_repo.get_by_id(training.id)
        assert fetched is not None
        assert fetched.title == "Docker Fundamentals"
        assert fetched.provider == "Udemy"

    async def test_add_with_optional_fields(
        self, additional_training_repo: AdditionalTrainingRepository
    ):
        training = make_additional_training(
            duration="40 hours",
            certificate_url="https://certificate.example.com/123",
            description="Complete Docker course",
        )
        await additional_training_repo.add(training)

        fetched = await additional_training_repo.get_by_id(training.id)
        assert fetched is not None
        assert fetched.duration == "40 hours"
        assert fetched.certificate_url == "https://certificate.example.com/123"

    async def test_update(self, additional_training_repo: AdditionalTrainingRepository):
        training = make_additional_training()
        await additional_training_repo.add(training)

        updated = make_additional_training(title="K8s Advanced", provider="Coursera")
        await additional_training_repo.update(updated)

        fetched = await additional_training_repo.get_by_id(training.id)
        assert fetched is not None
        assert fetched.title == "K8s Advanced"

    async def test_delete(self, additional_training_repo: AdditionalTrainingRepository):
        training = make_additional_training()
        await additional_training_repo.add(training)

        assert await additional_training_repo.delete(training.id) is True
        assert await additional_training_repo.get_by_id(training.id) is None

    async def test_delete_nonexistent(
        self, additional_training_repo: AdditionalTrainingRepository
    ):
        assert await additional_training_repo.delete("nonexistent") is False

    async def test_list_all(
        self, additional_training_repo: AdditionalTrainingRepository
    ):
        await additional_training_repo.add(
            make_additional_training(id="t1", order_index=0)
        )
        await additional_training_repo.add(
            make_additional_training(id="t2", order_index=1)
        )

        result = await additional_training_repo.list_all()
        assert len(result) == 2

    async def test_count(self, additional_training_repo: AdditionalTrainingRepository):
        assert await additional_training_repo.count() == 0
        await additional_training_repo.add(make_additional_training())
        assert await additional_training_repo.count() == 1

    async def test_exists(self, additional_training_repo: AdditionalTrainingRepository):
        training = make_additional_training()
        await additional_training_repo.add(training)

        assert await additional_training_repo.exists(training.id) is True
        assert await additional_training_repo.exists("nonexistent") is False


class TestAdditionalTrainingRepositoryOrdering:
    async def test_get_by_order_index(
        self, additional_training_repo: AdditionalTrainingRepository
    ):
        await additional_training_repo.add(
            make_additional_training(id="t1", order_index=0)
        )
        await additional_training_repo.add(
            make_additional_training(id="t2", order_index=1)
        )

        result = await additional_training_repo.get_by_order_index(PROFILE_ID, 1)
        assert result is not None
        assert result.id == "t2"

    async def test_get_all_ordered(
        self, additional_training_repo: AdditionalTrainingRepository
    ):
        await additional_training_repo.add(
            make_additional_training(id="t2", title="Beta", order_index=1)
        )
        await additional_training_repo.add(
            make_additional_training(id="t1", title="Alpha", order_index=0)
        )

        result = await additional_training_repo.get_all_ordered(
            PROFILE_ID, ascending=True
        )
        assert result[0].title == "Alpha"
        assert result[1].title == "Beta"

    async def test_reorder_move_down(
        self, additional_training_repo: AdditionalTrainingRepository
    ):
        await additional_training_repo.add(
            make_additional_training(id="t0", title="A", order_index=0)
        )
        await additional_training_repo.add(
            make_additional_training(id="t1", title="B", order_index=1)
        )
        await additional_training_repo.add(
            make_additional_training(id="t2", title="C", order_index=2)
        )

        await additional_training_repo.reorder(PROFILE_ID, "t0", 2)

        result = await additional_training_repo.get_all_ordered(PROFILE_ID)
        assert result[0].title == "B"
        assert result[1].title == "C"
        assert result[2].title == "A"

    async def test_reorder_move_up(
        self, additional_training_repo: AdditionalTrainingRepository
    ):
        await additional_training_repo.add(
            make_additional_training(id="t0", title="A", order_index=0)
        )
        await additional_training_repo.add(
            make_additional_training(id="t1", title="B", order_index=1)
        )
        await additional_training_repo.add(
            make_additional_training(id="t2", title="C", order_index=2)
        )

        await additional_training_repo.reorder(PROFILE_ID, "t2", 0)

        result = await additional_training_repo.get_all_ordered(PROFILE_ID)
        assert result[0].title == "C"
        assert result[1].title == "A"
        assert result[2].title == "B"
