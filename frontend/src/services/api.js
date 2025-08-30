import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Routes API
export const fetchRoutes = async () => {
  try {
    const response = await api.get("/routes/");
    return response.data;
  } catch (error) {
    console.error("Error fetching routes:", error);
    throw error;
  }
};

export const fetchRoute = async (routeId) => {
  try {
    const response = await api.get(`/routes/${routeId}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching route:", error);
    throw error;
  }
};

export const fetchRouteStops = async (routeId) => {
  try {
    const response = await api.get(`/routes/${routeId}/stops/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching route stops:", error);
    throw error;
  }
};

// Buses API
export const fetchBuses = async (routeId = null) => {
  try {
    const url = routeId ? `/buses/?route=${routeId}` : "/buses/";
    const response = await api.get(url);
    return response.data;
  } catch (error) {
    console.error("Error fetching buses:", error);
    throw error;
  }
};

export const fetchBus = async (busId) => {
  try {
    const response = await api.get(`/buses/${busId}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching bus:", error);
    throw error;
  }
};

export const fetchBusLocations = async (busId, hours = 24) => {
  try {
    const response = await api.get(`/buses/${busId}/locations/?hours=${hours}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching bus locations:", error);
    throw error;
  }
};

export const updateBusLocation = async (busId, locationData) => {
  try {
    const response = await api.post(
      `/buses/${busId}/update_location/`,
      locationData
    );
    return response.data;
  } catch (error) {
    console.error("Error updating bus location:", error);
    throw error;
  }
};

// Bus Locations API
export const fetchAllBusLocations = async (hours = null) => {
  try {
    const url = hours ? `/locations/?hours=${hours}` : "/locations/";
    const response = await api.get(url);
    return response.data;
  } catch (error) {
    console.error("Error fetching bus locations:", error);
    throw error;
  }
};

export const fetchLatestLocations = async () => {
  try {
    const response = await api.get("/locations/latest/");
    return response.data;
  } catch (error) {
    console.error("Error fetching latest locations:", error);
    throw error;
  }
};

// Bus Tracking API
export const fetchBusTracking = async () => {
  try {
    const response = await api.get("/buses/tracking/");
    return response.data;
  } catch (error) {
    console.error("Error fetching bus tracking data:", error);
    throw error;
  }
};

export default api;
