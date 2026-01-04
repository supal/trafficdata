import { db } from './database.js';

export interface Statistics {
  count: number;
  average: number;
  min: number;
  max: number;
  median: number;
}

export function calculateStatistics(values: number[]): Statistics | null {
  const validValues = values.filter(v => v > 0).sort((a, b) => a - b);
  if (validValues.length === 0) return null;

  const sum = validValues.reduce((a, b) => a + b, 0);
  const mean = sum / validValues.length;
  const median = validValues.length % 2 === 0
    ? (validValues[validValues.length / 2 - 1] + validValues[validValues.length / 2]) / 2
    : validValues[Math.floor(validValues.length / 2)];

  return {
    count: validValues.length,
    average: Math.round(mean * 100) / 100,
    min: Math.round(validValues[0] * 100) / 100,
    max: Math.round(validValues[validValues.length - 1] * 100) / 100,
    median: Math.round(median * 100) / 100,
  };
}

export function formatStatistics(vehicleName: string, stats: Statistics | null): string {
  if (!stats) {
    return `${vehicleName}:\n  No data available`;
  }

  return `${vehicleName}:
  Average Speed: ${stats.average} km/h
  Min Speed: ${stats.min} km/h
  Max Speed: ${stats.max} km/h
  Median Speed: ${stats.median} km/h
  Data Points: ${stats.count}`;
}

export async function generateSpeedGraph(
  vehicleTypes?: string[],
  startDate?: string,
  endDate?: string
): Promise<string | null> {
  try {
    // Get traffic data
    let data: any[] = [];
    
    if (startDate && endDate) {
      data = await db.getTrafficByDateRange(startDate, endDate);
    } else {
      data = await db.getAllTrafficData(10000);
    }

    if (!data || data.length === 0) {
      return null;
    }

    // Default vehicle types if not specified
    if (!vehicleTypes) {
      vehicleTypes = ['heavy_vehicles_avg_speed', 'passenger_car_avg_speed'];
    }

    // Group data by time
    const timeSeriesMap = new Map<string, any>();
    
    for (const record of data) {
      const timeKey = record.measurement_time ? new Date(record.measurement_time).toISOString().split('T')[0] : 'unknown';
      if (!timeSeriesMap.has(timeKey)) {
        timeSeriesMap.set(timeKey, {});
      }
      const dayData = timeSeriesMap.get(timeKey);
      
      // Aggregate speeds
      for (const vehicleType of vehicleTypes) {
        if (!dayData[vehicleType]) {
          dayData[vehicleType] = [];
        }
        if (record[vehicleType] && record[vehicleType] > 0) {
          dayData[vehicleType].push(record[vehicleType]);
        }
      }
    }

    // Calculate daily averages
    const timeSeries: any[] = [];
    const sortedDates = Array.from(timeSeriesMap.keys()).sort();
    
    for (const date of sortedDates) {
      const dayData = timeSeriesMap.get(date)!;
      const point: any = { date };
      
      for (const vehicleType of vehicleTypes) {
        const speeds = dayData[vehicleType] || [];
        if (speeds.length > 0) {
          const avg = speeds.reduce((a: number, b: number) => a + b, 0) / speeds.length;
          point[vehicleType] = Math.round(avg * 100) / 100;
        }
      }
      timeSeries.push(point);
    }

    // Generate text-based chart (ASCII art)
    const chart = generateTextChart(timeSeries, vehicleTypes);
    return chart;
  } catch (error) {
    console.error('Error generating speed graph:', error);
    return null;
  }
}

function generateTextChart(data: any[], vehicleTypes: string[]): string {
  if (data.length === 0) return 'No data available';

  // Get max speed for scaling
  let maxSpeed = 0;
  for (const point of data) {
    for (const vehicleType of vehicleTypes) {
      if (point[vehicleType] && point[vehicleType] > maxSpeed) {
        maxSpeed = point[vehicleType];
      }
    }
  }

  maxSpeed = Math.ceil(maxSpeed / 10) * 10; // Round up to nearest 10
  const maxSpeed100 = Math.max(100, maxSpeed);

  // Build chart
  let chart = '\nAverage Speed Trends Over Time\n';
  chart += '=' .repeat(80) + '\n\n';

  // Legend
  const colors = {
    'heavy_vehicles_avg_speed': '🔴 Heavy Vehicles',
    'passenger_car_avg_speed': '🔵 Passenger Cars',
    'heavy_vehicles_trailer_avg_speed': '🔶 Heavy w/ Trailer',
    'passenger_car_trailer_avg_speed': '🟦 Passenger w/ Trailer',
  };

  chart += 'Legend:\n';
  for (const [key, label] of Object.entries(colors)) {
    if (vehicleTypes.includes(key)) {
      chart += `  ${label}\n`;
    }
  }
  chart += '\n';

  // Y-axis labels
  const lines = 20;
  for (let y = lines; y >= 0; y--) {
    const speed = Math.round((y / lines) * maxSpeed100);
    const speedStr = speed.toString().padStart(4);
    chart += `${speedStr} | `;

    // Plot data points
    for (let x = 0; x < data.length; x++) {
      const point = data[x];
      let char = ' ';
      
      for (const vehicleType of vehicleTypes) {
        const speedVal = point[vehicleType];
        if (speedVal && Math.abs((speedVal / maxSpeed100 * lines) - y) < 0.5) {
          char = '●';
          break;
        }
      }
      chart += char;
    }
    chart += '\n';
  }

  // X-axis
  chart += '     +' + '-'.repeat(Math.min(data.length, 60)) + '\n';
  
  // X-axis labels (show every nth date)
  const step = Math.ceil(data.length / 10);
  chart += '     ';
  for (let x = 0; x < data.length; x += step) {
    const date = data[x].date;
    chart += date.substring(5, 10); // MM-DD format
  }
  chart += '\n';

  chart += '\nData points: ' + data.length + '\n';
  chart += 'Y-axis range: 0 - ' + maxSpeed100 + ' km/h\n';

  return chart;
}

export async function analyzePeakHours(vehicleType?: string): Promise<string> {
  try {
    const data = await db.getAllTrafficData(10000);
    if (!data || data.length === 0) {
      return 'No data available';
    }

    // Group by hour
    const hourMap = new Map<number, number[]>();
    
    for (const record of data) {
      if (!record.measurement_time) continue;
      
      const date = new Date(record.measurement_time);
      const hour = date.getHours();
      
      let speedValue = 0;
      if (vehicleType) {
        const speedKey = `${vehicleType}_avg_speed` as keyof typeof record;
        speedValue = (record[speedKey] as any) || 0;
      } else {
        speedValue = record.all_vehicles_avg_speed || 0;
      }
      
      if (speedValue > 0) {
        if (!hourMap.has(hour)) {
          hourMap.set(hour, []);
        }
        hourMap.get(hour)!.push(speedValue);
      }
    }

    // Calculate average for each hour
    const hourlyData: any[] = [];
    for (let hour = 0; hour < 24; hour++) {
      const speeds = hourMap.get(hour) || [];
      if (speeds.length > 0) {
        const avg = speeds.reduce((a, b) => a + b, 0) / speeds.length;
        hourlyData.push({
          hour: `${hour.toString().padStart(2, '0')}:00`,
          average: Math.round(avg * 100) / 100,
          count: speeds.length,
        });
      }
    }

    // Find peak hours
    const sorted = [...hourlyData].sort((a, b) => b.average - a.average);
    const peak = sorted.slice(0, 5);
    const lowest = sorted.slice(-5).reverse();

    let result = `\nTraffic Pattern Analysis\n`;
    result += `${'='.repeat(60)}\n`;
    
    if (vehicleType) {
      result += `Vehicle Type: ${vehicleType}\n\n`;
    } else {
      result += `All Vehicles Average\n\n`;
    }

    result += `Peak Hours (Highest Average Speeds):\n`;
    for (const hour of peak) {
      result += `  ${hour.hour}: ${hour.average} km/h (${hour.count} data points)\n`;
    }

    result += `\nLowest Hours (Lowest Average Speeds):\n`;
    for (const hour of lowest) {
      result += `  ${hour.hour}: ${hour.average} km/h (${hour.count} data points)\n`;
    }

    return result;
  } catch (error) {
    console.error('Error analyzing peak hours:', error);
    return 'Error analyzing traffic patterns';
  }
}

// Transform traffic data to long format
export interface LongFormatRecord {
  measurement_time: string;
  county: string;
  road_number: string;
  punkt_nummer: string;
  vehicle_type: string;
  count: number;
  avg_speed: number;
}

export async function transformToLongFormat(limit?: number): Promise<LongFormatRecord[]> {
  try {
    const data = await db.getAllTrafficData(limit || 5000);
    const longFormat: LongFormatRecord[] = [];

    const vehicleTypes = [
      'all_vehicles',
      'passenger_car',
      'heavy_vehicles',
      'heavy_vehicles_trailer',
      'heavy_vehicles_no_trailer',
      'three_axle_tractor_trailer',
      'two_axle_tractor_trailer',
      'three_axle_tractor_no_trailer',
      'two_axle_tractor_no_trailer',
      'passenger_car_trailer',
      'passenger_car_no_trailer',
    ];

    for (const record of data) {
      for (const vehicleType of vehicleTypes) {
        const countKey = `${vehicleType}_count` as keyof typeof record;
        const speedKey = `${vehicleType}_avg_speed` as keyof typeof record;
        
        const count = parseInt(String((record[countKey] as any) || 0));
        const speed = parseFloat(String((record[speedKey] as any) || 0));

        if (count > 0 || speed > 0) {
          longFormat.push({
            measurement_time: String(record.measurement_time || ''),
            county: String(record.county || ''),
            road_number: String(record.road_number || ''),
            punkt_nummer: String(record.punkt_nummer || ''),
            vehicle_type: vehicleType,
            count,
            avg_speed: speed,
          });
        }
      }
    }

    return longFormat;
  } catch (error) {
    console.error('Error transforming to long format:', error);
    return [];
  }
}

// Generate bar chart for average speeds
export async function generateSpeedBarChart(): Promise<string> {
  try {
    const data = await db.getAllTrafficData(5000);
    
    const vehicleTypeMap = new Map<string, number[]>();
    const vehicleTypeLabels: { [key: string]: string } = {
      all_vehicles: 'All Vehicles',
      passenger_car: 'Passenger Cars',
      heavy_vehicles: 'Heavy Vehicles',
      heavy_vehicles_trailer: 'HV with Trailer',
      heavy_vehicles_no_trailer: 'HV no Trailer',
      three_axle_tractor_trailer: '3-Axle Tractor+Trailer',
      two_axle_tractor_trailer: '2-Axle Tractor+Trailer',
      three_axle_tractor_no_trailer: '3-Axle Tractor',
      two_axle_tractor_no_trailer: '2-Axle Tractor',
      passenger_car_trailer: 'Passenger+Trailer',
      passenger_car_no_trailer: 'Passenger Car (no Trailer)',
    };

    for (const record of data) {
      for (const [vehicleType, label] of Object.entries(vehicleTypeLabels)) {
        const speedKey = `${vehicleType}_avg_speed` as keyof typeof record;
        const speed = parseFloat(String((record[speedKey] as any) || 0));
        
        if (speed > 0) {
          if (!vehicleTypeMap.has(vehicleType)) {
            vehicleTypeMap.set(vehicleType, []);
          }
          vehicleTypeMap.get(vehicleType)!.push(speed);
        }
      }
    }

    let result = '\n╔════════════════════════════════════════════════════╗\n';
    result += '║         AVERAGE SPEED BY VEHICLE TYPE             ║\n';
    result += '╚════════════════════════════════════════════════════╝\n\n';

    const entries = Array.from(vehicleTypeMap.entries())
      .map(([type, speeds]) => ({
        type,
        label: vehicleTypeLabels[type],
        average: speeds.reduce((a, b) => a + b, 0) / speeds.length,
      }))
      .sort((a, b) => b.average - a.average);

    const maxSpeed = Math.max(...entries.map(e => e.average));
    const barWidth = 40;

    for (const entry of entries) {
      const barLength = Math.round((entry.average / maxSpeed) * barWidth);
      const bar = '█'.repeat(barLength) + '░'.repeat(barWidth - barLength);
      result += `${entry.label.padEnd(25)} │${bar}│ ${entry.average.toFixed(1)} km/h\n`;
    }

    result += '\n';
    return result;
  } catch (error) {
    console.error('Error generating speed bar chart:', error);
    return 'Error generating chart';
  }
}

// Generate bar chart for vehicle counts
export async function generateVehicleCountBarChart(): Promise<string> {
  try {
    const data = await db.getAllTrafficData(5000);
    
    const vehicleTypeMap = new Map<string, number[]>();
    const vehicleTypeLabels: { [key: string]: string } = {
      all_vehicles: 'All Vehicles',
      passenger_car: 'Passenger Cars',
      heavy_vehicles: 'Heavy Vehicles',
      heavy_vehicles_trailer: 'HV with Trailer',
      heavy_vehicles_no_trailer: 'HV no Trailer',
      three_axle_tractor_trailer: '3-Axle Tractor+Trailer',
      two_axle_tractor_trailer: '2-Axle Tractor+Trailer',
      three_axle_tractor_no_trailer: '3-Axle Tractor',
      two_axle_tractor_no_trailer: '2-Axle Tractor',
      passenger_car_trailer: 'Passenger+Trailer',
      passenger_car_no_trailer: 'Passenger Car (no Trailer)',
    };

    for (const record of data) {
      for (const [vehicleType, label] of Object.entries(vehicleTypeLabels)) {
        const countKey = `${vehicleType}_count` as keyof typeof record;
        const count = parseInt(String((record[countKey] as any) || 0));
        
        if (count > 0) {
          if (!vehicleTypeMap.has(vehicleType)) {
            vehicleTypeMap.set(vehicleType, []);
          }
          vehicleTypeMap.get(vehicleType)!.push(count);
        }
      }
    }

    let result = '\n╔════════════════════════════════════════════════════╗\n';
    result += '║        AVERAGE VEHICLE COUNT BY TYPE               ║\n';
    result += '╚════════════════════════════════════════════════════╝\n\n';

    const entries = Array.from(vehicleTypeMap.entries())
      .map(([type, counts]) => ({
        type,
        label: vehicleTypeLabels[type],
        average: counts.reduce((a, b) => a + b, 0) / counts.length,
      }))
      .sort((a, b) => b.average - a.average);

    const maxCount = Math.max(...entries.map(e => e.average));
    const barWidth = 40;

    for (const entry of entries) {
      const barLength = Math.round((entry.average / maxCount) * barWidth);
      const bar = '█'.repeat(barLength) + '░'.repeat(barWidth - barLength);
      result += `${entry.label.padEnd(25)} │${bar}│ ${entry.average.toFixed(1)} vehicles\n`;
    }

    result += '\n';
    return result;
  } catch (error) {
    console.error('Error generating vehicle count chart:', error);
    return 'Error generating chart';
  }
}
