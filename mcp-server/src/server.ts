#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
  TextContent,
} from '@modelcontextprotocol/sdk/types.js';
import { db } from './database.js';
import {
  generateSpeedGraph,
  analyzePeakHours,
  transformToLongFormat,
  generateSpeedBarChart,
  generateVehicleCountBarChart,
} from './analytics.js';

// Create the MCP server with capabilities
const server = new Server({
  name: 'traffic-mcp-server',
  version: '1.0.0',
}, {
  capabilities: {
    tools: {},
  },
});

// Vehicle type configurations for analytics
const VEHICLE_TYPES = {
  all_vehicles: { name: 'All Vehicles' },
  passenger_cars: { name: 'Passenger Cars' },
  heavy_vehicles: { name: 'Heavy Vehicles' },
  heavy_vehicles_trailer: { name: 'Heavy Vehicles with Trailer' },
  heavy_vehicles_no_trailer: { name: 'Heavy Vehicles without Trailer' },
  three_axle_tractor_trailer: { name: 'Three-Axle Tractor with Trailer' },
  two_axle_tractor_trailer: { name: 'Two-Axle Tractor with Trailer' },
  three_axle_tractor_no_trailer: { name: 'Three-Axle Tractor without Trailer' },
  two_axle_tractor_no_trailer: { name: 'Two-Axle Tractor without Trailer' },
  passenger_car_trailer: { name: 'Passenger Cars with Trailer' },
  passenger_car_no_trailer: { name: 'Passenger Cars without Trailer' },
};

// Define available tools
const tools: Tool[] = [
  {
    name: 'ping',
    description: 'Test the server with a simple ping',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'get_all_traffic_data',
    description: 'Retrieve all traffic data from the database with optional limit',
    inputSchema: {
      type: 'object',
      properties: {
        limit: {
          type: 'number',
          description: 'Maximum number of records to return (default: 1000)',
          default: 1000,
        },
      },
      required: [],
    },
  },
  {
    name: 'get_traffic_statistics',
    description: 'Get comprehensive traffic statistics including counts and speeds by vehicle type',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'get_speed_comparison',
    description: 'Compare average speeds for all vehicle types',
    inputSchema: {
      type: 'object',
      properties: {
        start_date: {
          type: 'string',
          description: 'Optional start date (YYYY-MM-DD)',
        },
        end_date: {
          type: 'string',
          description: 'Optional end date (YYYY-MM-DD)',
        },
      },
      required: [],
    },
  },
  {
    name: 'get_vehicle_count_comparison',
    description: 'Compare average vehicle counts by type',
    inputSchema: {
      type: 'object',
      properties: {
        start_date: {
          type: 'string',
          description: 'Optional start date (YYYY-MM-DD)',
        },
        end_date: {
          type: 'string',
          description: 'Optional end date (YYYY-MM-DD)',
        },
      },
      required: [],
    },
  },
  {
    name: 'generate_speed_graph',
    description: 'Generate a visualization of speed trends over time for selected vehicle types',
    inputSchema: {
      type: 'object',
      properties: {
        vehicle_types: {
          type: 'array',
          items: { type: 'string' },
          description: 'Vehicle types to include in graph (default: heavy_vehicles, passenger_cars)',
        },
        start_date: {
          type: 'string',
          description: 'Optional start date (YYYY-MM-DD)',
        },
        end_date: {
          type: 'string',
          description: 'Optional end date (YYYY-MM-DD)',
        },
      },
      required: [],
    },
  },
  {
    name: 'get_peak_hours',
    description: 'Analyze traffic patterns to find peak hours and times',
    inputSchema: {
      type: 'object',
      properties: {
        vehicle_type: {
          type: 'string',
          description: 'Specific vehicle type to analyze (optional)',
        },
      },
      required: [],
    },
  },
  {
    name: 'get_traffic_by_location',
    description: 'Get traffic data by county, road number, or measurement point',
    inputSchema: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'County name, road number, or measurement point (punkt_nummer)',
        },
      },
      required: ['location'],
    },
  },
  {
    name: 'get_traffic_by_date_range',
    description: 'Get traffic data within a specific date range',
    inputSchema: {
      type: 'object',
      properties: {
        start_date: {
          type: 'string',
          description: 'Start date (YYYY-MM-DD or ISO 8601 format)',
        },
        end_date: {
          type: 'string',
          description: 'End date (YYYY-MM-DD or ISO 8601 format)',
        },
      },
      required: ['start_date', 'end_date'],
    },
  },
  {
    name: 'get_traffic_by_road',
    description: 'Get traffic data for a specific road number',
    inputSchema: {
      type: 'object',
      properties: {
        road_number: {
          type: 'string',
          description: 'Road number (e.g., "E4", "3", "45")',
        },
      },
      required: ['road_number'],
    },
  },
  {
    name: 'get_traffic_by_county',
    description: 'Get traffic data for a specific county',
    inputSchema: {
      type: 'object',
      properties: {
        county: {
          type: 'string',
          description: 'County name',
        },
      },
      required: ['county'],
    },
  },
  {
    name: 'get_traffic_by_measurement_point',
    description: 'Get traffic data for a specific measurement point',
    inputSchema: {
      type: 'object',
      properties: {
        punkt_nummer: {
          type: 'string',
          description: 'Measurement point number (punkt_nummer)',
        },
      },
      required: ['punkt_nummer'],
    },
  },
  {
    name: 'transform_to_long_format',
    description: 'Transform traffic data from wide format to long format (one row per vehicle type)',
    inputSchema: {
      type: 'object',
      properties: {
        limit: {
          type: 'number',
          description: 'Maximum number of records to process (default: 5000)',
          default: 5000,
        },
      },
      required: [],
    },
  },
  {
    name: 'generate_speed_bar_chart',
    description: 'Generate a bar chart visualization of average speeds by vehicle type',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'generate_vehicle_count_bar_chart',
    description: 'Generate a bar chart visualization of average vehicle counts by type',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
];

// Handler for listing available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

// Handler for calling tools
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result;

    switch (name) {
      case 'ping': {
        return {
          content: [
            {
              type: 'text' as const,
              text: 'pong',
            },
          ],
        };
      }

      case 'get_all_traffic_data': {
        const limit = (args as any).limit || 1000;
        result = await db.getAllTrafficData(limit);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_traffic_by_location': {
        const location = (args as any).location;
        if (!location) {
          throw new Error('location parameter is required');
        }
        result = await db.getTrafficByLocation(location);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_traffic_by_date_range': {
        const { start_date, end_date } = args as any;
        if (!start_date || !end_date) {
          throw new Error('start_date and end_date parameters are required');
        }
        result = await db.getTrafficByDateRange(start_date, end_date);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_traffic_statistics': {
        result = await db.getTrafficStats();
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_traffic_by_road': {
        const { road_number } = args as any;
        if (!road_number) {
          throw new Error('road_number parameter is required');
        }
        result = await db.getTrafficByRoad(road_number);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_traffic_by_county': {
        const { county } = args as any;
        if (!county) {
          throw new Error('county parameter is required');
        }
        result = await db.getTrafficByCounty(county);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_traffic_by_measurement_point': {
        const { punkt_nummer } = args as any;
        if (!punkt_nummer) {
          throw new Error('punkt_nummer parameter is required');
        }
        result = await db.getTrafficByMeasurementPoint(punkt_nummer);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_vehicle_count_comparison': {
        const { start_date, end_date } = args as any;
        result = await db.getVehicleCountsComparison(start_date, end_date);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_speed_comparison': {
        const { start_date, end_date } = args as any;
        result = await db.getSpeedsComparison(start_date, end_date);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'generate_speed_graph': {
        const { vehicle_types, start_date, end_date } = args as any;
        const graphData = await generateSpeedGraph(vehicle_types, start_date, end_date);
        if (!graphData) {
          throw new Error('Could not generate graph');
        }
        return {
          content: [
            {
              type: 'text' as const,
              text: graphData,
            },
          ],
        };
      }

      case 'get_peak_hours': {
        const { vehicle_type } = args as any;
        const analysis = await analyzePeakHours(vehicle_type);
        return {
          content: [
            {
              type: 'text' as const,
              text: analysis,
            },
          ],
        };
      }

      case 'transform_to_long_format': {
        const { limit } = args as any;
        const longFormatData = await transformToLongFormat(limit);
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(longFormatData, null, 2),
            },
          ],
        };
      }

      case 'generate_speed_bar_chart': {
        const chart = await generateSpeedBarChart();
        return {
          content: [
            {
              type: 'text' as const,
              text: chart,
            },
          ],
        };
      }

      case 'generate_vehicle_count_bar_chart': {
        const chart = await generateVehicleCountBarChart();
        return {
          content: [
            {
              type: 'text' as const,
              text: chart,
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: 'text' as const,
          text: `Error: ${errorMessage}`,
          isError: true,
        },
      ],
    };
  }
});

async function main() {
  console.log('🚀 Starting Traffic MCP Server...');
  
  try {
    // Connect to database
    await db.connect();

    // Start the server
    const transport = new StdioServerTransport();
    await server.connect(transport);
    
    console.log('✓ MCP Server is running and connected to database');
  } catch (error) {
    console.error('✗ Failed to start server:', error);
    process.exit(1);
  }
}

main();
