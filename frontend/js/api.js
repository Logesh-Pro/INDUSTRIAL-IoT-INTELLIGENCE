const API_BASE = "http://127.0.0.1:5000/api";

async function apiRequest(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`);

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
    }

    return await response.json();
}

async function getHealth() {
    return apiRequest("/health");
}

async function getDatabaseHealth() {
    return apiRequest("/health/database");
}

async function getSystem() {
    return apiRequest("/system");
}

async function getLatestTelemetry() {
    return apiRequest("/latest");
}

async function getSummary() {
    return apiRequest("/summary");
}

async function getDevices() {
    return apiRequest("/devices");
}

async function getDevice(deviceId) {
    return apiRequest(`/devices/${encodeURIComponent(deviceId)}`);
}

async function getHistory(hours = 24) {
    return apiRequest(`/history?hours=${hours}`);
}

async function getAlarms(hours = 24) {
    return apiRequest(`/alarms?hours=${hours}`);
}

async function getActiveAlarms() {
    return apiRequest("/alarms/active");
}

async function getDeviceEvents(hours = 24) {
    return apiRequest(`/device-events?hours=${hours}`);
}

async function getTrends(hours = 24) {
    return apiRequest(`/trends?hours=${hours}`);
}
