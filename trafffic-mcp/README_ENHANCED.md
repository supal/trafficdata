# Enhanced Traffic MCP Server

A comprehensive Python-based MCP (Model Context Protocol) server with tools for analyzing traffic data across all vehicle type combinations.

## Features

### Core Tools
- **ping**: Returns "pong" for testing connectivity
- **sum**: Adds two numbers together
- **read_file**: Reads and returns the contents of a text file

### Vehicle Type Analysis Tools

The server now supports average speed analysis for all vehicle type combinations:

#### Basic Vehicle Types
- **average_speed_all_vehicles**: All vehicles combined
- **average_speed_heavy_vehicles**: Heavy vehicles (all types)
- **average_speed_passenger_cars**: Passenger cars (all types)

#### Heavy Vehicle Combinations
- **average_speed_heavy_with_trailer**: Heavy vehicles with trailer
- **average_speed_heavy_without_trailer**: Heavy vehicles without trailer

#### Passenger Car Combinations
- **average_speed_passenger_with_trailer**: Passenger cars with trailer
- **average_speed_passenger_without_trailer**: Passenger cars without trailer

#### Tractor Types
- **average_speed_two_axle_with_trailer**: Two-axle tractors with trailer
- **average_speed_three_axle_with_trailer**: Three-axle tractors with trailer
- **average_speed_two_axle_without_trailer**: Two-axle tractors without trailer
- **average_speed_three_axle_without_trailer**: Three-axle tractors without trailer

### Analysis Tools
- **all_vehicle_statistics**: Returns comprehensive statistics for all vehicle types simultaneously
- **speed_graph**: Generates visual graphs comparing speed over time for selected vehicle types

## Installation

### Prerequisites
- Python 3.10+ (tested with Python 3.13)

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

```bash
python server.py
```

## Available Data Points by Vehicle Type

| Vehicle Type | Data Points | Avg Speed | Min/Max Speed |
|---|---|---|---|
| All Vehicles | 323 | 60.55 km/h | 21.20/87.60 |
| Heavy Vehicles | 89 | 58.73 km/h | 33.50/82.10 |
| Passenger Cars | 323 | 60.78 km/h | 21.20/118.80 |
| Heavy w/ Trailer | 10 | 62.71 km/h | 43.20/70.00 |
| Heavy w/o Trailer | 86 | 58.47 km/h | 24.80/87.80 |
| 2-Axle Tractor w/ Trailer | 8 | 64.22 km/h | 43.20/70.00 |
| 3-Axle Tractor w/ Trailer | 4 | 53.33 km/h | 43.20/70.00 |
| 2-Axle Tractor w/o Trailer | 78 | 59.11 km/h | 24.80/87.80 |
| 3-Axle Tractor w/o Trailer | 11 | 53.76 km/h | 33.50/69.80 |
| Passenger w/ Trailer | 43 | 46.64 km/h | 26.30/66.20 |
| Passenger w/o Trailer | 323 | 61.04 km/h | 21.20/118.80 |

## Usage Examples

### Get Statistics for a Specific Vehicle Type
```json
{
  "name": "average_speed_heavy_with_trailer"
}
```

Returns:
```
Heavy Vehicles with Trailer:
  Average Speed: 62.71 km/h
  Min Speed: 43.20 km/h
  Max Speed: 70.00 km/h
  Median Speed: 70.00 km/h
  Data Points: 10
```

### Get All Vehicle Type Statistics
```json
{
  "name": "all_vehicle_statistics"
}
```

Returns comprehensive statistics for all 11 vehicle type combinations.

### Generate Comparison Graph
```json
{
  "name": "speed_graph",
  "arguments": {
    "vehicle_types": ["heavy_with_trailer", "passenger_with_trailer"]
  }
}
```

Returns: A PNG graph comparing heavy vehicles with trailers vs passenger cars with trailers over time.

## Graph Generation Capabilities

The `speed_graph` tool can generate graphs for any combination of vehicle types:

- **Heavy vs Passenger Comparison**: See how heavy vehicles differ from passenger cars
- **Trailer Impact**: Compare vehicles with and without trailers
- **Tractor Comparison**: Compare different tractor axle configurations
- **Custom Combinations**: Mix any vehicle types for custom analysis

## Project Structure

```
.
├── server.py              # Main MCP server with all vehicle types
├── test_direct.py         # Direct function tests
├── test_all_vehicles.py   # Comprehensive all-vehicle-type tests
├── test_client.py         # MCP protocol client tests
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── data/
    └── trafikverket_data_9dccacb0.xlsx  # Traffic data file
```

## Requirements

- Python 3.10 or higher
- mcp (Model Context Protocol SDK)
- pandas (data processing)
- openpyxl (Excel file handling)
- matplotlib (graph generation)
- statistics (standard library)

## Key Statistics Provided

For each vehicle type, the server calculates:
- **Average Speed**: Mean speed across all measurements
- **Minimum Speed**: Lowest recorded speed
- **Maximum Speed**: Highest recorded speed
- **Median Speed**: Middle value of speed distribution
- **Data Points**: Number of valid measurements

## Implementation Details

- **Async/Await**: Full async support for concurrent requests
- **Stdio Transport**: Communication via standard input/output
- **Type Hints**: Complete type annotations for IDE support
- **Error Handling**: Graceful error messages for invalid inputs
- **Modular Design**: Easy to extend with additional vehicle types
- **Graph Customization**: Flexible graph generation with color-coded vehicle types

## Testing

Run the comprehensive test suite:

```bash
python test_all_vehicles.py
```

This tests:
- Data loading for all 11 vehicle type combinations
- Statistical calculations
- Specific vehicle groupings
- Graph generation for various combinations

