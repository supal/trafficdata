# MCP Server Tools Reference

## Complete Tool List

### Core Utility Tools

#### ping
- **Description**: Returns "pong" as a simple test
- **Input**: None
- **Output**: Text "pong"
- **Purpose**: Test connectivity

#### sum
- **Description**: Adds two numbers together
- **Input**: 
  - `a` (number): First number
  - `b` (number): Second number
- **Output**: Text with sum result
- **Purpose**: Basic calculation test

#### read_file
- **Description**: Reads and returns the contents of a text file
- **Input**: 
  - `path` (string): Path to the file
- **Output**: Text content of file
- **Purpose**: File reading utility

---

## Vehicle Type Analysis Tools (11 Tools)

All vehicle type tools return statistics including:
- Average Speed (km/h)
- Minimum Speed (km/h)
- Maximum Speed (km/h)
- Median Speed (km/h)
- Number of Data Points

### 1. average_speed_all_vehicles
- **Name**: All Vehicles
- **Data Points**: 323
- **Average Speed**: 60.55 km/h
- **Typical Use**: Overall traffic analysis

### 2. average_speed_heavy_vehicles
- **Name**: Heavy Vehicles (all types combined)
- **Data Points**: 89
- **Average Speed**: 58.73 km/h
- **Typical Use**: Heavy vehicle behavior analysis

### 3. average_speed_passenger_cars
- **Name**: Passenger Cars (all types combined)
- **Data Points**: 323
- **Average Speed**: 60.78 km/h
- **Typical Use**: Passenger vehicle behavior analysis

### 4. average_speed_heavy_with_trailer
- **Name**: Heavy Vehicles with Trailer
- **Data Points**: 10
- **Average Speed**: 62.71 km/h
- **Typical Use**: Impact of trailers on heavy vehicles

### 5. average_speed_heavy_without_trailer
- **Name**: Heavy Vehicles without Trailer
- **Data Points**: 86
- **Average Speed**: 58.47 km/h
- **Typical Use**: Unencumbered heavy vehicle analysis

### 6. average_speed_passenger_with_trailer
- **Name**: Passenger Cars with Trailer
- **Data Points**: 43
- **Average Speed**: 46.64 km/h
- **Typical Use**: Impact of trailers on passenger cars (significant slowdown)

### 7. average_speed_passenger_without_trailer
- **Name**: Passenger Cars without Trailer
- **Data Points**: 323
- **Average Speed**: 61.04 km/h
- **Typical Use**: Standard passenger car performance

### 8. average_speed_two_axle_with_trailer
- **Name**: Two-Axle Tractor with Trailer
- **Data Points**: 8
- **Average Speed**: 64.22 km/h
- **Typical Use**: Lighter tractor configuration analysis

### 9. average_speed_three_axle_with_trailer
- **Name**: Three-Axle Tractor with Trailer
- **Data Points**: 4
- **Average Speed**: 53.33 km/h
- **Typical Use**: Heavier tractor configuration analysis (limited data)

### 10. average_speed_two_axle_without_trailer
- **Name**: Two-Axle Tractor without Trailer
- **Data Points**: 78
- **Average Speed**: 59.11 km/h
- **Typical Use**: Unencumbered lighter tractor analysis

### 11. average_speed_three_axle_without_trailer
- **Name**: Three-Axle Tractor without Trailer
- **Data Points**: 11
- **Average Speed**: 53.76 km/h
- **Typical Use**: Unencumbered heavier tractor analysis

---

## Aggregate Analysis Tools

### all_vehicle_statistics
- **Description**: Returns average speed statistics for all vehicle types simultaneously
- **Input**: None
- **Output**: Formatted text containing statistics for all 11 vehicle types
- **Purpose**: Get comprehensive overview in one call
- **Return Example**:
```
Average Speed Statistics for All Vehicle Types:
======================================================================

All Vehicles:
  Average Speed: 60.55 km/h
  Min Speed: 21.20 km/h
  Max Speed: 87.60 km/h
  Median Speed: 60.80 km/h
  Data Points: 323

[... continues for all 11 types ...]
```

---

## Graph Tools

### speed_graph
- **Description**: Generates a PNG graph showing average speed over time for selected vehicle types
- **Input** (optional):
  - `vehicle_types` (array of strings): List of vehicle type keys to include
    - If omitted, defaults to ["heavy_vehicles", "passenger_cars"]
- **Output**: Base64-encoded PNG image
- **MIME Type**: image/png
- **Graph Features**:
  - Time-based x-axis with proper date formatting
  - Speed-based y-axis (km/h)
  - Color-coded lines for each vehicle type
  - Legend showing vehicle types
  - Grid for easy reading
  - High-resolution output (100 DPI)

#### Example Vehicle Type Combinations:
1. **Heavy vs Passenger**: `["heavy_vehicles", "passenger_cars"]`
2. **Trailer Impact**: `["heavy_with_trailer", "heavy_without_trailer"]`
3. **All Tractors**: `["two_axle_with_trailer", "three_axle_with_trailer", "two_axle_without_trailer", "three_axle_without_trailer"]`
4. **Complete Comparison**: All 11 vehicle types

#### Color Scheme:
- Heavy Vehicles: Red
- Passenger Cars: Blue
- Heavy with Trailer: Dark Red
- Heavy without Trailer: Light Coral
- Passenger with Trailer: Dark Blue
- Passenger without Trailer: Light Blue
- Two-Axle with Trailer: Orange
- Three-Axle with Trailer: Dark Orange
- Two-Axle without Trailer: Yellow
- Three-Axle without Trailer: Gold

---

## Tool Summary

| Category | Count | Purpose |
|---|---|---|
| Core Utility | 3 | Basic operations (ping, sum, file read) |
| Vehicle Type Analysis | 11 | Individual vehicle type statistics |
| Aggregate Analysis | 1 | All-in-one statistics view |
| Graph Tools | 1 | Visual comparison and analysis |
| **TOTAL** | **16** | Complete traffic analysis suite |

---

## Common Usage Patterns

### Pattern 1: Compare Two Vehicle Types
```
Call: average_speed_heavy_vehicles
Call: average_speed_passenger_cars
Compare results manually or use speed_graph tool
```

### Pattern 2: Trailer Impact Analysis
```
Call: speed_graph with ["heavy_with_trailer", "heavy_without_trailer"]
Observe how trailers affect speed over time
```

### Pattern 3: Complete Overview
```
Call: all_vehicle_statistics
Get all 11 vehicle types in one response
Identify patterns and anomalies
```

### Pattern 4: Tractor Configuration Comparison
```
Call: speed_graph with 4 tractor types
Compare 2-axle vs 3-axle
Compare with vs without trailer
```

---

## Response Format Examples

### Statistics Response
```
Heavy Vehicles:
  Average Speed: 58.73 km/h
  Min Speed: 33.50 km/h
  Max Speed: 82.10 km/h
  Median Speed: 58.40 km/h
  Data Points: 89
```

### Graph Response
- Base64-encoded PNG image
- Can be embedded in documents
- Can be saved to file for viewing
- Compatible with all image viewers
- High quality (100 DPI)

---

