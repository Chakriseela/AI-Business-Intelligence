import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SERVER_PATH = (
    PROJECT_ROOT
    / "backend"
    / "mcp_server"
    / "server.py"
)


# ---------------------------------------------------------
# MCP Server configuration
# ---------------------------------------------------------

server_params = StdioServerParameters(
    command=sys.executable,
    args=[str(SERVER_PATH)],
)


# ---------------------------------------------------------
# MCP Client
# ---------------------------------------------------------

class MCPClient:

    def __init__(self):
        self.read = None
        self.write = None
        self.session = None

        self._stdio_context = None
        self._session_context = None

    # -----------------------------------------------------
    # Connect
    # -----------------------------------------------------

    async def connect(self):

        self._stdio_context = stdio_client(
            server_params
        )

        self.read, self.write = (
            await self._stdio_context.__aenter__()
        )

        self._session_context = ClientSession(
            self.read,
            self.write,
        )

        self.session = (
            await self._session_context.__aenter__()
        )

        await self.session.initialize()

    # -----------------------------------------------------
    # Discover tools
    # -----------------------------------------------------

    async def list_tools(self) -> list[dict[str, Any]]:

        if self.session is None:
            raise RuntimeError(
                "MCP client is not connected."
            )

        result = await self.session.list_tools()

        tools = []

        for tool in result.tools:

            tools.append(
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "input_schema": tool.inputSchema,
                }
            )

        return tools

    # -----------------------------------------------------
    # Call MCP tool
    # -----------------------------------------------------

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:

        if self.session is None:
            raise RuntimeError(
                "MCP client is not connected."
            )

        result = await self.session.call_tool(
            tool_name,
            arguments=arguments,
        )

        response = {
            "tool_name": tool_name,
            "content": [],
            "structured_content": None,
            "is_error": getattr(
                result,
                "isError",
                False,
            ),
        }

        # -------------------------------------------------
        # Read MCP structured content
        # -------------------------------------------------

        structured_content = getattr(
            result,
            "structuredContent",
            None,
        )

        if structured_content is not None:

            response["structured_content"] = (
                structured_content
            )

        # -------------------------------------------------
        # Read MCP text content
        # -------------------------------------------------

        if result.content:

            for content in result.content:

                if hasattr(content, "text"):

                    text = content.text

                    response["content"].append(text)

                    # -------------------------------------
                    # Try to parse JSON automatically
                    # -------------------------------------

                    try:

                        parsed = json.loads(text)

                        if isinstance(
                            parsed,
                            dict,
                        ):

                            response[
                                "structured_content"
                            ] = parsed

                    except (json.JSONDecodeError, TypeError):
                        pass

                else:

                    response["content"].append(
                        str(content)
                    )

        return response

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    async def close(self):

        if self._session_context is not None:

            await self._session_context.__aexit__(
                None,
                None,
                None,
            )

            self._session_context = None

        if self._stdio_context is not None:

            await self._stdio_context.__aexit__(
                None,
                None,
                None,
            )

            self._stdio_context = None

        self.session = None

    # -----------------------------------------------------
    # Context manager
    # -----------------------------------------------------

    async def __aenter__(self):

        await self.connect()

        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):

        await self.close()


# ---------------------------------------------------------
# Test MCP client
# ---------------------------------------------------------

async def main():

    async with MCPClient() as client:

        tools = await client.list_tools()

        print("=" * 60)
        print("AVAILABLE MCP TOOLS")
        print("=" * 60)

        for tool in tools:

            print(
                f"\nTool: {tool['name']}"
            )

            print(
                f"Description:\n"
                f"{tool['description']}"
            )

            print(
                f"Input Schema:\n"
                f"{tool['input_schema']}"
            )

        print("\nMCP connection successful.")


if __name__ == "__main__":

    asyncio.run(main())