#!/usr/bin/env python3
"""
Test script to verify the MCP server tools.
This demonstrates how to test the server's capabilities.
"""

import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


async def test_server():
    """Test the MCP server with all three tools."""
    # Connect to the server via stdio
    async with stdio_client(
        ["bash", "-c", "source /Users/arif.ahsan/Documents/trafffic-mcp/venv/bin/activate && python /Users/arif.ahsan/Documents/trafffic-mcp/server.py"]
    ) as client:
        async with ClientSession(client) as session:
            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test ping tool
            print("\nTesting ping tool...")
            result = await session.call_tool("ping", {})
            print(f"  Result: {result.content[0].text}")
            
            # Test sum tool
            print("\nTesting sum tool (5 + 3)...")
            result = await session.call_tool("sum", {"a": 5, "b": 3})
            print(f"  Result: {result.content[0].text}")
            
            # Test read_file tool
            print("\nTesting read_file tool...")
            result = await session.call_tool("read_file", {"path": "/Users/arif.ahsan/Documents/trafffic-mcp/README.md"})
            lines = result.content[0].text.split('\n')
            print(f"  First 5 lines of README.md:")
            for line in lines[:5]:
                print(f"    {line}")


if __name__ == "__main__":
    asyncio.run(test_server())
