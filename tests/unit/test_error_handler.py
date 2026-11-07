
import pytest

from fastmcp import Client
from fastmcp.exceptions import ToolError

from server import mcp


@pytest.mark.integration
@pytest.mark.asyncio
async def test_invalid_timezone_tool():

    async with Client(mcp) as client:

        with pytest.raises(ToolError) as exc_info:
            await client.call_tool(
                "get_current_datetime",
                {"timezone": "Invalid/Timezone"},
            )

    error_message = str(exc_info.value)

    assert "Invalid/Timezone" in error_message
    assert "Traceback" not in error_message
