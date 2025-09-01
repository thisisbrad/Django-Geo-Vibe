#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/buses/"
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket!")
            
            # Listen for initial data
            message = await websocket.recv()
            data = json.loads(message)
            print(f"📨 Received: {data['type']}")
            if data['type'] == 'initial_data':
                print(f"📍 Initial buses: {len(data['buses'])}")
            
            print("👂 Listening for updates...")
            # Listen for more messages
            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    data = json.loads(message)
                    print(f"📨 Received update: {data}")
                except asyncio.TimeoutError:
                    print("⏰ No updates received in 10 seconds, continuing...")
                    continue
                except websockets.exceptions.ConnectionClosed:
                    print("🔌 Connection closed")
                    break
                    
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())