"""Tests for Tool use cases."""

from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    AddToolRequest,
    DeleteToolRequest,
    EditToolRequest,
    ListToolsRequest,
)
from app.application.use_cases.tool.add_tool import AddToolUseCase
from app.application.use_cases.tool.delete_tool import DeleteToolUseCase
from app.application.use_cases.tool.edit_tool import EditToolUseCase
from app.application.use_cases.tool.list_tools import ListToolsUseCase
from app.domain.entities.tool import Tool
from app.shared.shared_exceptions import DuplicateException, NotFoundException

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"


def _make_tool(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "name": "Docker",
        "order_index": 0,
        "category": "Container",
        "icon_url": None,
    }
    defaults.update(overrides)
    return Tool.create(**defaults)


class TestAddToolUseCase:
    @pytest.mark.unit
    async def test_add_tool_success(self):
        repo = AsyncMock()
        tool = _make_tool()
        repo.exists_by_name.return_value = False
        repo.add.return_value = tool

        uc = AddToolUseCase(repo)
        request = AddToolRequest(
            profile_id=PROFILE_ID,
            name="Docker",
            order_index=0,
            category="Container",
        )
        result = await uc.execute(request)

        assert result.name == "Docker"
        assert result.category == "Container"
        assert result.profile_id == PROFILE_ID
        repo.exists_by_name.assert_awaited_once_with(PROFILE_ID, "Docker")
        repo.add.assert_awaited_once()

    @pytest.mark.unit
    async def test_add_tool_with_icon_url(self):
        repo = AsyncMock()
        tool = _make_tool(icon_url="https://example.com/docker.png")
        repo.exists_by_name.return_value = False
        repo.add.return_value = tool

        uc = AddToolUseCase(repo)
        request = AddToolRequest(
            profile_id=PROFILE_ID,
            name="Docker",
            order_index=0,
            icon_url="https://example.com/docker.png",
        )
        result = await uc.execute(request)

        assert result.icon_url == "https://example.com/docker.png"
        repo.add.assert_awaited_once()

    @pytest.mark.unit
    async def test_add_tool_without_category(self):
        repo = AsyncMock()
        tool = _make_tool(category=None)
        repo.exists_by_name.return_value = False
        repo.add.return_value = tool

        uc = AddToolUseCase(repo)
        request = AddToolRequest(
            profile_id=PROFILE_ID,
            name="Docker",
            order_index=0,
        )
        result = await uc.execute(request)

        assert result.category is None
        repo.add.assert_awaited_once()

    @pytest.mark.unit
    async def test_add_tool_duplicate_name_raises(self):
        repo = AsyncMock()
        repo.exists_by_name.return_value = True

        uc = AddToolUseCase(repo)
        request = AddToolRequest(
            profile_id=PROFILE_ID,
            name="Docker",
            order_index=0,
        )
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.add.assert_not_awaited()


class TestDeleteToolUseCase:
    @pytest.mark.unit
    async def test_delete_tool_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteToolUseCase(repo)
        result = await uc.execute(DeleteToolRequest(tool_id="tool-001"))

        assert result.success is True
        repo.delete.assert_awaited_once_with("tool-001")

    @pytest.mark.unit
    async def test_delete_tool_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteToolUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(DeleteToolRequest(tool_id="nonexistent"))


class TestEditToolUseCase:
    @pytest.mark.unit
    async def test_edit_tool_success(self):
        repo = AsyncMock()
        tool = _make_tool()
        repo.get_by_id.return_value = tool
        repo.exists_by_name.return_value = False
        repo.update.return_value = tool

        uc = EditToolUseCase(repo)
        request = EditToolRequest(tool_id="tool-001", name="Podman")
        result = await uc.execute(request)

        assert result.name == "Podman"
        repo.get_by_id.assert_awaited_once_with("tool-001")
        repo.update.assert_awaited_once()

    @pytest.mark.unit
    async def test_edit_tool_change_category(self):
        repo = AsyncMock()
        tool = _make_tool()
        repo.get_by_id.return_value = tool
        repo.update.return_value = tool

        uc = EditToolUseCase(repo)
        request = EditToolRequest(tool_id="tool-001", category="Orchestration")
        await uc.execute(request)

        repo.update.assert_awaited_once()
        repo.exists_by_name.assert_not_awaited()

    @pytest.mark.unit
    async def test_edit_tool_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditToolUseCase(repo)
        request = EditToolRequest(tool_id="nonexistent", name="Podman")
        with pytest.raises(NotFoundException):
            await uc.execute(request)

    @pytest.mark.unit
    async def test_edit_tool_duplicate_name_raises(self):
        repo = AsyncMock()
        tool = _make_tool()
        repo.get_by_id.return_value = tool
        repo.exists_by_name.return_value = True

        uc = EditToolUseCase(repo)
        request = EditToolRequest(tool_id="tool-001", name="Kubernetes")
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    @pytest.mark.unit
    async def test_edit_tool_same_name_no_duplicate_check(self):
        repo = AsyncMock()
        tool = _make_tool()
        repo.get_by_id.return_value = tool
        repo.update.return_value = tool

        uc = EditToolUseCase(repo)
        # Passing the same name as the existing tool should not trigger exists_by_name
        request = EditToolRequest(tool_id="tool-001", name="Docker")
        await uc.execute(request)

        repo.exists_by_name.assert_not_awaited()
        repo.update.assert_awaited_once()


class TestListToolsUseCase:
    @pytest.mark.unit
    async def test_list_tools_empty(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = ListToolsUseCase(repo)
        request = ListToolsRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 0
        assert result.tools == []
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    @pytest.mark.unit
    async def test_list_tools_returns_all(self):
        repo = AsyncMock()
        tools = [
            _make_tool(name="Docker", order_index=0, category="Container"),
            _make_tool(name="PostgreSQL", order_index=1, category="Database"),
        ]
        repo.find_by.return_value = tools

        uc = ListToolsUseCase(repo)
        request = ListToolsRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 2
        assert len(result.tools) == 2
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    @pytest.mark.unit
    async def test_list_tools_filter_by_category(self):
        repo = AsyncMock()
        tools = [_make_tool(name="PostgreSQL", order_index=0, category="Database")]
        repo.find_by.return_value = tools

        uc = ListToolsUseCase(repo)
        request = ListToolsRequest(profile_id=PROFILE_ID, category="Database")
        result = await uc.execute(request)

        assert result.total == 1
        assert result.tools[0].name == "PostgreSQL"
        repo.find_by.assert_awaited_once_with(
            profile_id=PROFILE_ID, category="Database"
        )

    @pytest.mark.unit
    async def test_list_tools_sorted_ascending_by_order_index(self):
        repo = AsyncMock()
        # Return tools out of order
        tools = [
            _make_tool(name="Redis", order_index=2, category="Cache"),
            _make_tool(name="Docker", order_index=0, category="Container"),
            _make_tool(name="PostgreSQL", order_index=1, category="Database"),
        ]
        repo.find_by.return_value = tools

        uc = ListToolsUseCase(repo)
        request = ListToolsRequest(profile_id=PROFILE_ID, ascending=True)
        result = await uc.execute(request)

        assert [t.name for t in result.tools] == ["Docker", "PostgreSQL", "Redis"]

    @pytest.mark.unit
    async def test_list_tools_sorted_descending_by_order_index(self):
        repo = AsyncMock()
        tools = [
            _make_tool(name="Docker", order_index=0, category="Container"),
            _make_tool(name="PostgreSQL", order_index=1, category="Database"),
            _make_tool(name="Redis", order_index=2, category="Cache"),
        ]
        repo.find_by.return_value = tools

        uc = ListToolsUseCase(repo)
        request = ListToolsRequest(profile_id=PROFILE_ID, ascending=False)
        result = await uc.execute(request)

        assert [t.name for t in result.tools] == ["Redis", "PostgreSQL", "Docker"]
