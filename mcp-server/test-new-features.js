#!/usr/bin/env node

import { transformToLongFormat, generateSpeedBarChart, generateVehicleCountBarChart } from './dist/analytics.js';

async function testNewFeatures() {
  console.log('\n=== Testing Long Format Transformation ===\n');
  
  try {
    // Test long format transformation (first 5 records)
    const longFormat = await transformToLongFormat(100);
    console.log(`✓ Transformed ${longFormat.length} records to long format\n`);
    console.log('Sample long format records:');
    console.log(JSON.stringify(longFormat.slice(0, 5), null, 2));
    
    console.log('\n=== Testing Speed Bar Chart ===\n');
    const speedChart = await generateSpeedBarChart();
    console.log(speedChart);
    
    console.log('\n=== Testing Vehicle Count Bar Chart ===\n');
    const countChart = await generateVehicleCountBarChart();
    console.log(countChart);
    
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

testNewFeatures();
