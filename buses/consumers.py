import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Bus, BusLocation
from .serializers import BusTrackingSerializer


class BusTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'bus_tracking'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial data
        initial_data = await self.get_all_buses_data()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'buses': initial_data
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'get_buses':
            buses_data = await self.get_all_buses_data()
            await self.send(text_data=json.dumps({
                'type': 'buses_update',
                'buses': buses_data
            }))
    
    # Receive message from room group
    async def bus_location_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'bus_id': event['bus_id'],
            'location': event['location']
        }))
    
    async def bus_status_update(self, event):
        # Send bus status update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'bus_id': event['bus_id'],
            'status': event['status']
        }))
    
    @database_sync_to_async
    def get_all_buses_data(self):
        buses = Bus.objects.filter(is_active=True)
        serializer = BusTrackingSerializer(buses, many=True)
        return serializer.data


class RouteTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.route_id = self.scope['url_route']['kwargs']['route_id']
        self.room_group_name = f'route_{self.route_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial data for this route
        initial_data = await self.get_route_buses_data()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'route_id': self.route_id,
            'buses': initial_data
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'get_route_buses':
            buses_data = await self.get_route_buses_data()
            await self.send(text_data=json.dumps({
                'type': 'route_buses_update',
                'route_id': self.route_id,
                'buses': buses_data
            }))
    
    # Receive message from room group
    async def bus_location_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'bus_id': event['bus_id'],
            'location': event['location']
        }))
    
    @database_sync_to_async
    def get_route_buses_data(self):
        buses = Bus.objects.filter(route_id=self.route_id, is_active=True)
        serializer = BusTrackingSerializer(buses, many=True)
        return serializer.data