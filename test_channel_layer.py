#!/usr/bin/env python3
import os
import django
import asyncio

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tracking_backend.settings')
django.setup()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def test_channel_layer():
    """Test if the channel layer is working"""
    try:
        channel_layer = get_channel_layer()
        print(f"✅ Channel layer found: {type(channel_layer)}")
        
        # Test sending a message
        async_to_sync(channel_layer.group_send)(
            'bus_tracking',
            {
                'type': 'bus_location_update',
                'bus_id': 999,
                'test': True,
                'message': 'Test message'
            }
        )
        print("✅ Test message sent successfully")
        
    except Exception as e:
        print(f"❌ Channel layer test failed: {e}")

if __name__ == "__main__":
    test_channel_layer()