#!/usr/bin/env python3
"""
Comprehensive test of the enhanced MCP server with all vehicle type combinations.
"""

import sys
sys.path.insert(0, '/Users/arif.ahsan/Documents/GitHub/trafficdata/trafffic-mcp')

from server import load_traffic_data, calculate_statistics, format_statistics, VEHICLE_TYPES, generate_speed_graph
import base64


def test_load_all_vehicle_types():
    """Test loading all vehicle type data."""
    print("Testing load_traffic_data() for all vehicle types...")
    data = load_traffic_data()
    
    assert data is not None, "Data is None"
    assert "timestamps" in data, "Missing timestamps"
    
    print(f"  ✓ Loaded {len(data['timestamps'])} records")
    print(f"\n  Vehicle Types Available:")
    
    for vehicle_key, vehicle_info in VEHICLE_TYPES.items():
        if vehicle_key in data:
            speeds = data[vehicle_key]
            valid_speeds = [s for s in speeds if s > 0]
            print(f"    - {vehicle_info['name']}: {len(valid_speeds)} data points")
    
    return data


def test_all_statistics(data):
    """Test statistics calculation for all vehicle types."""
    print("\n\nTesting statistics for all vehicle types...")
    print("=" * 70)
    
    results = {}
    for vehicle_key, vehicle_info in VEHICLE_TYPES.items():
        if vehicle_key in data:
            speeds = data[vehicle_key]
            stats = calculate_statistics(speeds)
            if stats:
                results[vehicle_key] = stats
                formatted = format_statistics(vehicle_info['name'], stats)
                print(f"\n{formatted}")
    
    return results


def test_vehicle_combinations(data):
    """Test specific vehicle combinations requested by user."""
    print("\n\nTesting Specific Vehicle Combinations:")
    print("=" * 70)
    
    # Group combinations
    combinations = {
        "Heavy Vehicles": ["heavy_vehicles", "heavy_with_trailer", "heavy_without_trailer"],
        "Passenger Cars": ["passenger_cars", "passenger_with_trailer", "passenger_without_trailer"],
        "Tractors": ["two_axle_with_trailer", "three_axle_with_trailer", 
                     "two_axle_without_trailer", "three_axle_without_trailer"],
    }
    
    for group_name, vehicle_keys in combinations.items():
        print(f"\n{group_name}:")
        print("-" * 70)
        for vehicle_key in vehicle_keys:
            if vehicle_key in VEHICLE_TYPES:
                speeds = data.get(vehicle_key, [])
                stats = calculate_statistics(speeds)
                if stats:
                    vehicle_name = VEHICLE_TYPES[vehicle_key]["name"]
                    print(f"  {vehicle_name:<40} Avg: {stats['average']:6.2f} km/h | Count: {stats['count']}")


def test_comparison_graph(data):
    """Test graph generation with different vehicle combinations."""
    print("\n\nTesting Graph Generation...")
    print("=" * 70)
    
    test_cases = [
        (
            "Heavy vs Passenger",
            ["heavy_vehicles", "passenger_cars"]
        ),
        (
            "Heavy: With/Without Trailer",
            ["heavy_with_trailer", "heavy_without_trailer"]
        ),
        (
            "Passenger: With/Without Trailer",
            ["passenger_with_trailer", "passenger_without_trailer"]
        ),
        (
            "All Tractors",
            ["two_axle_with_trailer", "three_axle_with_trailer", 
             "two_axle_without_trailer", "three_axle_without_trailer"]
        ),
    ]
    
    for description, vehicle_types in test_cases:
        print(f"\n  Generating graph: {description}")
        img_base64 = generate_speed_graph(vehicle_types)
        
        if img_base64:
            img_bytes = base64.b64decode(img_base64)
            assert img_bytes[:8] == b'\x89PNG\r\n\x1a\n', "Invalid PNG signature"
            print(f"    ✓ Generated successfully ({len(img_bytes)} bytes)")
        else:
            print(f"    ✗ Failed to generate graph")
            return False
    
    return True


if __name__ == "__main__":
    try:
        print("=" * 70)
        print("Enhanced MCP Server - All Vehicle Types Test")
        print("=" * 70)
        
        data = test_load_all_vehicle_types()
        results = test_all_statistics(data)
        test_vehicle_combinations(data)
        graph_success = test_comparison_graph(data)
        
        print("\n" + "=" * 70)
        if graph_success:
            print("✓ All tests passed!")
        else:
            print("✗ Some graph tests failed!")
        print("=" * 70)
        
        sys.exit(0 if graph_success else 1)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
