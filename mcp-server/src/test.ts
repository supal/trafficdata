import { db } from './database.js';

async function runTests() {
  console.log('🧪 Running Traffic Database Tests...\n');

  try {
    // Test 1: Connect to database
    console.log('Test 1: Connecting to database...');
    await db.connect();
    console.log('✓ Connection successful\n');

    // Test 2: Get all traffic data
    console.log('Test 2: Fetching all traffic data (limit: 5)...');
    const allData = await db.getAllTrafficData(5);
    console.log(`✓ Retrieved ${allData.length} records`);
    if (allData.length > 0) {
      console.log('Sample record:', JSON.stringify(allData[0], null, 2));
    }
    console.log();

    // Test 3: Get statistics
    console.log('Test 3: Fetching traffic statistics...');
    const stats = await db.getTrafficStats();
    console.log('✓ Statistics:', JSON.stringify(stats, null, 2));
    console.log();

    // Test 4: Get average speed
    console.log('Test 4: Calculating average speed for all vehicles...');
    const avgSpeed = await db.getAverageSpeedByVehicleType('all_vehicles_avg_speed');
    console.log('✓ Average speed:', JSON.stringify(avgSpeed, null, 2));
    console.log();

    console.log('✅ All tests completed successfully!\n');
  } catch (error) {
    console.error('❌ Test failed:', error);
  } finally {
    await db.close();
  }
}

runTests();
