from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q

from .models import Route, Bus, BusLocation, RouteStop
from .serializers import (
    RouteSerializer, BusSerializer, BusLocationSerializer, 
    BusLocationCreateSerializer, BusTrackingSerializer, RouteStopSerializer
)


class RouteViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bus routes"""
    queryset = Route.objects.filter(is_active=True)
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def buses(self, request, pk=None):
        """Get all active buses for this route"""
        route = self.get_object()
        buses = route.buses.filter(is_active=True)
        serializer = BusTrackingSerializer(buses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stops(self, request, pk=None):
        """Get all stops for this route"""
        route = self.get_object()
        stops = route.stops.filter(is_active=True).order_by('stop_order')
        serializer = RouteStopSerializer(stops, many=True)
        return Response(serializer.data)


class BusViewSet(viewsets.ModelViewSet):
    """ViewSet for managing buses"""
    queryset = Bus.objects.filter(is_active=True)
    serializer_class = BusSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Bus.objects.filter(is_active=True)
        route_id = self.request.query_params.get('route', None)
        if route_id is not None:
            queryset = queryset.filter(route_id=route_id)
        return queryset

    @action(detail=True, methods=['get'])
    def locations(self, request, pk=None):
        """Get location history for a specific bus"""
        bus = self.get_object()
        hours = request.query_params.get('hours', 24)
        try:
            hours = int(hours)
        except ValueError:
            hours = 24
        
        since = timezone.now() - timedelta(hours=hours)
        locations = bus.locations.filter(timestamp__gte=since).order_by('-timestamp')
        serializer = BusLocationSerializer(locations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        """Update the location of a specific bus"""
        bus = self.get_object()
        serializer = BusLocationCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(bus=bus)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def tracking(self, request):
        """Get real-time tracking data for all active buses"""
        buses = self.get_queryset()
        serializer = BusTrackingSerializer(buses, many=True)
        return Response(serializer.data)


class BusLocationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bus locations"""
    queryset = BusLocation.objects.all()
    serializer_class = BusLocationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = BusLocation.objects.all()
        bus_id = self.request.query_params.get('bus', None)
        if bus_id is not None:
            queryset = queryset.filter(bus_id=bus_id)
        
        # Filter by time range
        hours = self.request.query_params.get('hours', None)
        if hours:
            try:
                hours = int(hours)
                since = timezone.now() - timedelta(hours=hours)
                queryset = queryset.filter(timestamp__gte=since)
            except ValueError:
                pass
        
        return queryset.order_by('-timestamp')

    def perform_create(self, serializer):
        """Create a new location entry"""
        serializer.save()

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get the latest location for each active bus"""
        buses = Bus.objects.filter(is_active=True)
        latest_locations = []
        
        for bus in buses:
            location = bus.current_location
            if location:
                data = BusLocationSerializer(location).data
                data['bus_info'] = {
                    'id': bus.id,
                    'bus_number': bus.bus_number,
                    'route_number': bus.route.route_number,
                    'route_color': bus.route.color
                }
                latest_locations.append(data)
        
        return Response(latest_locations)


class RouteStopViewSet(viewsets.ModelViewSet):
    """ViewSet for managing route stops"""
    queryset = RouteStop.objects.filter(is_active=True)
    serializer_class = RouteStopSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = RouteStop.objects.filter(is_active=True)
        route_id = self.request.query_params.get('route', None)
        if route_id is not None:
            queryset = queryset.filter(route_id=route_id)
        return queryset.order_by('route', 'stop_order')
