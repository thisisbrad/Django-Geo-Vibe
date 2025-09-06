# Django-Geo-Vide: Real-time Bus Tracking System

A real-time bus tracking application built with Django REST API backend and React frontend with interactive maps. This system enables administrators and users to monitor bus locations, manage routes, and view real-time updates on an interactive map.

## 🚌 Features

- **Real-time Bus Tracking**: Track multiple buses on an interactive map with live updates
- **Interactive Maps**: Powered by Leaflet and OpenStreetMap with smooth animations
- **Route Management**: Manage bus routes with color-coded visualization
- **WebSocket Updates**: Live location updates without page refresh
- **Responsive Design**: Works on desktop and mobile devices
- **Admin Panel**: Django admin for managing buses, routes, and locations

## 🏗️ Architecture

The system follows a **client-server architecture** with a decoupled frontend (React/Vite) and backend (Django REST + WebSockets). It uses an **ASGI server** to support synchronous HTTP and asynchronous WebSocket connections.

### Technology Stack

#### Backend

- **Django 5.2**: Web framework
- **Django REST Framework**: API development
- **Django Channels**: WebSocket support
- **SQLite**: Database (easily upgradeable to PostgreSQL)
- **Uvicorn**: ASGI server for WebSocket support

#### Frontend

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Leaflet**: Interactive maps
- **React-Leaflet**: React integration for Leaflet
- **Axios**: HTTP client

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js 14+
- pip (Python package manager)
- npm (Node package manager)

### 1. Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd django-geo-vide

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install django djangorestframework django-cors-headers channels channels-redis uvicorn[standard]

# Run migrations
python manage.py migrate

# Create sample data
python manage.py create_sample_data

# Create admin user (optional)
python manage.py createsuperuser

# Start the ASGI server
uvicorn bus_tracking_backend.asgi:application --host 127.0.0.1 --port 8001
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

### 3. Start Simulation (for demo)

In a new terminal:

```bash
# Activate virtual environment
source venv/bin/activate

# Install requests library
pip install requests

# Run the simulation script
python simulate_bus_movement.py
```

## 🌐 Access the Application

- **Frontend**: http://localhost:5173 (or the port shown in terminal)
- **Backend API**: http://localhost:8001/api/
- **Admin Panel**: http://localhost:8001/admin/ (admin/admin123)

## 🛠️ API Endpoints

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

## 🔌 WebSocket Connections

### Bus Tracking

```javascript
// Connect to all buses
ws://localhost:8001/ws/buses/

// Connect to specific route
ws://localhost:8001/ws/route/{route_id}/
```

## 🗺️ Sample Data

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

## 📁 Project Structure

```
django-geo-vide/
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
├── manage.py                # Django management script
└── simulate_bus_movement.py  # Demo script
```

## ⚙️ Customization

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

## 🏭 Production Deployment

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

## 🐛 Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**

   - Check if Django server is running with ASGI (uvicorn)
   - Verify WebSocket URL in frontend matches backend
   - Ensure CORS settings allow WebSocket connections

2. **Map Not Loading**

   - Check internet connection (OpenStreetMap tiles)
   - Verify Leaflet CSS is imported
   - Check browser console for JavaScript errors

3. **API Errors**
   - Verify Django server is running on correct port
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

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📸 Screenshots

The application provides:

- **Live Bus Tracking**: Real-time bus positions on interactive map
- **Route Visualization**: Color-coded routes with stops
- **Bus Information**: Detailed bus status and location data
- **Responsive Design**: Works on desktop, tablet, and mobile devices

---

**Demo Credentials:**

- Admin: `admin` / `admin123`
- Frontend: http://localhost:5173
- Backend: http://localhost:8001
