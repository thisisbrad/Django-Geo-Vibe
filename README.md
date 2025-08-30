# Bus Tracking System

A real-time bus tracking application built with Django REST API backend and React frontend with interactive maps.

## Features

🚌 **Real-time Bus Tracking**: Track multiple buses on an interactive map
🗺️ **Interactive Maps**: Powered by Leaflet and OpenStreetMap
🛣️ **Route Management**: Manage bus routes with colored visualization
📡 **WebSocket Updates**: Live location updates without page refresh
🎨 **Responsive Design**: Works on desktop and mobile devices
📊 **Admin Panel**: Django admin for managing buses, routes, and locations

## Technology Stack

### Backend

- **Django 5.2**: Web framework
- **Django REST Framework**: API development
- **WebSockets (Channels)**: Real-time communication
- **SQLite**: Database (easily upgradeable to PostgreSQL)
- **Redis**: WebSocket channel layer (optional, falls back to in-memory)

### Frontend

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Leaflet**: Interactive maps
- **React-Leaflet**: React integration for Leaflet
- **Axios**: HTTP client

## Quick Start

### 1. Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install django djangorestframework django-cors-headers channels channels-redis

# Run migrations and create sample data
python manage.py migrate
python manage.py create_sample_data

# Create admin user (optional)
python manage.py createsuperuser

# Start Django server
python manage.py runserver 8000
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/ (admin/admin123)

## API Endpoints

### Routes

- `GET /api/routes/` - List all routes
- `GET /api/routes/{id}/` - Get route details
- `GET /api/routes/{id}/buses/` - Get buses for a route
- `GET /api/routes/{id}/stops/` - Get stops for a route

### Buses

- `GET /api/buses/` - List all buses
- `GET /api/buses/{id}/` - Get bus details
- `GET /api/buses/{id}/locations/` - Get bus location history
- `POST /api/buses/{id}/update_location/` - Update bus location
- `GET /api/buses/tracking/` - Get real-time tracking data

### Locations

- `GET /api/locations/` - List all locations
- `GET /api/locations/latest/` - Get latest location for each bus

## WebSocket Connections

### Bus Tracking

```javascript
// Connect to all buses
ws://localhost:8000/ws/buses/

// Connect to specific route
ws://localhost:8000/ws/route/{route_id}/
```

## Sample Data

The system comes with pre-configured sample data:

### Routes

1. **Route 101 - Downtown Loop** (Orange #FF6B35)

   - Central Station → City Hall → Museum District → Shopping Center → Park Avenue

2. **Route 202 - University Express** (Blue #004E89)

   - University Gate → Student Center → Library → Sports Complex

3. **Route 303 - Airport Shuttle** (Green #009639)
   - Direct airport service

### Buses

- **B101A & B101B**: Downtown Loop
- **B202A**: University Express
- **B303A**: Airport Shuttle

## Simulating Real-time Movement

To simulate bus movements for demonstration:

```bash
# Install requests if not already installed
pip install requests

# Run the simulation script
python simulate_bus_movement.py
```

This script will:

- Update bus locations every 10 seconds
- Simulate realistic movement patterns
- Generate random speeds and headings
- Show live updates on the map

## Development

### Project Structure

```
bus-tracking/
├── bus_tracking_backend/     # Django project settings
├── buses/                    # Main Django app
│   ├── models.py            # Bus, Route, Location models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── consumers.py         # WebSocket consumers
│   └── management/commands/  # Custom management commands
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API and WebSocket services
│   │   └── App.jsx          # Main app component
│   └── package.json
├── manage.py                # Django management script
└── simulate_bus_movement.py  # Demo script
```

### Key Components

#### Backend Models

- **Route**: Bus routes with stops and styling
- **Bus**: Individual bus vehicles
- **BusLocation**: GPS coordinates with timestamps
- **RouteStop**: Stops along routes

#### Frontend Components

- **BusMap**: Interactive map with real-time markers
- **BusList**: Sidebar with bus details and status
- **RouteSelector**: Route filtering dropdown

## Customization

### Adding New Routes

1. Use Django admin at `/admin/`
2. Create Route with number, name, and color
3. Add RouteStop entries with coordinates
4. Assign buses to the route

### Map Configuration

Edit `frontend/src/components/BusMap.jsx`:

- Change default center coordinates
- Modify zoom levels
- Customize bus icons
- Add additional map layers

### Styling

Edit `frontend/src/App.css`:

- Modify color schemes
- Adjust responsive breakpoints
- Customize component layouts

## Production Deployment

### Backend (Django)

1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up Redis for WebSocket channel layer
4. Use production ASGI server (uvicorn/daphne)
5. Configure CORS settings for your domain

### Frontend (React)

1. Build production assets: `npm run build`
2. Serve static files with nginx or Apache
3. Update API base URL in `services/api.js`

### Environment Variables

```bash
# .env file
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://...
REDIS_URL=redis://...
ALLOWED_HOSTS=your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**

   - Check if Django server is running
   - Verify WebSocket URL in frontend
   - Ensure CORS settings allow WebSocket connections

2. **Map Not Loading**

   - Check internet connection (OpenStreetMap tiles)
   - Verify Leaflet CSS is imported
   - Check browser console for JavaScript errors

3. **API Errors**
   - Verify Django server is running on port 8000
   - Check CORS configuration
   - Ensure database migrations are applied

### Debug Mode

Enable debug logging in Django settings:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'buses': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Screenshots

The application provides:

- **Live Bus Tracking**: Real-time bus positions on interactive map
- **Route Visualization**: Color-coded routes with stops
- **Bus Information**: Detailed bus status and location data
- **Responsive Design**: Works on desktop, tablet, and mobile devices

---

**Demo Credentials:**

- Admin: `admin` / `admin123`
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
