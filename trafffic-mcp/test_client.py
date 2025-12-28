#!/usr/bin/env python3
"""
Test script to verify the MCP server tools.
This demonstrates how to test the server's capabilities.
"""

import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import base64
import sys


async def test_server():
    """Test the MCP server with all available tools."""
    # Connect to the server via stdio
    server_params = StdioServerParameters(
        command="/Users/arif.ahsan/Documents/GitHub/trafficdata/trafffic-mcp/.venv/bin/python",
        args=["/Users/arif.ahsan/Documents/trafffic-mcp/server.py"]
    )
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
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
            
            # Test average_speed_heavy_vehicles tool
            print("\nTesting average_speed_heavy_vehicles tool...")
            result = await session.call_tool("average_speed_heavy_vehicles", {})
            print(f"  Result:\n{result.content[0].text}")
            
            # Test average_speed_passenger_cars tool
            print("\nTesting average_speed_passenger_cars tool...")
            result = await session.call_tool("average_speed_passenger_cars", {})
            print(f"  Result:\n{result.content[0].text}")
            
            # Test speed_graph tool
            print("\nTesting speed_graph tool...")
            result = await session.call_tool("speed_graph", {})
            if result.content[0].type == "image":
                # Verify it's a valid base64-encoded PNG
                img_data = result.content[0].data
                print(f"  ✓ Graph generated successfully!")
                print(f"  Image type: {result.content[0].mimeType}")
                print(f"  Base64 data length: {len(img_data)} characters")
                
                # Optionally decode and save to file for verification
                try:
                    img_bytes = base64.b64decode(img_data)
                    output_path = "/Users/arif.ahsan/Documents/trafffic-mcp/traffic_speed_graph_test.png"
                    with open(output_path, 'wb') as f:
                        f.write(img_bytes)
                    print(f"  ✓ Graph saved to: {output_path}")
                    print(f"  ✓ File size: {len(img_bytes)} bytes")
                except Exception as e:
                    print(f"  Error saving graph: {e}")
            else:
                print(f"  ✗ Unexpected result type: {result.content[0].type}")
                return False
    
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_server())
        if success is not False:
            print("\n✓ All tests passed!")
            sys.exit(0)
        else:
            print("\n✗ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


