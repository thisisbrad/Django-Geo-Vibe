from django.core.management.base import BaseCommand
from buses.models import Route, Bus, RouteStop, BusLocation
from django.utils import timezone
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create sample data for bus tracking system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create routes
        route1 = Route.objects.create(
            route_number='101',
            name='Downtown Loop',
            description='Connects downtown area with main attractions',
            color='#FF6B35'
        )

        route2 = Route.objects.create(
            route_number='202',
            name='University Express',
            description='Express route to university campus',
            color='#004E89'
        )

        route3 = Route.objects.create(
            route_number='303',
            name='Airport Shuttle',
            description='Direct service to airport',
            color='#009639'
        )

        # Create route stops for Route 101
        stops_101 = [
            {'name': 'Central Station', 'lat': Decimal('40.7589'), 'lng': Decimal('-73.9851')},
            {'name': 'City Hall', 'lat': Decimal('40.7614'), 'lng': Decimal('-73.9776')},
            {'name': 'Museum District', 'lat': Decimal('40.7505'), 'lng': Decimal('-73.9934')},
            {'name': 'Shopping Center', 'lat': Decimal('40.7549'), 'lng': Decimal('-73.9840')},
            {'name': 'Park Avenue', 'lat': Decimal('40.7505'), 'lng': Decimal('-73.9800')},
        ]

        for i, stop in enumerate(stops_101):
            RouteStop.objects.create(
                route=route1,
                stop_name=stop['name'],
                latitude=stop['lat'],
                longitude=stop['lng'],
                stop_order=i + 1
            )

        # Create route stops for Route 202
        stops_202 = [
            {'name': 'University Gate', 'lat': Decimal('40.8075'), 'lng': Decimal('-73.9626')},
            {'name': 'Student Center', 'lat': Decimal('40.8100'), 'lng': Decimal('-73.9580')},
            {'name': 'Library', 'lat': Decimal('40.8050'), 'lng': Decimal('-73.9550')},
            {'name': 'Sports Complex', 'lat': Decimal('40.8000'), 'lng': Decimal('-73.9500')},
        ]

        for i, stop in enumerate(stops_202):
            RouteStop.objects.create(
                route=route2,
                stop_name=stop['name'],
                latitude=stop['lat'],
                longitude=stop['lng'],
                stop_order=i + 1
            )

        # Create buses
        buses = [
            {'number': 'B101A', 'plate': 'NYC-1001', 'route': route1, 'driver': 'John Smith'},
            {'number': 'B101B', 'plate': 'NYC-1002', 'route': route1, 'driver': 'Mary Johnson'},
            {'number': 'B202A', 'plate': 'NYC-2001', 'route': route2, 'driver': 'David Wilson'},
            {'number': 'B303A', 'plate': 'NYC-3001', 'route': route3, 'driver': 'Sarah Brown'},
        ]

        created_buses = []
        for bus_data in buses:
            bus = Bus.objects.create(
                bus_number=bus_data['number'],
                license_plate=bus_data['plate'],
                route=bus_data['route'],
                driver_name=bus_data['driver'],
                capacity=50
            )
            created_buses.append(bus)

        # Create sample locations for buses
        base_locations = [
            {'lat': Decimal('40.7589'), 'lng': Decimal('-73.9851')},  # Route 101
            {'lat': Decimal('40.7614'), 'lng': Decimal('-73.9776')},  # Route 101
            {'lat': Decimal('40.8075'), 'lng': Decimal('-73.9626')},  # Route 202
            {'lat': Decimal('40.7000'), 'lng': Decimal('-73.8000')},  # Route 303
        ]

        for i, bus in enumerate(created_buses):
            base_lat = base_locations[i]['lat']
            base_lng = base_locations[i]['lng']
            
            # Create recent location
            BusLocation.objects.create(
                bus=bus,
                latitude=base_lat + Decimal(str(random.uniform(-0.01, 0.01))),
                longitude=base_lng + Decimal(str(random.uniform(-0.01, 0.01))),
                speed=random.uniform(20, 60),
                heading=random.uniform(0, 360),
                timestamp=timezone.now()
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )