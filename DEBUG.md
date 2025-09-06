Django-Geo-Vide: Real-time Bus Tracking System
A real-time bus tracking application built with Django REST API backend and React frontend with interactive maps.
Table of Contents
Features
Technology Stack
Prerequisites
Setup Instructions

1. Backend Setup
2. Frontend Setup
   Running the Application
3. Start Backend Server
4. Start Frontend Server
5. Run Bus Movement Simulation
   Accessing the Application
   API Endpoints
   WebSocket Connections
   Admin Panel
   Troubleshooting
   Customization
   Production Deployment
   Features
   🚌 Real-time Bus Tracking: Track multiple buses on an interactive map
   🗺️ Interactive Maps: Powered by Leaflet and OpenStreetMap
   🛣️ Route Management: Manage bus routes with colored visualization
   📡 WebSocket Updates: Live location updates without page refresh
   🎨 Responsive Design: Works on desktop and mobile devices
   📊 Admin Panel: Django admin for managing buses, routes, and locations
   Technology Stack
   Backend
   Django 5.2: Web framework
   Django REST Framework: API development
   WebSockets (Channels): Real-time communication
   SQLite: Database (easily upgradeable to PostgreSQL)
   Redis: WebSocket channel layer (optional, falls back to in-memory)
   Uvicorn: ASGI server for WebSocket support
   Frontend
   React 18: UI framework
   Vite: Build tool and dev server
   Leaflet: Interactive maps
   React-Leaflet: React integration for Leaflet
   Axios: HTTP client
   Prerequisites
   Before you begin, ensure you have the following installed:
   Python 3.7 or higher
   Node.js and npm
   pip (Python package manager)
   Setup Instructions
6. Backend Setup
   Create and activate a virtual environment:
   bash
   cd /path/to/Django-Geo-Vide
   python3 -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   Install Python dependencies:
   bash
   pip install django djangorestframework django-cors-headers channels channels-redis uvicorn[standard] requests
   Run database migrations:
   bash
   python manage.py migrate
   Create sample data:
   bash
   python manage.py create_sample_data
   (Optional) Create admin user:
   bash
   python manage.py createsuperuser
7. Frontend Setup
   Navigate to frontend directory:
   bash
   cd frontend
   Install npm dependencies:
   bash
   npm install
   Running the Application
8. Start Backend Server
   In a new terminal window, start the backend server using Uvicorn (required for WebSocket support):
   bash
   cd /path/to/Django-Geo-Vide
   source venv/bin/activate
   uvicorn bus_tracking_backend.asgi:application --host 127.0.0.1 --port 8001
   Note: The application is configured to run on port 8001. If this port is in use, you can specify a different port:
   bash
   uvicorn bus_tracking_backend.asgi:application --host 127.0.0.1 --port YOUR_PORT_NUMBER
   You should see output similar to:
   INFO: Started server process [XXXXX]
   INFO: Waiting for application startup.
   INFO: Application startup complete.
   INFO: Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
9. Start Frontend Server
   In another terminal window, start the frontend development server:
   bash
   cd /path/to/Django-Geo-Vide/frontend
   npm run dev
   The frontend server will start and display the URL where the application is running:
   ➜ Local: http://localhost:5173/
   Note: If port 5173 is in use, Vite will automatically select another port (e.g., 5174). Make note of the actual port displayed in your terminal.
10. Run Bus Movement Simulation
    In a third terminal window, start the bus movement simulation:
    bash
    cd /path/to/Django-Geo-Vide
    source venv/bin/activate
    python simulate_bus_movement.py
    You should see output similar to:
    🚌 Starting Bus Movement Simulation...
    📍 Updating bus locations every 10 seconds
    ⏹️ Press Ctrl+C to stop
    Found 4 active buses
    ✅ Updated B101A - Lat: 52.361571, Lng: 4.877899, Speed: 21.8 km/h
    ✅ Updated B101B - Lat: 52.369217, Lng: 4.890106, Speed: 29.2 km/h
    ✅ Updated B202A - Lat: 52.360855, Lng: 4.886089, Speed: 42.9 km/h
    ✅ Updated B303A - Lat: 52.386356, Lng: 4.886604, Speed: 39.5 km/h
    ⏳ Waiting 10 seconds for next update...
    The simulation will continue running, updating bus locations every 10 seconds.
    Accessing the Application
    Once all services are running:
    Open your web browser
    Navigate to the frontend URL (typically http://localhost:5173 or http://localhost:5174)
    You should see the interactive map with bus markers
    As the simulation runs, you'll see buses moving in real-time on the map
    API Endpoints
    Routes
    GET /api/routes/ - List all routes
    GET /api/routes/{id}/ - Get route details
    GET /api/routes/{id}/buses/ - Get buses for a route
    GET /api/routes/{id}/stops/ - Get stops for a route
    Buses
    GET /api/buses/ - List all buses
    GET /api/buses/{id}/ - Get bus details
    GET /api/buses/{id}/locations/ - Get bus location history
    POST /api/buses/{id}/update_location/ - Update bus location
    GET /api/buses/tracking/ - Get real-time tracking data
    Locations
    GET /api/locations/ - List all locations
    GET /api/locations/latest/ - Get latest location for each bus
    WebSocket Connections
    Bus Tracking
    ws://localhost:8001/ws/buses/ - Connect to all buses
    ws://localhost:8001/ws/route/{route_id}/ - Connect to specific route
    The frontend automatically connects to the WebSocket endpoint to receive real-time updates.
    Admin Panel
    Access the Django admin panel at: http://127.0.0.1:8001/admin/Default Credentials:
    Username: admin
    Password: admin123
    In the admin panel, you can:
    Manage routes, buses, and locations
    Add new routes and buses
    Modify existing data
    View database records
    Troubleshooting
    Common Issues
    Port Conflicts
    If port 8001 is in use, change it in the Uvicorn command
    If port 5173 is in use, Vite will automatically use another port
    Update CORS settings in bus_tracking_backend/settings.py if using different ports
    WebSocket Connection Failed
    Ensure you're using Uvicorn, not the standard Django development server
    Check that the frontend and backend ports match the configuration
    Verify CORS settings in bus_tracking_backend/settings.py
    Map Not Loading
    Check internet connection (OpenStreetMap tiles require internet)
    Verify Leaflet CSS is imported
    Check browser console for JavaScript errors
    API Errors
    Verify backend server is running
    Check CORS configuration
    Ensure database migrations are applied
    Process Management
    To stop running services, use Ctrl+C in each terminal window. If processes are still running:
    bash

# Find processes running on specific ports

lsof -i :8001
lsof -i :5173

# Kill processes by PID

kill -9 PID_NUMBER
Customization
Adding New Routes
Use Django admin at /admin/
Create Route with number, name, and color
Add RouteStop entries with coordinates
Assign buses to the route
Map Configuration
Edit frontend/src/components/BusMap.jsx:
Change default center coordinates
Modify zoom levels
Customize bus icons
Add additional map layers
Styling
Edit frontend/src/App.css:
Modify color schemes
Adjust responsive breakpoints
Customize component layouts
Simulation Interval
To change how frequently buses update, edit simulate_bus_movement.py:
Modify the time.sleep(10) value in the main loop
Default is 10 seconds
Production Deployment
Backend (Django)
Set DEBUG = False in settings.py
Configure proper database (PostgreSQL recommended)
Set up Redis for WebSocket channel layer
Use production ASGI server (uvicorn/daphne)
Configure CORS settings for your domain
Frontend (React)
Build production assets: npm run build
Serve static files with nginx or Apache
Update API base URL in services/api.js
Environment Variables
Create a .env file:
bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://...
REDIS_URL=redis://...
ALLOWED_HOSTS=your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com
Demo Credentials:
Admin: admin / admin123
Frontend: http://localhost:5173 (or the port Vite assigns)
Backend: http://127.0.0.1:8001
Enjoy tracking buses in real-time! 🚌🗺
