import { useState, useEffect } from "react";
import BusMap from "./components/BusMap";
import RouteSelector from "./components/RouteSelector";
import BusList from "./components/BusList";
import { fetchRoutes, fetchBuses } from "./services/api";
import "./App.css";
import "leaflet/dist/leaflet.css";

function App() {
  const [routes, setRoutes] = useState([]);
  const [buses, setBuses] = useState([]);
  const [selectedRoute, setSelectedRoute] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [routesData, busesData] = await Promise.all([
        fetchRoutes(),
        fetchBuses(),
      ]);
      setRoutes(routesData);
      setBuses(busesData);
    } catch (err) {
      setError("Failed to load data: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRouteChange = async (routeId) => {
    setSelectedRoute(routeId);
    if (routeId) {
      try {
        const routeBuses = await fetchBuses(routeId);
        setBuses(routeBuses);
      } catch (err) {
        setError("Failed to load route buses: " + err.message);
      }
    } else {
      const allBuses = await fetchBuses();
      setBuses(allBuses);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <h2>Loading Bus Tracking System...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error: {error}</h2>
        <button onClick={loadInitialData}>Retry</button>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚌 Bus Tracking System</h1>
        <RouteSelector
          routes={routes}
          selectedRoute={selectedRoute}
          onRouteChange={handleRouteChange}
        />
      </header>

      <main className="app-main">
        <div className="map-container">
          <BusMap buses={buses} routes={routes} selectedRoute={selectedRoute} />
        </div>

        <div className="sidebar">
          <BusList buses={buses} selectedRoute={selectedRoute} />
        </div>
      </main>
    </div>
  );
}

export default App;
