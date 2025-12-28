#!/usr/bin/env python3
"""
A MCP server with tools for traffic data analysis.
Tools: ping, sum, read_file, average_speed_heavy_vehicles, average_speed_passenger_cars, speed_graph
"""

import asyncio
from pathlib import Path
from mcp.server import Server
import mcp.types as types
from openpyxl import load_workbook
import statistics
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import base64
from io import BytesIO


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
        
        # Time is in column 1
        # Heavy vehicle speed is in column 5 (0-indexed: 4)
        # Passenger car speed is in column 7 (0-indexed: 6)
        time_col = 1
        heavy_vehicle_speed_col = 5
        passenger_car_speed_col = 7
        
        # Extract data from row 3 onwards
        timestamps = []
        heavy_speeds = []
        passenger_speeds = []
        
        for row_idx in range(3, ws.max_row + 1):
            # Get timestamp
            time_cell = ws.cell(row=row_idx, column=time_col).value
            timestamp = None
            if time_cell:
                try:
                    if isinstance(time_cell, datetime):
                        timestamp = time_cell
                    else:
                        timestamp = datetime.fromisoformat(str(time_cell))
                except:
                    pass
            
            # Heavy vehicle speed
            heavy_cell = ws.cell(row=row_idx, column=heavy_vehicle_speed_col).value
            heavy_speed = None
            if heavy_cell and str(heavy_cell).strip() and str(heavy_cell) != "0,0":
                try:
                    heavy_speed = float(str(heavy_cell).replace(",", "."))
                    if heavy_speed <= 0:
                        heavy_speed = None
                except:
                    pass
            
            # Passenger car speed
            passenger_cell = ws.cell(row=row_idx, column=passenger_car_speed_col).value
            passenger_speed = None
            if passenger_cell and str(passenger_cell).strip() and str(passenger_cell) != "0,0":
                try:
                    passenger_speed = float(str(passenger_cell).replace(",", "."))
                    if passenger_speed <= 0:
                        passenger_speed = None
                except:
                    pass
            
            # Only add row if we have timestamp and at least one speed value
            if timestamp and (heavy_speed is not None or passenger_speed is not None):
                timestamps.append(timestamp)
                heavy_speeds.append(heavy_speed if heavy_speed is not None else 0)
                passenger_speeds.append(passenger_speed if passenger_speed is not None else 0)
        
        return {
            "timestamps": timestamps,
            "heavy_speeds": heavy_speeds,
            "passenger_speeds": passenger_speeds
        }
    except Exception as e:
        return {"error": str(e)}


def generate_speed_graph():
    """Generate a graph showing average speed over time for heavy vehicles and passenger cars."""
    try:
        data = load_traffic_data()
        if not data or "error" in data:
            return None
        
        timestamps = data.get("timestamps", [])
        heavy_speeds = data.get("heavy_speeds", [])
        passenger_speeds = data.get("passenger_speeds", [])
        
        if not timestamps or not (heavy_speeds or passenger_speeds):
            return None
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot both datasets
        ax.plot(timestamps, heavy_speeds, label='Heavy Vehicles', color='red', linewidth=2, marker='o', markersize=3)
        ax.plot(timestamps, passenger_speeds, label='Passenger Cars', color='blue', linewidth=2, marker='s', markersize=3)
        
        # Format the plot
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Average Speed (km/h)', fontsize=12)
        ax.set_title('Average Speed Over Time: Heavy Vehicles vs Passenger Cars', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis to show dates nicely
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        fig.autofmt_xdate(rotation=45, ha='right')
        
        # Tight layout to prevent label cutoff
        fig.tight_layout()
        
        # Save to bytes buffer
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        
        # Encode to base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return img_base64
    except Exception as e:
        return None


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
        types.Tool(
            name="speed_graph",
            description="Generates and returns a graph showing average speed over time for heavy vehicles and passenger cars",
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
    
    elif name == "speed_graph":
        img_base64 = generate_speed_graph()
        if not img_base64:
            return [types.TextContent(type="text", text="Error generating graph")]
        
        return [types.ImageContent(type="image", data=img_base64, mimeType="image/png")]
    
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
