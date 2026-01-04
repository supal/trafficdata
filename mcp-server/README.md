# Traffic MCP Server

A Model Context Protocol (MCP) server built with Node.js/TypeScript that connects to a PostgreSQL database for traffic data analysis.

## Features

- 📊 **Traffic Data Queries** - Retrieve traffic data with multiple filtering options
- 🗄️ **PostgreSQL Integration** - Direct database connection
- 🔧 **Type-Safe** - Built with TypeScript
- 🚀 **Fast & Efficient** - Node.js with connection pooling
- 📈 **Statistics** - Get comprehensive traffic metrics and analytics

## Prerequisites

- Node.js 18+ and npm
- PostgreSQL 12+
- Traffic data database with `traffic_data` table

## Installation

### 1. Install Dependencies
```bash
cd mcp-server
npm install
```

### 2. Configure Environment Variables
The `.env` file is already created. Edit it with your database credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=traffic_data
```

### 3. Build the Project
```bash
npm run build
```

## Usage

### Start the Server
```bash
npm start
```

### Development Mode (with auto-reload)
```bash
npm run dev
```

### Run Tests
```bash
npm test
```

### Watch Mode (auto-compile TypeScript)
```bash
npm run watch
```

## Available Tools

### 1. `get_all_traffic_data`
Retrieve all traffic records from the database.

**Parameters:**
- `limit` (number, optional): Maximum records to return (default: 1000)

**Example:**
```json
{
  "limit": 100
}
```

---

### 2. `get_traffic_by_location`
Search traffic data by county, road number, or measurement point.

**Parameters:**
- `location` (string, required): County name, road number, or punkt_nummer

**Example:**
```json
{
  "location": "Stockholm"
}
```

---

### 3. `get_traffic_by_date_range`
Retrieve traffic data within a specific date range.

**Parameters:**
- `start_date` (string, required): Start date (YYYY-MM-DD or ISO 8601)
- `end_date` (string, required): End date (YYYY-MM-DD or ISO 8601)

**Example:**
```json
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-04"
}
```

---

### 4. `get_traffic_statistics`
Get comprehensive traffic statistics including:
- Total records count
- Average speeds by vehicle type
- Max/Min speeds
- Unique counties, roads, and measurement points

**Parameters:** None

---

### 5. `get_traffic_by_road`
Get traffic data for a specific road number.

**Parameters:**
- `road_number` (string, required): Road number (e.g., "E4", "3", "45")

**Example:**
```json
{
  "road_number": "E4"
}
```

---

### 6. `get_traffic_by_county`
Get traffic data for a specific county.

**Parameters:**
- `county` (string, required): County name

**Example:**
```json
{
  "county": "Västra Götaland"
}
```

---

### 7. `get_traffic_by_measurement_point`
Get traffic data for a specific measurement point.

**Parameters:**
- `punkt_nummer` (string, required): Measurement point number

**Example:**
```json
{
  "punkt_nummer": "12345"
}
```

---

### 8. `get_vehicle_counts_comparison`
Get average vehicle counts by type (all vehicles, passenger cars, heavy vehicles, with/without trailers).

**Parameters:**
- `start_date` (string, optional): Filter from this date
- `end_date` (string, optional): Filter to this date

**Example:**
```json
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-04"
}
```

**Returns:**
- avg_all_vehicles
- avg_passenger_cars
- avg_heavy_vehicles
- avg_heavy_with_trailer
- avg_heavy_without_trailer
- avg_passenger_with_trailer
- avg_passenger_without_trailer

---

### 9. `get_speeds_comparison`
Get average speeds by vehicle type across all measurement points.

**Parameters:**
- `start_date` (string, optional): Filter from this date
- `end_date` (string, optional): Filter to this date

**Example:**
```json
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-04"
}
```

**Returns:**
- avg_all_vehicles_speed
- avg_passenger_cars_speed
- avg_heavy_vehicles_speed
- avg_heavy_with_trailer_speed
- avg_heavy_without_trailer_speed
- avg_passenger_with_trailer_speed
- avg_passenger_without_trailer_speed
- avg_three_axle_trailer_speed
- avg_two_axle_trailer_speed

---

## Project Structure

```
mcp-server/
├── src/
│   ├── server.ts       # MCP server implementation
│   ├── database.ts     # PostgreSQL database client
│   └── test.ts         # Database tests
├── dist/               # Compiled JavaScript (generated)
├── package.json        # Project dependencies
├── tsconfig.json       # TypeScript configuration
├── .env                # Environment variables (update with credentials)
└── README.md           # This file
```

## Database Schema

The server connects to an existing PostgreSQL table named `traffic_data` with the following structure:

```sql
CREATE TABLE public.traffic_data (
  id SERIAL PRIMARY KEY,
  measurement_time TIMESTAMP NOT NULL,
  county VARCHAR(100),
  road_number VARCHAR(10),
  punkt_nummer VARCHAR(20),
  
  all_vehicles_count INTEGER,
  all_vehicles_avg_speed DECIMAL(5, 2),
  
  passenger_car_count INTEGER,
  passenger_car_avg_speed DECIMAL(5, 2),
  
  heavy_vehicles_count INTEGER,
  heavy_vehicles_avg_speed DECIMAL(5, 2),
  
  heavy_vehicles_trailer_count INTEGER,
  heavy_vehicles_trailer_avg_speed DECIMAL(5, 2),
  
  heavy_vehicles_no_trailer_count INTEGER,
  heavy_vehicles_no_trailer_avg_speed DECIMAL(5, 2),
  
  three_axle_tractor_trailer_count INTEGER,
  three_axle_tractor_trailer_avg_speed DECIMAL(5, 2),
  
  two_axle_tractor_trailer_count INTEGER,
  two_axle_tractor_trailer_avg_speed DECIMAL(5, 2),
  
  three_axle_tractor_no_trailer_count INTEGER,
  three_axle_tractor_no_trailer_avg_speed DECIMAL(5, 2),
  
  two_axle_tractor_no_trailer_count INTEGER,
  two_axle_tractor_no_trailer_avg_speed DECIMAL(5, 2),
  
  passenger_car_trailer_count INTEGER,
  passenger_car_trailer_avg_speed DECIMAL(5, 2),
  
  passenger_car_no_trailer_count INTEGER,
  passenger_car_no_trailer_avg_speed DECIMAL(5, 2),
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting

### Connection Error
- Verify PostgreSQL is running
- Check `.env` credentials
- Ensure database name exists

### Build Error
```bash
npm run build
```

### Test Database Connection
```bash
npm test
```

## Development

### Type Checking
TypeScript is configured in strict mode. All code is type-safe.

### Adding New Tools
1. Add tool definition in `src/server.ts`
2. Add corresponding database method in `src/database.ts`
3. Implement the tool handler in the `CallToolRequestSchema` handler

### Example: Adding a New Tool
```typescript
// In database.ts
async getNewData(param: string): Promise<any[]> {
  const result = await this.pool.query(
    'SELECT * FROM traffic_data WHERE column = $1',
    [param]
  );
  return result.rows;
}

// In server.ts
{
  name: 'new_tool',
  description: 'Description of the tool',
  inputSchema: {
    type: 'object',
    properties: {
      param: { type: 'string' }
    },
    required: ['param']
  }
}

// In the tool handler
case 'new_tool': {
  result = await db.getNewData((args as any).param);
  // return result
}
```

## Performance Notes

- Connection pooling is enabled for better performance
- Queries support LIMIT to prevent large data transfers
- Use date ranges to filter large datasets efficiently

## License

MIT
