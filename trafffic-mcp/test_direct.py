#!/usr/bin/env python3
"""
Direct test of server functions without using MCP protocol.
"""

import sys
sys.path.insert(0, '/Users/arif.ahsan/Documents/GitHub/trafficdata/trafffic-mcp')

from server import load_traffic_data, generate_speed_graph
import statistics
import base64


def test_load_traffic_data():
    """Test loading traffic data."""
    print("Testing load_traffic_data()...")
    data = load_traffic_data()
    
    assert data is not None, "Data is None"
    assert "timestamps" in data, "Missing timestamps"
    assert "heavy_speeds" in data, "Missing heavy_speeds"
    assert "passenger_speeds" in data, "Missing passenger_speeds"
    
    timestamps = data['timestamps']
    heavy_speeds = data['heavy_speeds']
    passenger_speeds = data['passenger_speeds']
    
    assert len(timestamps) > 0, "No timestamps"
    assert len(heavy_speeds) > 0, "No heavy speeds"
    assert len(passenger_speeds) > 0, "No passenger speeds"
    assert len(timestamps) == len(heavy_speeds), "Timestamp/heavy speed mismatch"
    assert len(timestamps) == len(passenger_speeds), "Timestamp/passenger speed mismatch"
    
    print(f"  ✓ Loaded {len(timestamps)} records")
    print(f"    - Timestamps: {len(timestamps)} records")
    print(f"    - Heavy speeds: {len(heavy_speeds)} records")
    print(f"    - Passenger speeds: {len(passenger_speeds)} records")
    return data


def test_average_speeds(data):
    """Test average speed calculations."""
    print("\nTesting average speed calculations...")
    
    heavy_speeds = [s for s in data['heavy_speeds'] if s > 0]
    passenger_speeds = [s for s in data['passenger_speeds'] if s > 0]
    
    assert len(heavy_speeds) > 0, "No valid heavy speeds"
    assert len(passenger_speeds) > 0, "No valid passenger speeds"
    
    heavy_avg = statistics.mean(heavy_speeds)
    passenger_avg = statistics.mean(passenger_speeds)
    
    print(f"  ✓ Heavy vehicles statistics:")
    print(f"    - Average Speed: {heavy_avg:.2f} km/h")
    print(f"    - Min Speed: {min(heavy_speeds):.2f} km/h")
    print(f"    - Max Speed: {max(heavy_speeds):.2f} km/h")
    print(f"    - Data Points: {len(heavy_speeds)}")
    
    print(f"  ✓ Passenger cars statistics:")
    print(f"    - Average Speed: {passenger_avg:.2f} km/h")
    print(f"    - Min Speed: {min(passenger_speeds):.2f} km/h")
    print(f"    - Max Speed: {max(passenger_speeds):.2f} km/h")
    print(f"    - Data Points: {len(passenger_speeds)}")


def test_graph_generation():
    """Test graph generation."""
    print("\nTesting speed_graph()...")
    
    img_base64 = generate_speed_graph()
    assert img_base64 is not None, "Graph generation failed"
    assert len(img_base64) > 0, "Graph data is empty"
    
    # Verify it can be decoded
    img_bytes = base64.b64decode(img_base64)
    assert len(img_bytes) > 0, "Decoded image is empty"
    
    # Verify it's a valid PNG (PNG signature)
    assert img_bytes[:8] == b'\x89PNG\r\n\x1a\n', "Invalid PNG signature"
    
    # Save for inspection
    output_path = "/Users/arif.ahsan/Documents/GitHub/trafficdata/trafffic-mcp/traffic_speed_graph_direct_test.png"
    with open(output_path, 'wb') as f:
        f.write(img_bytes)
    
    print(f"  ✓ Graph generated successfully!")
    print(f"    - Base64 data length: {len(img_base64)} characters")
    print(f"    - PNG file size: {len(img_bytes)} bytes")
    print(f"    - Saved to: {output_path}")


if __name__ == "__main__":
    try:
        print("=" * 60)
        print("Running MCP Server Direct Function Tests")
        print("=" * 60)
        
        data = test_load_traffic_data()
        test_average_speeds(data)
        test_graph_generation()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
