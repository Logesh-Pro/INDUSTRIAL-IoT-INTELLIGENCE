$ErrorActionPreference = "SilentlyContinue"

Write-Host ""
Write-Host "============================================================"
Write-Host "       INDUSTRIAL IoT - STOPPING ALL SERVICES"
Write-Host "============================================================"
Write-Host ""

Write-Host "[1/4] Stopping Telemetry Processor..."
Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -match "python.exe" -and
        $_.CommandLine -match "backend.services.telemetry_processor"
    } |
    ForEach-Object {
        Stop-Process -Id $_.ProcessId -Force
    }

Write-Host "[2/4] Stopping Flask API..."
Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -match "python.exe" -and
        $_.CommandLine -match "backend.api.app"
    } |
    ForEach-Object {
        Stop-Process -Id $_.ProcessId -Force
    }

Write-Host "[3/4] Stopping Mosquitto..."
Get-Process mosquitto -ErrorAction SilentlyContinue |
    Stop-Process -Force

Write-Host "[4/4] Stopping InfluxDB..."
Get-Process influxd -ErrorAction SilentlyContinue |
    Stop-Process -Force

Write-Host ""
Write-Host "============================================================"
Write-Host "             ALL IIoT SERVICES STOPPED"
Write-Host "============================================================"
Write-Host ""
