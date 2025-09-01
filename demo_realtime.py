#!/usr/bin/env python3
import asyncio
import websockets
import json
from datetime import datetime

async def demo_realtime():
    uri = "ws://127.0.0.1:8000/ws/buses/"
    print("🚌 Real-time Bus Tracking Demo")
    print("=" * 50)
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket!")
            
            # Get initial data
            message = await websocket.recv()
            data = json.loads(message)
            print(f"📍 Initial data: {len(data.get('buses', []))} buses loaded")
            print("-" * 50)
            
            # Listen for real-time updates
            update_count = 0
            while update_count < 5:  # Show 5 updates
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                    data = json.loads(message)
                    
                    if data['type'] == 'location_update':
                        update_count += 1
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        location = data['location']
                        
                        print(f"🔄 [{timestamp}] Update #{update_count}")
                        print(f"   🚌 Bus ID: {data['bus_id']}")
                        print(f"   📍 Location: {location['latitude']}, {location['longitude']}")
                        print(f"   🏃 Speed: {location['speed']} km/h")
                        print(f"   🧭 Heading: {location['heading']}°")
                        print("-" * 30)
                        
                except asyncio.TimeoutError:
                    print("⏰ Waiting for next update...")
                    
            print("✅ Demo completed! Real-time updates working perfectly! 🎉")
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(demo_realtime())