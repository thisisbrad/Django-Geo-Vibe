# System Overview

## Core Components

The Django-Geo-Vide system follows a modern full-stack architecture with clear separation between frontend and backend components. The backend provides a RESTful API using Django REST Framework, while the frontend consumes this API and displays data through interactive components.

## Architecture Overview

The Django-Geo-Vide system follows a modern full-stack architecture with clear separation between frontend and backend components. The backend provides a RESTful API using Django REST Framework, while the frontend consumes this API and displays data through interactive components.

```mermaid
graph TB
subgraph "Frontend"
A[React App] --> B[BusMap]
A --> C[BusList]
A --> D[RouteSelector]
B --> E[Leaflet Map]
C --> F[WebSocket Updates]
D --> G[Route Filtering]
end
subgraph "Backend"
H[Django REST API] --> I[RouteViewSet]
H --> J[BusViewSet]
H --> K[BusLocationViewSet]
I --> L[Route Model]
J --> M[Bus Model]
K --> N[BusLocation Model]
O[WebSocket Consumers] --> P[BusTrackingConsumer]
O --> Q[RouteTrackingConsumer]
end
subgraph "Database"
L --> R[(SQLite)]
M --> R
N --> R
end
subgraph "Communication"
A --> |HTTP/REST| H
A --> |WebSocket| O
S[Simulation Script] --> |HTTP POST| H
end
T[Admin User] --> |Django Admin| H
U[Passenger] --> A
V[Operator] --> A
```

## Simulation and Testing

Deploying the Django-Geo-Vide system for production use requires several configuration changes to ensure security, performance, and reliability. The development configuration prioritizes ease of setup, but production deployment necessitates adjustments to critical settings.

Security settings must be updated by setting DEBUG = False and configuring proper ALLOWED_HOSTS to include the production domain. The current configuration allows all CORS origins, which should be restricted to specific domains in production. A strong SECRET_KEY should be used and stored securely, preferably through environment variables.

For WebSocket functionality, Redis should be used as the channel layer backend in production instead of the in-memory layer used in development.
