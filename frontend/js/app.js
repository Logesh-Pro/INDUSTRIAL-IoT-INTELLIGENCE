"use strict";

const state = {
    historyHours: 1,
    telemetryChart: null,
    monitorChart: null,
    temperatureChart: null,
    humidityChart: null,
    occupancyChart: null,
    latest: null
};

function $(id) {
    return document.getElementById(id);
}

function safeNumber(value, fallback = 0) {
    const n = Number(value);
    return Number.isFinite(n) ? n : fallback;
}

function formatTime(value) {
    if (!value) return "--";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "--";
    return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });
}

function formatDate(value) {
    if (!value) return "--";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "--";
    return date.toLocaleDateString();
}

function formatUptime(seconds) {
    seconds = Math.max(0, Number(seconds) || 0);

    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    if (days > 0) return `${days}d ${hours}h`;
    if (hours > 0) return `${hours}h ${minutes}m`;
    return `${minutes}m`;
}

function updateClock() {
    const now = new Date();

    $("clock-time").textContent =
        now.toLocaleTimeString([], {
            hour12: false
        });

    $("clock-date").textContent =
        now.toLocaleDateString([], {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }).toUpperCase();
}

setInterval(updateClock, 1000);
updateClock();


function showSection(name) {
    document.querySelectorAll(".dashboard-section").forEach(section => {
        section.classList.remove("active");
    });

    const target = $(`section-${name}`);

    if (target) {
        target.classList.add("active");
    }

    document.querySelectorAll(".nav-item").forEach(item => {
        item.classList.toggle(
            "active",
            item.dataset.section === name
        );
    });

    if (name === "devices") loadDevices();
    if (name === "alarms") loadAlarms();
    if (name === "trends") loadTrends(state.historyHours);
    if (name === "system") loadSystem();
}

window.showSection = showSection;


document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
        showSection(item.dataset.section);
    });
});


async function loadHealth() {
    try {
        const health = await getHealth();

        $("system-status").textContent =
            health.status === "healthy"
                ? "SYSTEM ONLINE"
                : "SYSTEM DEGRADED";

        $("api-status").textContent =
            String(health.status || "UNKNOWN").toUpperCase();

        if (health.status !== "healthy") {
            $("api-status").style.color = "var(--danger)";
        }

    } catch (error) {
        console.error("Health:", error);
        $("system-status").textContent = "API OFFLINE";
        $("api-status").textContent = "OFFLINE";
        $("api-status").style.color = "var(--danger)";
    }
}


async function loadDatabaseHealth() {
    try {
        const db = await getDatabaseHealth();

        const connected =
            db.status === "connected" ||
            db.status === "healthy";

        $("db-status").textContent =
            connected ? "CONNECTED" : "DISCONNECTED";

        $("database-badge").textContent = connected ? "CONNECTED" : "DATABASE DEGRADED";

        if (!connected) {
            $("db-status").style.color = "var(--danger)";
            $("database-badge").style.color = "var(--danger)";
        }

    } catch (error) {
        console.error("Database:", error);
        $("db-status").textContent = "DISCONNECTED";
        $("database-badge").textContent = "DATABASE DEGRADED";
    }
}


async function loadLatest() {
    try {
        const data = await getLatestTelemetry();

        const latest =
            data.data ||
            data;

        state.latest = latest;

        const temperature =
            safeNumber(latest.temperature);

        const humidity =
            safeNumber(latest.humidity);

        const people =
            Math.round(safeNumber(latest.people));

        $("kpi-temperature").textContent =
            temperature.toFixed(1);

        $("kpi-humidity").textContent =
            humidity.toFixed(1);

        $("kpi-people").textContent =
            people;

        $("state-temp").textContent =
            `${temperature.toFixed(1)} °C`;

        $("state-humidity").textContent =
            `${humidity.toFixed(1)} %`;

        $("state-people").textContent =
            people;

        $("monitor-temp").textContent =
            `${temperature.toFixed(1)} °C`;

        $("monitor-humidity").textContent =
            `${humidity.toFixed(1)} %`;

        $("monitor-people").textContent =
            people;

        $("temp-meter").style.width =
            `${Math.min(100, Math.max(0, temperature / 40 * 100))}%`;

        $("humidity-meter").style.width =
            `${Math.min(100, Math.max(0, humidity))}%`;

        $("people-meter").style.width =
            `${Math.min(100, Math.max(0, people / 10 * 100))}%`;

        $("temperature-state").textContent =
            temperature >= 32 ? "CRITICAL" : "NORMAL";

        $("temperature-state").className =
            temperature >= 32 ? "bad" : "good";

        $("humidity-state").textContent =
            humidity >= 80 ? "HIGH" : "NORMAL";

        $("humidity-state").className =
            humidity >= 80 ? "warning" : "good";

        $("occupancy-state").textContent =
            people >= 7 ? "HIGH LOAD" : "MONITORING";

        $("occupancy-state").className =
            people >= 7 ? "warning" : "good";

        if (latest.timestamp) {
            $("state-last-seen").textContent =
                formatTime(latest.timestamp);
        }

        $("last-update").textContent =
            new Date().toLocaleTimeString();

    } catch (error) {
        console.error("Latest telemetry:", error);
    }
}


async function loadSummary() {
    try {
        const data = await getSummary();

        const summary =
            data.data ||
            data;

        const total =
            safeNumber(summary.total_devices);

        const online =
            safeNumber(summary.online_devices);

        const offline =
            safeNumber(summary.offline_devices);

        const people =
            safeNumber(summary.total_people);

        $("kpi-devices").textContent = total;
        $("kpi-devices-detail").textContent =
            `${online} online`;

        $("device-total").textContent = total;
        $("device-online").textContent = online;
        $("device-offline").textContent = offline;

        if (
            state.latest === null &&
            people > 0
        ) {
            $("kpi-people").textContent = people;
        }

    } catch (error) {
        console.error("Summary:", error);
    }
}


async function loadDevices() {
    try {
        const response = await getDevices();

        const devices =
            Array.isArray(response)
                ? response
                : response.devices ||
                  response.data ||
                  [];

        $("device-total").textContent = devices.length;

        const online = devices.filter(
            d => d.status === "online" || d.online === 1
        ).length;

        $("device-online").textContent = online;
        $("device-offline").textContent =
            Math.max(0, devices.length - online);

        const tbody = $("device-table");

        if (!devices.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="table-loading">
                        No devices found
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = devices.map(device => {
            const online =
                device.status === "online" ||
                device.online === 1;

            return `
                <tr>
                    <td><strong>${escapeHtml(device.device_id || "--")}</strong></td>
                    <td>${escapeHtml(device.site || "site01")} / ${escapeHtml(device.zone || "zone01")}</td>
                    <td>
                        <span class="status-pill ${online ? "online" : "offline"}">
                            ${online ? "ONLINE" : "OFFLINE"}
                        </span>
                    </td>
                    <td>${safeNumber(device.temperature).toFixed(1)} °C</td>
                    <td>${safeNumber(device.humidity).toFixed(1)} %</td>
                    <td>${Math.round(safeNumber(device.people))}</td>
                    <td>${formatTime(device.last_seen)}</td>
                </tr>
            `;
        }).join("");

        if (devices[0]) {
            const d = devices[0];
            const online =
                d.status === "online" ||
                d.online === 1;

            $("device-badge").textContent =
                online ? "ONLINE" : "OFFLINE";

            $("device-badge").style.color =
                online ? "var(--good)" : "var(--danger)";

            $("device-badge").style.borderColor =
                online
                    ? "rgba(53,212,154,.35)"
                    : "rgba(255,93,103,.35)";

            $("state-last-seen").textContent =
                formatTime(d.last_seen);
        }

    } catch (error) {
        console.error("Devices:", error);
    }
}


async function loadActiveAlarms() {
    try {
        const data = await getActiveAlarms();

        const alarms =
            data.alarms ||
            data.data?.alarms ||
            [];

        const count = alarms.length;

        $("kpi-alarms").textContent = count;
        $("nav-alarm-count").textContent = count;

        const alarmState = $("alarm-state");
        const preview = $("alarm-preview");
        const banner = $("alarm-banner");

        if (count === 0) {
            alarmState.textContent = "SYSTEM CLEAR";
            alarmState.className = "good";

            preview.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">✓</div>
                    <strong>NO ACTIVE ALARMS</strong>
                    <span>All monitored conditions are within configured limits.</span>
                </div>
            `;

            banner.className = "alarm-status-banner";
            banner.innerHTML = `
                <div class="banner-icon">✓</div>
                <div>
                    <strong>SYSTEM CLEAR</strong>
                    <span>No active safety conditions detected</span>
                </div>
            `;

            return;
        }

        alarmState.textContent =
            `${count} ACTIVE`;

        alarmState.className = "bad";

        preview.innerHTML = alarms.slice(0, 4).map(alarm => `
            <div class="event-row">
                <div class="event-time">${formatTime(alarm.timestamp)}</div>
                <div class="event-main">
                    <strong>${escapeHtml(alarm.alarm_type || "ALARM")}</strong>
                    <small>${escapeHtml(alarm.message || "")}</small>
                </div>
                <div class="event-status bad">${escapeHtml(alarm.severity || "WARNING")}</div>
            </div>
        `).join("");

        banner.className = "alarm-status-banner danger";
        banner.innerHTML = `
            <div class="banner-icon">!</div>
            <div>
                <strong>${count} ACTIVE ALARM${count > 1 ? "S" : ""}</strong>
                <span>Immediate attention may be required.</span>
            </div>
        `;

    } catch (error) {
        console.error("Active alarms:", error);
    }
}


async function loadAlarms() {
    try {
        const data = await getAlarms(24);

        const alarms =
            Array.isArray(data)
                ? data
                : data.alarms ||
                  data.data ||
                  [];

        const tbody = $("alarm-table");

        if (!alarms.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="table-loading">
                        No alarm history available
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = alarms.slice(0, 100).map(alarm => `
            <tr>
                <td>${formatTime(alarm.timestamp)}</td>
                <td><strong>${escapeHtml(alarm.device_id || "--")}</strong></td>
                <td>${escapeHtml(alarm.alarm_type || "--")}</td>
                <td>
                    <span class="${alarm.severity === "CRITICAL" ? "bad" : "warning"}">
                        ${escapeHtml(alarm.severity || "--")}
                    </span>
                </td>
                <td>${escapeHtml(alarm.status || "--")}</td>
                <td>${alarm.value ?? "--"}</td>
                <td>${escapeHtml(alarm.message || "--")}</td>
            </tr>
        `).join("");

    } catch (error) {
        console.error("Alarm history:", error);
    }

    await loadDeviceEvents();
}


async function loadDeviceEvents() {
    try {
        const data = await getDeviceEvents(24);

        const events =
            Array.isArray(data)
                ? data
                : data.events ||
                  data.data ||
                  [];

        renderEvents(events);

        const tbody = $("event-table");

        if (!events.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="table-loading">
                        No device events available
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = events.slice(0, 100).map(event => `
            <tr>
                <td>${formatTime(event.timestamp)}</td>
                <td><strong>${escapeHtml(event.device_id || "--")}</strong></td>
                <td>DEVICE EVENT</td>
                <td>
                    <span class="${event.status === "online" ? "good" : "bad"}">
                        ${escapeHtml(String(event.status || "--").toUpperCase() === "ONLINE" ? "CONNECTED" : (String(event.status).toUpperCase() === "OFFLINE" ? "DISCONNECTED" : String(event.status).toUpperCase()))}
                    </span>
                </td>
                <td>${escapeHtml(event.value || "--")}</td>
            </tr>
        `).join("");

    } catch (error) {
        console.error("Device events:", error);
    }
}


function renderEvents(events) {
    const container = $("event-preview");

    if (!events.length) {
        container.innerHTML =
            `<div class="empty-state compact">No recent device events.</div>`;
        return;
    }

    container.innerHTML = events.slice(0, 6).map(event => `
        <div class="event-row">
            <div class="event-time">${formatTime(event.timestamp)}</div>
            <div class="event-main">
                <strong>${escapeHtml(event.device_id || "DEVICE")}</strong>
                <small>${escapeHtml(event.value || event.status || "Event received")}</small>
            </div>
            <div class="event-status">
                ${escapeHtml(String(event.status || "EVENT").toUpperCase() === "ONLINE" ? "CONNECTED" : (String(event.status).toUpperCase() === "OFFLINE" ? "DISCONNECTED" : String(event.status).toUpperCase()))}
            </div>
        </div>
    `).join("");
}


function chartOptions() {
    return {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 400
        },
        interaction: {
            mode: "index",
            intersect: false
        },
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            x: {
                grid: {
                    color: "rgba(60,90,100,.15)"
                },
                ticks: {
                    color: "#607982",
                    maxTicksLimit: 8,
                    font: {
                        size: 8
                    }
                }
            },
            y: {
                grid: {
                    color: "rgba(60,90,100,.15)"
                },
                ticks: {
                    color: "#607982",
                    font: {
                        size: 8
                    }
                }
            }
        }
    };
}


function makeChart(canvasId, datasets, extraScales = {}) {
    const canvas = $(canvasId);

    if (!canvas) return null;

    return new Chart(canvas, {
        type: "line",
        data: {
            labels: [],
            datasets
        },
        options: { ...chartOptions(), scales: { ...chartOptions().scales, ...extraScales } } });
}


function createCharts() {

    state.telemetryChart = makeChart(
        "telemetry-chart",
        [
            {
                label: "Temperature",
                data: [],
                borderColor: "#27d9c5",
                backgroundColor: "rgba(39,217,197,.06)",
                borderWidth: 1.7,
                pointRadius: 0,
                tension: .35,
                fill: true
            },
            {
                label: "Humidity",
                data: [],
                borderColor: "#42a5ff",
                borderWidth: 1.4,
                pointRadius: 0,
                tension: .35
            },
            {
                label: "Occupancy",
                data: [],
                borderColor: "#e6b84b",
                borderWidth: 1.4,
                pointRadius: 0,
                tension: .35,
                yAxisID: "yPeople" } ], { yPeople: { position: "right", grid: { drawOnChartArea: false }, ticks: { color: "#607982", font: { size: 8 } } } } );

    state.monitorChart = makeChart(
        "monitor-chart",
        [
            {
                label: "Temperature",
                data: [],
                borderColor: "#27d9c5",
                borderWidth: 1.7,
                pointRadius: 0,
                tension: .35
            },
            {
                label: "Humidity",
                data: [],
                borderColor: "#42a5ff",
                borderWidth: 1.4,
                pointRadius: 0,
                tension: .35
            }
        ]
    );

    state.temperatureChart = makeChart(
        "temperature-chart",
        [{
            label: "Temperature",
            data: [],
            borderColor: "#27d9c5",
            borderWidth: 1.7,
            pointRadius: 0,
            tension: .35
        }]
    );

    state.humidityChart = makeChart(
        "humidity-chart",
        [{
            label: "Humidity",
            data: [],
            borderColor: "#42a5ff",
            borderWidth: 1.7,
            pointRadius: 0,
            tension: .35
        }]
    );

    state.occupancyChart = makeChart(
        "occupancy-chart",
        [{
            label: "Occupancy",
            data: [],
            borderColor: "#e6b84b",
            borderWidth: 1.7,
            pointRadius: 0,
            tension: .35
        }]
    );
}


function normalizeHistory(response) {
    const records =
        Array.isArray(response)
            ? response
            : response.data ||
              response.history ||
              [];

    const grouped = {};

    records.forEach(record => {
        const timestamp =
            record.timestamp ||
            record._time;

        const field =
            record.field ||
            record._field;

        const value =
            record.value ??
            record._value;

        if (!timestamp || !field) return;

        const key = timestamp;

        if (!grouped[key]) {
            grouped[key] = {
                timestamp,
                temperature: null,
                humidity: null,
                people: null
            };
        }

        if (field === "temperature") {
            grouped[key].temperature = safeNumber(value);
        }

        if (field === "humidity") {
            grouped[key].humidity = safeNumber(value);
        }

        if (field === "people") {
            grouped[key].people = safeNumber(value);
        }
    });

    return Object.values(grouped)
        .sort(
            (a, b) =>
                new Date(a.timestamp) -
                new Date(b.timestamp)
        );
}


async function loadTrends(hours = 1) {
    state.historyHours = hours;

    try {
        const response = await getHistory(hours);
        const records = normalizeHistory(response);

        const labels = records.map(
            r => formatTime(r.timestamp)
        );

        const temperature = records.map(
            r => r.temperature
        );

        const humidity = records.map(
            r => r.humidity
        );

        const people = records.map(
            r => r.people
        );

        updateChart(
            state.telemetryChart,
            labels,
            [temperature, humidity, people]
        );

        updateChart(
            state.monitorChart,
            labels,
            [temperature, humidity]
        );

        updateChart(
            state.temperatureChart,
            labels,
            [temperature]
        );

        updateChart(
            state.humidityChart,
            labels,
            [humidity]
        );

        updateChart(
            state.occupancyChart,
            labels,
            [people]
        );

    } catch (error) {
        console.error("Trends:", error);
    }
}


function updateChart(chart, labels, datasets) {
    if (!chart) return;

    chart.data.labels = labels;

    datasets.forEach((data, index) => {
        if (chart.data.datasets[index]) {
            chart.data.datasets[index].data = data;
        }
    });

    chart.update("none");
}


document.querySelectorAll(".range-btn[data-hours]").forEach(button => {
    button.addEventListener("click", () => {

        document
            .querySelectorAll(".range-btn[data-hours]")
            .forEach(btn => btn.classList.remove("active"));

        button.classList.add("active");

        const hours =
            Number(button.dataset.hours);

        loadTrends(hours);
    });
});


document.querySelectorAll(".trend-range").forEach(button => {
    button.addEventListener("click", () => {

        document
            .querySelectorAll(".trend-range")
            .forEach(btn => btn.classList.remove("active"));

        button.classList.add("active");

        loadTrends(
            Number(button.dataset.hours)
        );
    });
});


async function loadSystem() {
    try {
        const data = await getSystem();

        $("sys-status").textContent =
            String(data.status || "--").toUpperCase();

        $("sys-env").textContent =
            String(data.environment || "--").toUpperCase();

        $("environment").textContent =
            String(data.environment || "UNKNOWN").toUpperCase();

        $("sys-python").textContent =
            data.python_version || "--";

        $("sys-cpu").textContent =
            `${safeNumber(data.cpu_usage_percent).toFixed(1)} %`;

        $("sys-memory").textContent =
            `${safeNumber(data.memory_usage_percent).toFixed(1)} %`;

        $("sys-pid").textContent =
            data.process_id || "--";

        $("sys-uptime").textContent =
            formatUptime(data.uptime_seconds);

    } catch (error) {
        console.error("System:", error);
    }
}


async function refreshAll() {
    await Promise.all([
        loadHealth(),
        loadDatabaseHealth(),
        loadLatest(),
        loadSummary(),
        loadDevices(),
        loadActiveAlarms()
    ]);

    await loadTrends(state.historyHours);
}


function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


async function initializeDashboard() {
    console.log("Industrial IoT Operations Center initializing...");

    createCharts();

    await refreshAll();

    await loadDeviceEvents();

    console.log("Industrial IoT Operations Center ONLINE");

    setInterval(async () => {
        await Promise.all([
            loadLatest(),
            loadSummary(),
            loadDevices(),
            loadActiveAlarms()
        ]);
    }, 3500);

    setInterval(async () => {
        await loadHealth();
        await loadDatabaseHealth();
    }, 5000);

    setInterval(async () => {
        await loadTrends(state.historyHours);
    }, 10000);
}


document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);

window.refreshAll = refreshAll;
