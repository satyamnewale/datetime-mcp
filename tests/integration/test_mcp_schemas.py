import pytest

from fastmcp import Client
from server import mcp


@pytest.mark.contract
@pytest.mark.asyncio
async def test_tool_schemas_are_exposed():
    async with Client(mcp) as client:
        tools = await client.list_tools()

    tools_by_name = {tool.name: tool for tool in tools}

    assert "get_current_datetime" in tools_by_name
    assert "calculate_relative_datetime" in tools_by_name

    current_datetime = tools_by_name["get_current_datetime"]

    assert current_datetime.input_schema is not None
    assert "timezone" in current_datetime.input_schema["properties"]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_tool_descriptions_are_available():
    async with Client(mcp) as client:
        tools = await client.list_tools()

    for tool in tools:
        assert tool.description
        assert len(tool.description.strip()) > 10