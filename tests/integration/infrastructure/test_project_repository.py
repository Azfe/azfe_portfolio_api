"""Integration tests for ProjectRepository against real MongoDB."""

from app.infrastructure.repositories import ProjectRepository

from .conftest import PROFILE_ID, make_project


class TestProjectRepositoryCRUD:
    async def test_add_and_retrieve(self, project_repo: ProjectRepository):
        proj = make_project()
        await project_repo.add(proj)

        fetched = await project_repo.get_by_id(proj.id)
        assert fetched is not None
        assert fetched.title == "Portfolio Website"
        assert fetched.profile_id == PROFILE_ID

    async def test_add_with_optional_fields(self, project_repo: ProjectRepository):
        proj = make_project(
            technologies=["Python", "FastAPI"],
            repo_url="https://github.com/user/repo",
        )
        await project_repo.add(proj)

        fetched = await project_repo.get_by_id(proj.id)
        assert fetched is not None
        assert fetched.technologies == ["Python", "FastAPI"]
        assert fetched.repo_url == "https://github.com/user/repo"

    async def test_update(self, project_repo: ProjectRepository):
        proj = make_project()
        await project_repo.add(proj)

        updated = make_project(
            title="Updated Portfolio",
            description="An updated portfolio project with new features and improvements",
        )
        await project_repo.update(updated)

        fetched = await project_repo.get_by_id(proj.id)
        assert fetched is not None
        assert fetched.title == "Updated Portfolio"

    async def test_delete(self, project_repo: ProjectRepository):
        proj = make_project()
        await project_repo.add(proj)

        assert await project_repo.delete(proj.id) is True
        assert await project_repo.get_by_id(proj.id) is None

    async def test_delete_nonexistent(self, project_repo: ProjectRepository):
        assert await project_repo.delete("nonexistent") is False

    async def test_list_all(self, project_repo: ProjectRepository):
        await project_repo.add(make_project(id="p1", order_index=0))
        await project_repo.add(make_project(id="p2", order_index=1))

        result = await project_repo.list_all()
        assert len(result) == 2

    async def test_count(self, project_repo: ProjectRepository):
        assert await project_repo.count() == 0
        await project_repo.add(make_project())
        assert await project_repo.count() == 1

    async def test_exists(self, project_repo: ProjectRepository):
        proj = make_project()
        await project_repo.add(proj)

        assert await project_repo.exists(proj.id) is True
        assert await project_repo.exists("nonexistent") is False


class TestProjectRepositoryOrdering:
    async def test_get_by_order_index(self, project_repo: ProjectRepository):
        await project_repo.add(make_project(id="p1", order_index=0))
        await project_repo.add(make_project(id="p2", order_index=1))

        result = await project_repo.get_by_order_index(PROFILE_ID, 1)
        assert result is not None
        assert result.id == "p2"

    async def test_get_all_ordered(self, project_repo: ProjectRepository):
        await project_repo.add(make_project(id="p2", title="Beta", order_index=1))
        await project_repo.add(make_project(id="p1", title="Alpha", order_index=0))

        result = await project_repo.get_all_ordered(PROFILE_ID, ascending=True)
        assert result[0].title == "Alpha"
        assert result[1].title == "Beta"

    async def test_reorder_move_down(self, project_repo: ProjectRepository):
        await project_repo.add(make_project(id="p0", title="A", order_index=0))
        await project_repo.add(make_project(id="p1", title="B", order_index=1))
        await project_repo.add(make_project(id="p2", title="C", order_index=2))

        await project_repo.reorder(PROFILE_ID, "p0", 2)

        result = await project_repo.get_all_ordered(PROFILE_ID)
        assert result[0].title == "B"
        assert result[1].title == "C"
        assert result[2].title == "A"

    async def test_reorder_move_up(self, project_repo: ProjectRepository):
        await project_repo.add(make_project(id="p0", title="A", order_index=0))
        await project_repo.add(make_project(id="p1", title="B", order_index=1))
        await project_repo.add(make_project(id="p2", title="C", order_index=2))

        await project_repo.reorder(PROFILE_ID, "p2", 0)

        result = await project_repo.get_all_ordered(PROFILE_ID)
        assert result[0].title == "C"
        assert result[1].title == "A"
        assert result[2].title == "B"
