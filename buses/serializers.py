from rest_framework import serializers
from .models import Route, Bus, BusLocation, RouteStop


class RouteStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStop
        fields = ['id', 'stop_name', 'latitude', 'longitude', 'stop_order', 'estimated_time', 'is_active']


class RouteSerializer(serializers.ModelSerializer):
    stops = RouteStopSerializer(many=True, read_only=True)
    buses_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ['id', 'route_number', 'name', 'description', 'color', 'is_active', 
                 'stops', 'buses_count', 'created_at', 'updated_at']

    def get_buses_count(self, obj):
        return obj.buses.filter(is_active=True).count()


class BusLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusLocation
        fields = ['id', 'latitude', 'longitude', 'speed', 'heading', 'accuracy', 'timestamp']


class BusSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    route_id = serializers.IntegerField(write_only=True)
    current_location = BusLocationSerializer(read_only=True)
    recent_locations = serializers.SerializerMethodField()

    class Meta:
        model = Bus
        fields = ['id', 'bus_number', 'license_plate', 'route', 'route_id', 'driver_name', 
                 'capacity', 'is_active', 'current_location', 'recent_locations', 'created_at', 'updated_at']

    def get_recent_locations(self, obj):
        # Get last 10 locations for this bus
        locations = obj.locations.order_by('-timestamp')[:10]
        return BusLocationSerializer(locations, many=True).data


class BusLocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusLocation
        fields = ['latitude', 'longitude', 'speed', 'heading', 'accuracy']


class BusTrackingSerializer(serializers.ModelSerializer):
    """Optimized serializer for real-time tracking"""
    route_number = serializers.CharField(source='route.route_number', read_only=True)
    route_color = serializers.CharField(source='route.color', read_only=True)
    current_location = BusLocationSerializer(read_only=True)

    class Meta:
        model = Bus
        fields = ['id', 'bus_number', 'route_number', 'route_color', 'current_location']