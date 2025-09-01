import requests
import random
import time
import json
from decimal import Decimal

# API base URL
API_BASE = 'http://localhost:8000/api'

def simulate_bus_movements():
    """Simulate real-time bus movements by updating their locations"""
    
    # Get all active buses
    try:
        response = requests.get(f'{API_BASE}/buses/')
        buses = response.json()
        print(f"Found {len(buses)} active buses")
    except Exception as e:
        print(f"Error fetching buses: {e}")
        return
    
    # Update each bus location with slight movement
    for bus in buses:
        if bus.get('current_location'):
            current_lat = float(bus['current_location']['latitude'])
            current_lng = float(bus['current_location']['longitude'])
            
            # Simulate small movement (within ~100 meters)
            lat_change = random.uniform(-0.001, 0.001)  # ~110m
            lng_change = random.uniform(-0.001, 0.001)  # ~110m
            
            new_lat = current_lat + lat_change
            new_lng = current_lng + lng_change
            
            # Random speed between 20-60 km/h
            speed = random.uniform(20, 60)
            
            # Random heading
            heading = random.uniform(0, 360)
            
            # Create location update
            location_data = {
                'latitude': round(new_lat, 8),  # Round to 8 decimal places to fit DecimalField(max_digits=10, decimal_places=8)
                'longitude': round(new_lng, 8), # Round to 8 decimal places to fit DecimalField(max_digits=11, decimal_places=8)
                'speed': round(speed, 2),
                'heading': round(heading, 2),
                'accuracy': round(random.uniform(3, 10), 2)  # GPS accuracy in meters
            }
            
            try:
                # Update bus location
                update_url = f"{API_BASE}/buses/{bus['id']}/update_location/"
                response = requests.post(update_url, json=location_data)
                
                if response.status_code == 201:
                    print(f"✅ Updated {bus['bus_number']} - Lat: {new_lat:.6f}, Lng: {new_lng:.6f}, Speed: {speed:.1f} km/h")
                else:
                    print(f"❌ Failed to update {bus['bus_number']}: {response.status_code}")
                    print(f"   Error response: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error updating {bus['bus_number']}: {e}")

def main():
    print("🚌 Starting Bus Movement Simulation...")
    print("📍 Updating bus locations every 10 seconds")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        while True:
            simulate_bus_movements()
            print("⏳ Waiting 10 seconds for next update...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\\n🛑 Simulation stopped by user")
    except Exception as e:
        print(f"\\n❌ Simulation error: {e}")

if __name__ == "__main__":
    main()