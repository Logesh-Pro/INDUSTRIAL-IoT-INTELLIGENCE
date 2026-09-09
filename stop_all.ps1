$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "============================================================"
Write-Host "INDUSTRIAL IoT - STOP PROJECT SERVICES"
Write-Host "============================================================"

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
        Stop-Process `
            -Id $_.ProcessId `
            -Force `
            -ErrorAction SilentlyContinue
    }

Write-Host ""
Write-Host "Project Python services stopped." -ForegroundColor Green
Write-Host ""
Write-Host "InfluxDB is intentionally left running."
Write-Host "Close influxd separately when you no longer need it."
