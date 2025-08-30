from django.db import models
from django.utils import timezone


class Route(models.Model):
    """Represents a bus route in the city"""
    route_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#0066cc')  # Hex color for map display
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Route {self.route_number}: {self.name}"

    class Meta:
        ordering = ['route_number']


class Bus(models.Model):
    """Represents a bus vehicle"""
    bus_number = models.CharField(max_length=20, unique=True)
    license_plate = models.CharField(max_length=20, unique=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='buses')
    driver_name = models.CharField(max_length=100, blank=True)
    capacity = models.IntegerField(default=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bus {self.bus_number} - Route {self.route.route_number}"

    @property
    def current_location(self):
        """Get the most recent location of this bus"""
        return self.locations.order_by('-timestamp').first()

    class Meta:
        ordering = ['bus_number']
        verbose_name_plural = 'Buses'


class BusLocation(models.Model):
    """Represents a bus location at a specific time"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    speed = models.FloatField(default=0.0)  # km/h
    heading = models.FloatField(null=True, blank=True)  # degrees (0-360)
    accuracy = models.FloatField(null=True, blank=True)  # GPS accuracy in meters
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus.bus_number} at ({self.latitude}, {self.longitude}) - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['bus', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]


class RouteStop(models.Model):
    """Represents a bus stop on a route"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    stop_order = models.IntegerField()  # Order of this stop in the route
    estimated_time = models.TimeField(null=True, blank=True)  # Estimated arrival time
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stop_name} - Route {self.route.route_number}"

    class Meta:
        ordering = ['route', 'stop_order']
        unique_together = ['route', 'stop_order']
