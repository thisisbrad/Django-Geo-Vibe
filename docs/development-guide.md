# Development Guide

## Setting up the Development Environment

### Prerequisites

- Python 3.7+
- Node.js 14+
- pip (Python package manager)
- npm (Node package manager)

### Backend Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install Python dependencies
4. Run database migrations
5. Create sample data
6. Start the ASGI server

### Frontend Setup

1. Navigate to the frontend directory
2. Install npm dependencies
3. Start the development server

## Project Structure

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
├── docs/                     # Documentation
└── manage.py                # Django management script
```

## Adding New Features

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

## Testing

### Backend Testing

Run Django tests with:
```
python manage.py test
```

### Frontend Testing

Run React tests with:
```
npm test
```

## Deployment

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

```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://...
REDIS_URL=redis://...
ALLOWED_HOSTS=your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com
```