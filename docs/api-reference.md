# API Reference

## Routes API

### List all routes
```
GET /api/routes/
```

### Get route details
```
GET /api/routes/{id}/
```

### Get buses for a route
```
GET /api/routes/{id}/buses/
```

### Get stops for a route
```
GET /api/routes/{id}/stops/
```

## Buses API

### List all buses
```
GET /api/buses/
```

### Get bus details
```
GET /api/buses/{id}/
```

### Get bus location history
```
GET /api/buses/{id}/locations/
```

### Update bus location
```
POST /api/buses/{id}/update_location/
```

### Get real-time tracking data
```
GET /api/buses/tracking/
```

## Locations API

### List all locations
```
GET /api/locations/
```

### Get latest location for each bus
```
GET /api/locations/latest/
```

## Route Stops API

### List all route stops
```
GET /api/route_stops/
```

### Get route stop details
```
GET /api/route_stops/{id}/
```