import pytest
from fastmcp.exceptions import ToolError
from fastmcp import Client

from server import mcp


EXPECTED_TOOLS = {
    "get_current_datetime",
    "get_current_date",
    "get_current_time",
    "get_timezone_info",
    "calculate_relative_date",
    "calculate_relative_datetime",
    "get_previous_n_days",
    "get_next_n_days",
    "get_week_dates",
    "get_date_range",
    "parse_natural_datetime",
    "get_month_dates",
    "calculate_date_difference",
    "calculate_time_difference",
}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_all_tools_registered():
    async with Client(mcp) as client:
        tools = await client.list_tools()

    registered_tools = {tool.name for tool in tools}

    assert registered_tools == EXPECTED_TOOLS


@pytest.mark.integration
@pytest.mark.asyncio
async def test_current_datetime_tool(frozen_time):
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_current_datetime",
            {"timezone": "Asia/Kolkata"}
        )

    assert result.structured_content is not None
    assert result.structured_content["date"] == "2026-11-05"
    assert result.structured_content["time"] == "15:30:00"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_relative_date_tool(frozen_time):
    async with Client(mcp) as client:
        result = await client.call_tool(
            "calculate_relative_date",
            {
                "amount": 15,
                "unit": "days",
                "direction": "future",
                "timezone": "Asia/Kolkata",
            }
        )

    assert result.structured_content is not None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_invalid_timezone_tool():
    async with Client(mcp) as client:

        with pytest.raises(ToolError) as exc_info:
            await client.call_tool(
                "get_current_datetime",
                {"timezone": "Invalid/Timezone"},
            )

        assert "Invalid/Timezone" in str(exc_info.value)