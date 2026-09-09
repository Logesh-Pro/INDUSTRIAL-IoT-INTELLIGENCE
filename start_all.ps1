$ErrorActionPreference = "Continue"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$InfluxExe = Join-Path $env:USERPROFILE "Downloads\influxdb2-2.9.1-windows_amd64\influxd.exe"

Write-Host "============================================================"
Write-Host "INDUSTRIAL IoT - START ALL SERVICES"
Write-Host "============================================================"

Set-Location $ProjectRoot

# ------------------------------------------------------------
# Stop old project processes to avoid duplicate instances
# ------------------------------------------------------------

Write-Host "`nCleaning previous project processes..."

Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -eq "python.exe" -and
        (
            $_.CommandLine -match "backend\.api\.app" -or
            $_.CommandLine -match "backend\.services\.telemetry_processor" -or
            $_.CommandLine -match "esp32_mqtt_simulator\.py"
        )
    } |
    ForEach-Object {
        Write-Host "Stopping PID $($_.ProcessId)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

Start-Sleep -Seconds 2


# ------------------------------------------------------------
# Start InfluxDB
# ------------------------------------------------------------

Write-Host "`nStarting InfluxDB..."

if (Test-Path $InfluxExe) {

    Start-Process `
        -FilePath $InfluxExe `
        -WorkingDirectory (Split-Path $InfluxExe) `
        -WindowStyle Normal

    Write-Host "InfluxDB starting..." -ForegroundColor Green

}
else {

    Write-Host "InfluxDB executable not found:"
    Write-Host $InfluxExe -ForegroundColor Red
}


# ------------------------------------------------------------
# Wait for InfluxDB
# ------------------------------------------------------------

Write-Host "Waiting for InfluxDB..."

$influxReady = $false

for ($i = 0; $i -lt 20; $i++) {

    try {

        $health = Invoke-RestMethod `
            "http://127.0.0.1:8086/health" `
            -TimeoutSec 2

        if ($health.status -eq "pass") {
            $influxReady = $true
            break
        }

    }
    catch {}

    Start-Sleep -Seconds 1
}

if ($influxReady) {
    Write-Host "InfluxDB: ONLINE" -ForegroundColor Green
}
else {
    Write-Host "InfluxDB did not become ready." -ForegroundColor Yellow
}


# ------------------------------------------------------------
# Start Flask API
# ------------------------------------------------------------

Write-Host "`nStarting Flask API..."

Start-Process `
    -FilePath "python" `
    -ArgumentList "-m backend.api.app" `
    -WorkingDirectory $ProjectRoot `
    -WindowStyle Normal

Write-Host "Flask API starting..." -ForegroundColor Green


# ------------------------------------------------------------
# Wait for API
# ------------------------------------------------------------

Write-Host "Waiting for Flask API..."

$apiReady = $false

for ($i = 0; $i -lt 20; $i++) {

    try {

        $health = Invoke-RestMethod `
            "http://127.0.0.1:5000/api/health" `
            -TimeoutSec 2

        if ($health.status -eq "healthy") {
            $apiReady = $true
            break
        }

    }
    catch {}

    Start-Sleep -Seconds 1
}

if ($apiReady) {
    Write-Host "Flask API: ONLINE" -ForegroundColor Green
}
else {
    Write-Host "Flask API did not become ready." -ForegroundColor Yellow
}


# ------------------------------------------------------------
# Start MQTT Processor
# ------------------------------------------------------------

Write-Host "`nStarting MQTT telemetry processor..."

Start-Process `
    -FilePath "python" `
    -ArgumentList "-m backend.services.telemetry_processor" `
    -WorkingDirectory $ProjectRoot `
    -WindowStyle Normal

Write-Host "MQTT Processor: STARTED" -ForegroundColor Green


# ------------------------------------------------------------
# Start ESP32 MQTT Simulator
# ------------------------------------------------------------

Start-Sleep -Seconds 3

Write-Host "`nStarting ESP32 MQTT simulator..."

Start-Process `
    -FilePath "python" `
    -ArgumentList "esp32_mqtt_simulator.py" `
    -WorkingDirectory $ProjectRoot `
    -WindowStyle Normal

Write-Host "ESP32 Simulator: STARTED" -ForegroundColor Green


# ------------------------------------------------------------
# Final startup information
# ------------------------------------------------------------

Start-Sleep -Seconds 5

Write-Host "`n============================================================"
Write-Host "INDUSTRIAL IoT SYSTEM STARTED"
Write-Host "============================================================"

Write-Host ""
Write-Host "Dashboard:"
Write-Host "http://127.0.0.1:5000/" -ForegroundColor Cyan

Write-Host ""
Write-Host "API:"
Write-Host "http://127.0.0.1:5000/api/health" -ForegroundColor Cyan

Write-Host ""
Write-Host "InfluxDB:"
Write-Host "http://127.0.0.1:8086" -ForegroundColor Cyan

Write-Host ""
Write-Host "MQTT:"
Write-Host "127.0.0.1:1883" -ForegroundColor Cyan

Write-Host ""
Write-Host "Telemetry:"
Write-Host "industrial/site01/zone01/telemetry"

Write-Host ""
Write-Host "System is ready."

# Open dashboard automatically
Start-Process "http://127.0.0.1:5000/"
