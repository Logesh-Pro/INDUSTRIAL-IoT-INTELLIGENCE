$ErrorActionPreference = "Stop"

$ProjectRoot = "C:\Users\admin\Desktop\iiot"
$MosquittoDir = "C:\Program Files\mosquitto"
$InfluxDir = "C:\Users\admin\Downloads\influxdb2-2.9.1-windows_amd64"

Write-Host ""
Write-Host "============================================================"
Write-Host "       INDUSTRIAL IoT - STARTING ALL SERVICES"
Write-Host "============================================================"
Write-Host ""

Set-Location $ProjectRoot

# ------------------------------------------------------------
# 1. MOSQUITTO MQTT BROKER
# ------------------------------------------------------------

Write-Host "[1/5] Starting Mosquitto MQTT Broker..."

$mosquittoRunning = Get-Process mosquitto -ErrorAction SilentlyContinue

if ($mosquittoRunning) {
    Write-Host "      Mosquitto is already running."
}
else {
    Start-Process powershell.exe -ArgumentList @(
        "-NoExit",
        "-Command",
        "Set-Location '$MosquittoDir'; .\mosquitto.exe -c .\iiot.conf -v"
    )

    Write-Host "      Mosquitto starting..."
}

Start-Sleep -Seconds 3

# Check MQTT port
$tcp = Get-NetTCPConnection -LocalPort 1883 -State Listen -ErrorAction SilentlyContinue

if ($tcp) {
    Write-Host "      MQTT Broker READY"
}
else {
    Write-Host "      WARNING: MQTT port 1883 not detected."
}

# ------------------------------------------------------------
# 2. INFLUXDB
# ------------------------------------------------------------

Write-Host ""
Write-Host "[2/5] Starting InfluxDB..."

$influxRunning = Get-Process influxd -ErrorAction SilentlyContinue

if ($influxRunning) {
    Write-Host "      InfluxDB is already running."
}
else {
    Start-Process powershell.exe -ArgumentList @(
        "-NoExit",
        "-Command",
        "Set-Location '$InfluxDir'; .\influxd.exe"
    )

    Write-Host "      InfluxDB starting..."
}

Write-Host "      Waiting for InfluxDB..."

$influxReady = $false

for ($i = 1; $i -le 30; $i++) {

    try {
        $response = Invoke-WebRequest `
            -Uri "http://127.0.0.1:8086/health" `
            -UseBasicParsing `
            -TimeoutSec 2 `
            -ErrorAction Stop

        if ($response.StatusCode -eq 200) {
            $influxReady = $true
            break
        }
    }
    catch {
        Start-Sleep -Seconds 1
    }
}

if ($influxReady) {
    Write-Host "      InfluxDB READY"
}
else {
    Write-Host "      WARNING: InfluxDB did not become ready."
}

# ------------------------------------------------------------
# 3. TELEMETRY PROCESSOR
# ------------------------------------------------------------

Write-Host ""
Write-Host "[3/5] Starting MQTT Telemetry Processor..."

$processorRunning = Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -match "python.exe" -and
        $_.CommandLine -match "backend.services.telemetry_processor"
    }

if ($processorRunning) {
    Write-Host "      Telemetry Processor is already running."
}
else {
    Start-Process powershell.exe -ArgumentList @(
        "-NoExit",
        "-Command",
        "Set-Location '$ProjectRoot'; python -m backend.services.telemetry_processor"
    )

    Write-Host "      Telemetry Processor starting..."
}

Start-Sleep -Seconds 4

# ------------------------------------------------------------
# 4. FLASK API
# ------------------------------------------------------------

Write-Host ""
Write-Host "[4/5] Starting Flask API..."

$apiRunning = Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -match "python.exe" -and
        $_.CommandLine -match "backend.api.app"
    }

if ($apiRunning) {
    Write-Host "      Flask API is already running."
}
else {
    Start-Process powershell.exe -ArgumentList @(
        "-NoExit",
        "-Command",
        "Set-Location '$ProjectRoot'; python -m backend.api.app"
    )

    Write-Host "      Flask API starting..."
}

Write-Host "      Waiting for Flask API..."

$apiReady = $false

for ($i = 1; $i -le 30; $i++) {

    try {
        $response = Invoke-WebRequest `
            -Uri "http://127.0.0.1:5000/api/health" `
            -UseBasicParsing `
            -TimeoutSec 2 `
            -ErrorAction Stop

        if ($response.StatusCode -eq 200) {
            $apiReady = $true
            break
        }
    }
    catch {
        Start-Sleep -Seconds 1
    }
}

if ($apiReady) {
    Write-Host "      Flask API READY"
}
else {
    Write-Host "      WARNING: Flask API did not become ready."
}

# ------------------------------------------------------------
# 5. DASHBOARD
# ------------------------------------------------------------

Write-Host ""
Write-Host "[5/5] Opening Industrial IoT Dashboard..."

Start-Sleep -Seconds 2

Start-Process "http://127.0.0.1:5000"

# ------------------------------------------------------------
# COMPLETE
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================================"
Write-Host "             INDUSTRIAL IoT SYSTEM READY"
Write-Host "============================================================"
Write-Host ""
Write-Host " MQTT Broker : 1883"
Write-Host " InfluxDB    : http://127.0.0.1:8086"
Write-Host " Flask API   : http://127.0.0.1:5000"
Write-Host " Dashboard   : http://127.0.0.1:5000"
Write-Host ""
Write-Host " ESP32_01 should now connect automatically."
Write-Host ""
Write-Host "============================================================"
Write-Host ""