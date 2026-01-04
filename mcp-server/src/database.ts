import { Pool, PoolClient } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

interface TrafficRecord {
  id?: number;
  measurement_time?: string;
  county?: string;
  road_number?: string;
  punkt_nummer?: string;
  all_vehicles_count?: number;
  all_vehicles_avg_speed?: number;
  passenger_car_count?: number;
  passenger_car_avg_speed?: number;
  heavy_vehicles_count?: number;
  heavy_vehicles_avg_speed?: number;
  heavy_vehicles_trailer_count?: number;
  heavy_vehicles_trailer_avg_speed?: number;
  heavy_vehicles_no_trailer_count?: number;
  heavy_vehicles_no_trailer_avg_speed?: number;
  three_axle_tractor_trailer_count?: number;
  three_axle_tractor_trailer_avg_speed?: number;
  two_axle_tractor_trailer_count?: number;
  two_axle_tractor_trailer_avg_speed?: number;
  three_axle_tractor_no_trailer_count?: number;
  three_axle_tractor_no_trailer_avg_speed?: number;
  two_axle_tractor_no_trailer_count?: number;
  two_axle_tractor_no_trailer_avg_speed?: number;
  passenger_car_trailer_count?: number;
  passenger_car_trailer_avg_speed?: number;
  passenger_car_no_trailer_count?: number;
  passenger_car_no_trailer_avg_speed?: number;
  created_at?: string;
}

export class TrafficDatabase {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      user: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || '',
      database: process.env.DB_NAME || 'traffic_data',
    });

    this.pool.on('error', (err) => {
      console.error('Unexpected error on idle client', err);
    });
  }

  async connect(): Promise<void> {
    try {
      const client = await this.pool.connect();
      console.log('✓ Connected to PostgreSQL database');
      client.release();
    } catch (err) {
      console.error('✗ Failed to connect to database:', err);
      throw err;
    }
  }

  async getAllTrafficData(limit: number = 1000): Promise<TrafficRecord[]> {
    try {
      const result = await this.pool.query(
        'SELECT * FROM traffic_data ORDER BY measurement_time DESC LIMIT $1',
        [limit]
      );
      return result.rows;
    } catch (err) {
      console.error('Error fetching traffic data:', err);
      throw err;
    }
  }

  async getTrafficByLocation(location: string): Promise<TrafficRecord[]> {
    try {
      const result = await this.pool.query(
        `SELECT * FROM traffic_data 
         WHERE county ILIKE $1 OR road_number ILIKE $1 OR punkt_nummer ILIKE $1
         ORDER BY measurement_time DESC 
         LIMIT 1000`,
        [`%${location}%`]
      );
      return result.rows;
    } catch (err) {
      console.error('Error fetching traffic data by location:', err);
      throw err;
    }
  }

  async getAverageSpeedByVehicleType(vehicleType: string, startDate?: string, endDate?: string): Promise<any> {
    try {
      let query = `SELECT AVG(${vehicleType}_avg_speed) as average_speed FROM traffic_data`;
      const params: any[] = [];

      if (startDate && endDate) {
        query += ' WHERE measurement_time BETWEEN $1 AND $2';
        params.push(startDate, endDate);
      }

      const result = await this.pool.query(query, params);
      return result.rows[0] || { average_speed: null };
    } catch (err) {
      console.error('Error calculating average speed:', err);
      throw err;
    }
  }

  async getTrafficStats(): Promise<any> {
    try {
      const result = await this.pool.query(`
        SELECT 
          COUNT(*) as total_records,
          AVG(all_vehicles_avg_speed) as avg_all_vehicles_speed,
          AVG(heavy_vehicles_avg_speed) as avg_heavy_vehicles_speed,
          AVG(passenger_car_avg_speed) as avg_passenger_car_speed,
          MAX(all_vehicles_avg_speed) as max_speed,
          MIN(all_vehicles_avg_speed) as min_speed,
          COUNT(DISTINCT county) as unique_counties,
          COUNT(DISTINCT road_number) as unique_roads,
          COUNT(DISTINCT punkt_nummer) as unique_measurement_points
        FROM traffic_data
      `);
      return result.rows[0];
    } catch (err) {
      console.error('Error fetching traffic statistics:', err);
      throw err;
    }
  }

  async getTrafficByDateRange(startDate: string, endDate: string): Promise<TrafficRecord[]> {
    try {
      const result = await this.pool.query(
        `SELECT * FROM traffic_data 
         WHERE measurement_time BETWEEN $1 AND $2
         ORDER BY measurement_time DESC`,
        [startDate, endDate]
      );
      return result.rows;
    } catch (err) {
      console.error('Error fetching traffic data by date range:', err);
      throw err;
    }
  }

  async getTrafficByRoad(roadNumber: string): Promise<TrafficRecord[]> {
    try {
      const result = await this.pool.query(
        `SELECT * FROM traffic_data 
         WHERE road_number = $1
         ORDER BY measurement_time DESC 
         LIMIT 1000`,
        [roadNumber]
      );
      return result.rows;
    } catch (err) {
      console.error('Error fetching traffic data by road:', err);
      throw err;
    }
  }

  async getTrafficByCounty(county: string): Promise<TrafficRecord[]> {
    try {
      const result = await this.pool.query(
        `SELECT * FROM traffic_data 
         WHERE county ILIKE $1
         ORDER BY measurement_time DESC 
         LIMIT 1000`,
        [`%${county}%`]
      );
      return result.rows;
    } catch (err) {
      console.error('Error fetching traffic data by county:', err);
      throw err;
    }
  }

  async getTrafficByMeasurementPoint(punktNummer: string): Promise<TrafficRecord[]> {
    try {
      const result = await this.pool.query(
        `SELECT * FROM traffic_data 
         WHERE punkt_nummer = $1
         ORDER BY measurement_time DESC 
         LIMIT 1000`,
        [punktNummer]
      );
      return result.rows;
    } catch (err) {
      console.error('Error fetching traffic data by measurement point:', err);
      throw err;
    }
  }

  async getVehicleCountsComparison(startDate?: string, endDate?: string): Promise<any> {
    try {
      let query = `SELECT 
        AVG(all_vehicles_count) as avg_all_vehicles,
        AVG(passenger_car_count) as avg_passenger_cars,
        AVG(heavy_vehicles_count) as avg_heavy_vehicles,
        AVG(heavy_vehicles_trailer_count) as avg_heavy_with_trailer,
        AVG(heavy_vehicles_no_trailer_count) as avg_heavy_without_trailer,
        AVG(passenger_car_trailer_count) as avg_passenger_with_trailer,
        AVG(passenger_car_no_trailer_count) as avg_passenger_without_trailer
      FROM traffic_data`;
      
      const params: any[] = [];

      if (startDate && endDate) {
        query += ' WHERE measurement_time BETWEEN $1 AND $2';
        params.push(startDate, endDate);
      }

      const result = await this.pool.query(query, params);
      return result.rows[0];
    } catch (err) {
      console.error('Error comparing vehicle counts:', err);
      throw err;
    }
  }

  async getSpeedsComparison(startDate?: string, endDate?: string): Promise<any> {
    try {
      let query = `SELECT 
        AVG(all_vehicles_avg_speed) as avg_all_vehicles_speed,
        AVG(passenger_car_avg_speed) as avg_passenger_cars_speed,
        AVG(heavy_vehicles_avg_speed) as avg_heavy_vehicles_speed,
        AVG(heavy_vehicles_trailer_avg_speed) as avg_heavy_with_trailer_speed,
        AVG(heavy_vehicles_no_trailer_avg_speed) as avg_heavy_without_trailer_speed,
        AVG(passenger_car_trailer_avg_speed) as avg_passenger_with_trailer_speed,
        AVG(passenger_car_no_trailer_avg_speed) as avg_passenger_without_trailer_speed,
        AVG(three_axle_tractor_trailer_avg_speed) as avg_three_axle_trailer_speed,
        AVG(two_axle_tractor_trailer_avg_speed) as avg_two_axle_trailer_speed
      FROM traffic_data`;
      
      const params: any[] = [];

      if (startDate && endDate) {
        query += ' WHERE measurement_time BETWEEN $1 AND $2';
        params.push(startDate, endDate);
      }

      const result = await this.pool.query(query, params);
      return result.rows[0];
    } catch (err) {
      console.error('Error comparing speeds:', err);
      throw err;
    }
  }

  async close(): Promise<void> {
    await this.pool.end();
    console.log('✓ Database connection closed');
  }
}

export const db = new TrafficDatabase();
