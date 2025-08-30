import { useState } from "react";

function RouteSelector({ routes = [], selectedRoute, onRouteChange }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleRouteSelect = (routeId) => {
    onRouteChange(routeId);
    setIsOpen(false);
  };

  const selectedRouteData = routes.find((route) => route.id === selectedRoute);

  return (
    <div className="route-selector">
      <label htmlFor="route-select">Filter by Route:</label>
      <div className="dropdown">
        <button
          className="dropdown-toggle"
          onClick={() => setIsOpen(!isOpen)}
          type="button"
        >
          {selectedRouteData ? (
            <>
              <span
                className="route-color"
                style={{ backgroundColor: selectedRouteData.color }}
              ></span>
              Route {selectedRouteData.route_number} - {selectedRouteData.name}
            </>
          ) : (
            "All Routes"
          )}
          <span className={`arrow ${isOpen ? "up" : "down"}`}>▼</span>
        </button>

        {isOpen && (
          <div className="dropdown-menu">
            <button
              className={`dropdown-item ${!selectedRoute ? "active" : ""}`}
              onClick={() => handleRouteSelect(null)}
            >
              All Routes
            </button>
            {routes.map((route) => (
              <button
                key={route.id}
                className={`dropdown-item ${
                  selectedRoute === route.id ? "active" : ""
                }`}
                onClick={() => handleRouteSelect(route.id)}
              >
                <span
                  className="route-color"
                  style={{ backgroundColor: route.color }}
                ></span>
                Route {route.route_number} - {route.name}
                <span className="bus-count">({route.buses_count} buses)</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default RouteSelector;
