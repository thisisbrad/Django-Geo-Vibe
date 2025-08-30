from django.contrib import admin
from .models import Route, Bus, BusLocation, RouteStop


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_number', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['route_number', 'name']
    ordering = ['route_number']


class BusLocationInline(admin.TabularInline):
    model = BusLocation
    extra = 0
    readonly_fields = ['timestamp', 'created_at']
    ordering = ['-timestamp']


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'license_plate', 'route', 'driver_name', 'is_active']
    list_filter = ['route', 'is_active', 'created_at']
    search_fields = ['bus_number', 'license_plate', 'driver_name']
    inlines = [BusLocationInline]
    ordering = ['bus_number']


@admin.register(BusLocation)
class BusLocationAdmin(admin.ModelAdmin):
    list_display = ['bus', 'latitude', 'longitude', 'speed', 'timestamp']
    list_filter = ['bus', 'timestamp']
    search_fields = ['bus__bus_number']
    readonly_fields = ['created_at']
    ordering = ['-timestamp']


class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 0
    ordering = ['stop_order']


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['stop_name', 'route', 'stop_order', 'is_active']
    list_filter = ['route', 'is_active']
    search_fields = ['stop_name', 'route__route_number']
    ordering = ['route', 'stop_order']
