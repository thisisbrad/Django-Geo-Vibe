import { useEffect, useRef, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import webSocketService from "../services/websocket";

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

// Custom bus icon
const createBusIcon = (color = "#0066cc", isSelected = false) => {
  return L.divIcon({
    html: `
      <div style="
        background-color: ${color};
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 3px solid ${isSelected ? "#ffff00" : "#ffffff"};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        color: white;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      ">
        🚌
      </div>
    `,
    className: "custom-bus-icon",
    iconSize: [26, 26],
    iconAnchor: [13, 13],
    popupAnchor: [0, -13],
  });
};

// Component to update map view when data changes
function MapUpdater({ buses, selectedRoute }) {
  const map = useMap();

  useEffect(() => {
    if (buses.length > 0) {
      const group = new L.FeatureGroup();

      buses.forEach((bus) => {
        if (bus.current_location) {
          const marker = L.marker([
            parseFloat(bus.current_location.latitude),
            parseFloat(bus.current_location.longitude),
          ]);
          group.addLayer(marker);
        }
      });

      if (group.getLayers().length > 0) {
        map.fitBounds(group.getBounds(), { padding: [20, 20] });
      }
    }
  }, [buses, selectedRoute, map]);

  return null;
}

function BusMap({ buses = [], routes = [], selectedRoute }) {
  const [realTimeBuses, setRealTimeBuses] = useState(buses);
  const [selectedBus, setSelectedBus] = useState(null);
  const mapRef = useRef();

  useEffect(() => {
    setRealTimeBuses(buses);
  }, [buses]);

  useEffect(() => {
    // Connect to WebSocket for real-time updates
    webSocketService.connect();

    const handleLocationUpdate = (data) => {
      if (data.type === "location_update") {
        setRealTimeBuses((prevBuses) =>
          prevBuses.map((bus) => {
            if (bus.id === data.bus_id) {
              return {
                ...bus,
                current_location: data.location,
              };
            }
            return bus;
          })
        );
      } else if (data.type === "buses_update") {
        setRealTimeBuses(data.buses);
      } else if (data.type === "initial_data") {
        setRealTimeBuses(data.buses);
      }
    };

    webSocketService.on("location_update", handleLocationUpdate);
    webSocketService.on("buses_update", handleLocationUpdate);
    webSocketService.on("initial_data", handleLocationUpdate);

    // Request initial data
    setTimeout(() => {
      if (webSocketService.isConnected()) {
        webSocketService.requestBusData();
      }
    }, 1000);

    return () => {
      webSocketService.off("location_update", handleLocationUpdate);
      webSocketService.off("buses_update", handleLocationUpdate);
      webSocketService.off("initial_data", handleLocationUpdate);
    };
  }, []);

  const handleBusClick = (bus) => {
    setSelectedBus(bus.id === selectedBus ? null : bus.id);
  };

  const formatLastUpdate = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d ago`;
  };

  // Default center (NYC coordinates as fallback)
  const defaultCenter = [40.7589, -73.9851];
  const defaultZoom = 12;

  return (
    <div className="bus-map">
      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        style={{ height: "100%", width: "100%" }}
        ref={mapRef}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        <MapUpdater buses={realTimeBuses} selectedRoute={selectedRoute} />

        {realTimeBuses.map((bus) => {
          if (!bus.current_location) return null;

          const position = [
            parseFloat(bus.current_location.latitude),
            parseFloat(bus.current_location.longitude),
          ];

          const routeColor = bus.route?.color || "#0066cc";
          const isSelected = selectedBus === bus.id;

          return (
            <Marker
              key={bus.id}
              position={position}
              icon={createBusIcon(routeColor, isSelected)}
              eventHandlers={{
                click: () => handleBusClick(bus),
              }}
            >
              <Popup>
                <div className="bus-popup">
                  <h3>🚌 Bus {bus.bus_number}</h3>
                  <p>
                    <strong>Route:</strong> {bus.route?.route_number} -{" "}
                    {bus.route?.name}
                  </p>
                  <p>
                    <strong>Speed:</strong>{" "}
                    {bus.current_location.speed?.toFixed(1) || 0} km/h
                  </p>
                  <p>
                    <strong>Last Update:</strong>{" "}
                    {formatLastUpdate(bus.current_location.timestamp)}
                  </p>
                  {bus.current_location.heading && (
                    <p>
                      <strong>Heading:</strong>{" "}
                      {bus.current_location.heading.toFixed(0)}°
                    </p>
                  )}
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>

      <div className="map-legend">
        <h4>Legend</h4>
        <div className="legend-item">
          <div
            className="legend-color"
            style={{ backgroundColor: "#0066cc" }}
          ></div>
          <span>Bus Location</span>
        </div>
        <p className="legend-note">Click on a bus for details</p>
      </div>

      <div className="map-status">
        <span
          className={`status-indicator ${
            webSocketService.isConnected() ? "connected" : "disconnected"
          }`}
        >
          {webSocketService.isConnected() ? "🟢 Live" : "🔴 Offline"}
        </span>
        <span className="bus-count">{realTimeBuses.length} buses tracked</span>
      </div>
    </div>
  );
}

export default BusMap;
