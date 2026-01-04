#!/usr/bin/env node

/**
 * Manual test script to verify MCP server tools
 * Simulates Claude calling the tools
 */

import { db } from './dist/database.js';
import { generateSpeedGraph, analyzePeakHours } from './dist/analytics.js';

async function runManualTests() {
  console.log('🧪 Manual Tool Tests\n');
  console.log('='.repeat(70) + '\n');

  try {
    await db.connect();

    // Test 1: Get all traffic data
    console.log('Test 1: get_all_traffic_data (limit: 10)');
    const allData = await db.getAllTrafficData(10);
    console.log(`✓ Retrieved ${allData.length} records\n`);

    // Test 2: Get statistics
    console.log('Test 2: get_traffic_statistics');
    const stats = await db.getTrafficStats();
    console.log(`✓ Statistics retrieved:`);
    console.log(`  Total Records: ${stats.total_records}`);
    console.log(`  Avg All Vehicles Speed: ${stats.avg_all_vehicles_speed} km/h`);
    console.log(`  Avg Passenger Cars Speed: ${stats.avg_passenger_car_speed} km/h\n`);

    // Test 3: Get speed comparison
    console.log('Test 3: get_speed_comparison');
    const speedComp = await db.getSpeedsComparison();
    console.log(`✓ Speed comparison retrieved:`);
    console.log(`  All Vehicles: ${speedComp.avg_all_vehicles_speed} km/h`);
    console.log(`  Heavy Vehicles: ${speedComp.avg_heavy_vehicles_speed} km/h`);
    console.log(`  Passenger Cars: ${speedComp.avg_passenger_car_speed} km/h\n`);

    // Test 4: Get vehicle count comparison
    console.log('Test 4: get_vehicle_count_comparison');
    const countComp = await db.getVehicleCountsComparison();
    console.log(`✓ Vehicle count comparison retrieved:`);
    console.log(`  All Vehicles: ${countComp.avg_all_vehicles}`);
    console.log(`  Heavy Vehicles: ${countComp.avg_heavy_vehicles}`);
    console.log(`  Passenger Cars: ${countComp.avg_passenger_cars}\n`);

    // Test 5: Get traffic by date range
    console.log('Test 5: get_traffic_by_date_range');
    const byDate = await db.getTrafficByDateRange('2023-11-01', '2023-11-30');
    console.log(`✓ Retrieved ${byDate.length} records for date range\n`);

    // Test 6: Get traffic by county
    console.log('Test 6: get_traffic_by_county');
    const byCounty = await db.getTrafficByCounty('Dalarnas');
    console.log(`✓ Retrieved ${byCounty.length} records for county\n`);

    // Test 7: Get traffic by road
    console.log('Test 7: get_traffic_by_road');
    const byRoad = await db.getTrafficByRoad('800');
    console.log(`✓ Retrieved ${byRoad.length} records for road\n`);

    // Test 8: Generate speed graph
    console.log('Test 8: generate_speed_graph');
    const graph = await generateSpeedGraph(['heavy_vehicles_avg_speed', 'passenger_car_avg_speed']);
    if (graph) {
      console.log(`✓ Speed graph generated (${graph.length} characters)\n`);
      console.log(graph);
    } else {
      console.log('✗ Graph generation failed\n');
    }

    // Test 9: Get peak hours
    console.log('\n\nTest 9: get_peak_hours');
    const peakHours = await analyzePeakHours();
    console.log(peakHours);

    console.log('\n' + '='.repeat(70));
    console.log('✅ All manual tests completed successfully!');
    console.log('='.repeat(70) + '\n');

  } catch (error) {
    console.error('❌ Test failed:', error);
  } finally {
    await db.close();
  }
}

runManualTests();
