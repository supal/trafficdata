#!/usr/bin/env node

import pg from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const pool = new pg.Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME || 'traffic_data',
});

async function testRecordCount() {
  try {
    const result = await pool.query('SELECT COUNT(*) as count FROM traffic_data');
    const count = result.rows[0].count;
    console.log(`\n✓ Total records in traffic_data table: ${count}\n`);
    
    // Get sample records
    const sampleResult = await pool.query('SELECT * FROM traffic_data LIMIT 3');
    console.log('Sample records:');
    console.log(JSON.stringify(sampleResult.rows, null, 2));
    
    await pool.end();
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

testRecordCount();
