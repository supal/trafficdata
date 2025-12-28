#!/usr/bin/env python3
"""
A MCP server with tools for traffic data analysis.
Tools: ping, sum, read_file, average_speed_heavy_vehicles, average_speed_passenger_cars
"""

import asyncio
from pathlib import Path
from mcp.server import Server
import mcp.types as types
from openpyxl import load_workbook
import statistics


# Create the MCP server
server = Server("traffic-mcp-server")


def load_traffic_data():
    """Load traffic data from Excel file."""
    excel_file = Path(__file__).parent / "data" / "trafikverket_data_9dccacb0.xlsx"
    if not excel_file.exists():
        return None
    
    try:
        wb = load_workbook(excel_file)
        ws = wb.active
        
        # Get headers from row 2
        headers = [cell.value for cell in ws[2]]
        
        # Heavy vehicle speed is in column 5 (0-indexed: 4)
        # Passenger car speed is in column 7 (0-indexed: 6)
        heavy_vehicle_speed_col = 5
        passenger_car_speed_col = 7
        
        # Extract data from row 3 onwards
        heavy_speeds = []
        passenger_speeds = []
        
        for row_idx in range(3, ws.max_row + 1):
            # Heavy vehicle speed
            cell_value = ws.cell(row=row_idx, column=heavy_vehicle_speed_col).value
            if cell_value and str(cell_value).strip() and str(cell_value) != "0,0":
                try:
                    speed = float(str(cell_value).replace(",", "."))
                    if speed > 0:
                        heavy_speeds.append(speed)
                except:
                    pass
            
            # Passenger car speed
            cell_value = ws.cell(row=row_idx, column=passenger_car_speed_col).value
            if cell_value and str(cell_value).strip() and str(cell_value) != "0,0":
                try:
                    speed = float(str(cell_value).replace(",", "."))
                    if speed > 0:
                        passenger_speeds.append(speed)
                except:
                    pass
        
        return {
            "heavy_speeds": heavy_speeds,
            "passenger_speeds": passenger_speeds
        }
    except Exception as e:
        return {"error": str(e)}


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
        types.Tool(
            name="average_speed_heavy_vehicles",
            description="Returns the average speed of heavy vehicles from traffic data",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="average_speed_passenger_cars",
            description="Returns the average speed of passenger cars from traffic data",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
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
    
    elif name == "average_speed_heavy_vehicles":
        data = load_traffic_data()
        if not data or "error" in data:
            return [types.TextContent(type="text", text=f"Error loading traffic data: {data.get('error', 'Unknown error')}")]
        
        speeds = data.get("heavy_speeds", [])
        if not speeds:
            return [types.TextContent(type="text", text="No heavy vehicle speed data available")]
        
        avg_speed = statistics.mean(speeds)
        min_speed = min(speeds)
        max_speed = max(speeds)
        count = len(speeds)
        
        result = f"Heavy Vehicles Statistics:\n"
        result += f"  Average Speed: {avg_speed:.2f} km/h\n"
        result += f"  Min Speed: {min_speed:.2f} km/h\n"
        result += f"  Max Speed: {max_speed:.2f} km/h\n"
        result += f"  Data Points: {count}"
        
        return [types.TextContent(type="text", text=result)]
    
    elif name == "average_speed_passenger_cars":
        data = load_traffic_data()
        if not data or "error" in data:
            return [types.TextContent(type="text", text=f"Error loading traffic data: {data.get('error', 'Unknown error')}")]
        
        speeds = data.get("passenger_speeds", [])
        if not speeds:
            return [types.TextContent(type="text", text="No passenger car speed data available")]
        
        avg_speed = statistics.mean(speeds)
        min_speed = min(speeds)
        max_speed = max(speeds)
        count = len(speeds)
        
        result = f"Passenger Cars Statistics:\n"
        result += f"  Average Speed: {avg_speed:.2f} km/h\n"
        result += f"  Min Speed: {min_speed:.2f} km/h\n"
        result += f"  Max Speed: {max_speed:.2f} km/h\n"
        result += f"  Data Points: {count}"
        
        return [types.TextContent(type="text", text=result)]
    
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
