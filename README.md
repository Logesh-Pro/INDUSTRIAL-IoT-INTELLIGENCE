# Industrial IoT People Monitoring & Environmental Analytics

An ESP32-based Industrial IoT monitoring system that combines **people counting, temperature and humidity monitoring, Wi-Fi communication, data logging, and a real-time analytics dashboard**.

The system uses two IR sensors to determine whether people are entering or leaving an area, a DHT sensor for environmental measurements, and an ESP32 as the main controller.

Sensor data is transmitted over Wi-Fi and stored in an Excel file while a Flask-based web dashboard displays live readings, historical graphs, statistics, and automatic environmental analysis.

---

## Project Overview

The system is designed to monitor an industrial or indoor environment in real time.

It currently provides:

- 👥 People counting
- 🌡️ Temperature monitoring
- 💧 Humidity monitoring
- 📊 Real-time graphs
- 📈 Historical data analysis
- 🧠 Automatic environmental analysis
- 📁 Excel data logging
- 🌐 Wi-Fi communication
- 🖥️ Web-based monitoring dashboard

The project is designed in a modular way so additional hardware such as a relay-controlled fan, LEDs, and a buzzer can be integrated later.

---

## System Architecture

```text
                ┌─────────────────────┐
                │       ESP32         │
                │   Main Controller   │
                └──────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌───────────┐    ┌───────────┐    ┌───────────┐
    │ IR Sensor │    │ IR Sensor │    │ DHT Sensor │
    │   ENTRY   │    │   EXIT    │    │ Temp/Humid │
    └───────────┘    └───────────┘    └───────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Wi-Fi    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Python    │
                    │ Data Logger │
                    └──────┬──────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Excel Data Storage │
                 │       (.xlsx)     │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Flask Web Server  │
                 │     Dashboard     │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Live Analytics &  │
                 │ Historical Graphs │
                 └───────────────────┘
