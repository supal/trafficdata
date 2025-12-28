# Traffic MCP Server

A Python-based MCP (Model Context Protocol) server with tools for traffic data analysis.

## Features

### Core Tools
- **ping**: Returns "pong" for testing connectivity
- **sum**: Adds two numbers together
- **read_file**: Reads and returns the contents of a text file

### Traffic Analysis Tools
- **average_speed_heavy_vehicles**: Calculates and returns average speed statistics for heavy vehicles
- **average_speed_passenger_cars**: Calculates and returns average speed statistics for passenger cars

## Installation

### Prerequisites
- Python 3.10+ (we used Python 3.13 in this example)

### Setup

1. Navigate to the project directory:
```bash
cd /Users/arif.ahsan/Documents/trafffic-mcp
```

2. Create a virtual environment:
```bash
python3.13 -m venv venv
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Once the virtual environment is activated, start the server with:

```bash
python server.py
```

The server will start and wait for incoming MCP client requests on stdin/stdout.

## Testing the Server

You can test the server using the provided test client. In a separate terminal (with the venv activated):

```bash
python test_client.py
```

This will test all three tools:
- **ping**: Returns "pong"
- **sum**: Adds 5 + 3 = 8
- **read_file**: Reads the README.md file

## Usage with MCP Clients

The server communicates via the MCP protocol over stdio. To use it with an MCP client, configure the client to spawn the server process:

```bash
/path/to/venv/bin/python /path/to/server.py
```

### Tool Schemas

#### Ping Tool
No input required.
```json
{
  "name": "ping"
}
```
Returns: `"pong"`

#### Sum Tool
Add two numbers together.
```json
{
  "name": "sum",
  "arguments": {
    "a": 5,
    "b": 3
  }
}
```
Returns: `"8"`

#### Read File Tool
Read a text file by path.
```json
{
  "name": "read_file",
  "arguments": {
    "path": "/path/to/file.txt"
  }
}
```
Returns: File contents as text

#### Average Speed Heavy Vehicles
Get average speed statistics for heavy vehicles from traffic data.
```json
{
  "name": "average_speed_heavy_vehicles"
}
```
Returns: 
```
Heavy Vehicles Statistics:
  Average Speed: 58.73 km/h
  Min Speed: 33.50 km/h
  Max Speed: 82.10 km/h
  Data Points: 89
```

#### Average Speed Passenger Cars
Get average speed statistics for passenger cars from traffic data.
```json
{
  "name": "average_speed_passenger_cars"
}
```
Returns:
```
Passenger Cars Statistics:
  Average Speed: 60.78 km/h
  Min Speed: 21.20 km/h
  Max Speed: 118.80 km/h
  Data Points: 323
```

## Project Structure

```
.
├── server.py          # Main MCP server implementation
├── test_client.py     # Test client for verifying the server
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Requirements

- Python 3.10 or higher
- mcp SDK (latest version)
- pandas (for data processing)
- openpyxl (for Excel file handling)

## Implementation Details

- **Async/Await**: The server uses Python's asyncio for handling concurrent requests
- **Stdio Transport**: Communication happens over standard input/output, making it compatible with MCP clients that spawn server processes
- **Type Hints**: Full type annotations for better IDE support and type checking
- **Error Handling**: Proper error messages for invalid inputs and missing files
