#!/usr/bin/env python3
"""
A simple MCP server with three tools: ping, sum, and read_file.
"""

import asyncio
import sys
from pathlib import Path
from mcp.server import Server
import mcp.types as types


# Create the MCP server
server = Server("simple-mcp-server")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available tools."""
    return [
        types.Tool(
            name="ping",
            description="Returns 'pong' as a simple test",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="sum",
            description="Adds two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number",
                    },
                },
                "required": ["a", "b"],
            },
        ),
        types.Tool(
            name="read_file",
            description="Reads and returns the contents of a text file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read",
                    },
                },
                "required": ["path"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Execute a tool by name with the given arguments."""
    if name == "ping":
        return [types.TextContent(type="text", text="pong")]
    
    elif name == "sum":
        a = arguments.get("a")
        b = arguments.get("b")
        if a is None or b is None:
            return [types.TextContent(type="text", text="Error: Missing 'a' or 'b' argument")]
        result = a + b
        return [types.TextContent(type="text", text=f"{result}")]
    
    elif name == "read_file":
        path = arguments.get("path")
        if not path:
            return [types.TextContent(type="text", text="Error: Missing 'path' argument")]
        try:
            file_path = Path(path)
            if not file_path.exists():
                return [types.TextContent(type="text", text=f"Error: File not found: {path}")]
            contents = file_path.read_text()
            return [types.TextContent(type="text", text=contents)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error reading file: {str(e)}")]
    
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server over stdio."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
