import { useState, useEffect } from "react";
import webSocketService from "../services/websocket";

function BusList({ buses = [], selectedRoute }) {
  const [realTimeBuses, setRealTimeBuses] = useState(buses);
  const [expandedBus, setExpandedBus] = useState(null);

  useEffect(() => {
    setRealTimeBuses(buses);
  }, [buses]);

  useEffect(() => {
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
      } else if (data.type === "buses_update" || data.type === "initial_data") {
        setRealTimeBuses(data.buses);
      }
    };

    webSocketService.on("location_update", handleLocationUpdate);
    webSocketService.on("buses_update", handleLocationUpdate);
    webSocketService.on("initial_data", handleLocationUpdate);

    return () => {
      webSocketService.off("location_update", handleLocationUpdate);
      webSocketService.off("buses_update", handleLocationUpdate);
      webSocketService.off("initial_data", handleLocationUpdate);
    };
  }, []);

  const formatLastUpdate = (timestamp) => {
    if (!timestamp) return "No data";

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

  const getStatusColor = (timestamp) => {
    if (!timestamp) return "#gray";

    const date = new Date(timestamp);
    const now = new Date();
    const diffMins = Math.floor((now - date) / 60000);

    if (diffMins < 5) return "#4CAF50"; // Green - Recent
    if (diffMins < 15) return "#FF9800"; // Orange - Moderate
    return "#F44336"; // Red - Old
  };

  const toggleBusExpanded = (busId) => {
    setExpandedBus(expandedBus === busId ? null : busId);
  };

  const filteredBuses = selectedRoute
    ? realTimeBuses.filter((bus) => bus.route?.id === selectedRoute)
    : realTimeBuses;

  return (
    <div className="bus-list">
      <div className="bus-list-header">
        <h3>🚌 Active Buses</h3>
        <span className="bus-count">{filteredBuses.length} buses</span>
      </div>

      {filteredBuses.length === 0 ? (
        <div className="no-buses">
          <p>No buses available</p>
          {selectedRoute && <p>Try selecting a different route</p>}
        </div>
      ) : (
        <div className="bus-items">
          {filteredBuses.map((bus) => {
            const isExpanded = expandedBus === bus.id;
            const statusColor = getStatusColor(bus.current_location?.timestamp);

            return (
              <div
                key={bus.id}
                className={`bus-item ${isExpanded ? "expanded" : ""}`}
              >
                <div
                  className="bus-item-header"
                  onClick={() => toggleBusExpanded(bus.id)}
                >
                  <div className="bus-info">
                    <div className="bus-number">
                      <span
                        className="status-dot"
                        style={{ backgroundColor: statusColor }}
                      ></span>
                      Bus {bus.bus_number}
                    </div>
                    <div className="route-info">
                      <span
                        className="route-color"
                        style={{
                          backgroundColor: bus.route?.color || "#0066cc",
                        }}
                      ></span>
                      {bus.route?.route_number}
                    </div>
                  </div>
                  <div className="bus-status">
                    <div className="speed">
                      {bus.current_location?.speed?.toFixed(1) || 0} km/h
                    </div>
                    <div className="last-update">
                      {formatLastUpdate(bus.current_location?.timestamp)}
                    </div>
                  </div>
                  <span
                    className={`expand-icon ${isExpanded ? "expanded" : ""}`}
                  >
                    ▼
                  </span>
                </div>

                {isExpanded && (
                  <div className="bus-item-details">
                    <div className="detail-row">
                      <span className="label">Route:</span>
                      <span className="value">
                        {bus.route?.name || "Unknown"}
                      </span>
                    </div>
                    <div className="detail-row">
                      <span className="label">License:</span>
                      <span className="value">{bus.license_plate}</span>
                    </div>
                    <div className="detail-row">
                      <span className="label">Driver:</span>
                      <span className="value">
                        {bus.driver_name || "Not assigned"}
                      </span>
                    </div>
                    <div className="detail-row">
                      <span className="label">Capacity:</span>
                      <span className="value">{bus.capacity} passengers</span>
                    </div>
                    {bus.current_location && (
                      <>
                        <div className="detail-row">
                          <span className="label">Location:</span>
                          <span className="value">
                            {parseFloat(bus.current_location.latitude).toFixed(
                              4
                            )}
                            ,{" "}
                            {parseFloat(bus.current_location.longitude).toFixed(
                              4
                            )}
                          </span>
                        </div>
                        {bus.current_location.heading && (
                          <div className="detail-row">
                            <span className="label">Heading:</span>
                            <span className="value">
                              {bus.current_location.heading.toFixed(0)}°
                            </span>
                          </div>
                        )}
                        {bus.current_location.accuracy && (
                          <div className="detail-row">
                            <span className="label">GPS Accuracy:</span>
                            <span className="value">
                              {bus.current_location.accuracy.toFixed(1)}m
                            </span>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      <div className="bus-list-footer">
        <div className="status-legend">
          <div className="legend-item">
            <span
              className="status-dot"
              style={{ backgroundColor: "#4CAF50" }}
            ></span>
            <span>Recent (&lt;5min)</span>
          </div>
          <div className="legend-item">
            <span
              className="status-dot"
              style={{ backgroundColor: "#FF9800" }}
            ></span>
            <span>Moderate (&lt;15min)</span>
          </div>
          <div className="legend-item">
            <span
              className="status-dot"
              style={{ backgroundColor: "#F44336" }}
            ></span>
            <span>Old (&gt;15min)</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BusList;
