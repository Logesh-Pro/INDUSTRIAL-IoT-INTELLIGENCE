# Industrial IoT People Monitoring & Environmental Analytics

An ESP32-based Industrial IoT monitoring system that combines **people counting, temperature and humidity monitoring, Wi-Fi communication, data logging, and a real-time analytics dashboard**.

The system uses two IR sensors to determine whether people are entering or leaving an area, a DHT sensor for environmental measurements, and an ESP32 as the main controller.

Sensor data is transmitted over Wi-Fi and stored in an Excel file while a Flask-based web dashboard displays live readings, historical graphs, statistics, and automatic environmental analysis.

---

## 📌 Project Overview

The system is designed to monitor an industrial or indoor environment in real time.

### Current capabilities

- 👥 People counting
- 🌡️ Temperature monitoring
- 💧 Humidity monitoring
- 📊 Real-time graphs
- 📈 Historical data analysis
- 🧠 Automatic environmental analysis
- 📁 Excel data logging
- 🌐 Wi-Fi communication
- 🖥️ Web-based monitoring dashboard
- 📡 ESP32 HTTP data interface
- 📊 Statistical analysis of collected data

The project is designed in a modular way so additional hardware such as a relay-controlled fan, LEDs, and a buzzer can be integrated later.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       ESP32         │
                         │   Main Controller   │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │ IR Sensor 1 │       │ IR Sensor 2 │       │ DHT Sensor  │
       │    ENTRY    │       │     EXIT    │       │ Temp/Humid  │
       └─────────────┘       └─────────────┘       └─────────────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │     Wi-Fi     │
                            └───────┬───────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Python Logger     │
                         │  esp32_logger.py    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Excel          │
                         │   .xlsx Runtime     │
                         │       Data          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Flask Server     │
                         │    dashboard.py     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │       Web Dashboard         │
                     │                             │
                     │ • Live Readings             │
                     │ • Historical Graphs         │
                     │ • Statistics                │
                     │ • Smart Analytics            │
                     │ • Environmental Analysis    │
                     └─────────────────────────────┘
# 🔌 Hardware

## Current Hardware

The current project uses:

- ESP32 development board
- 2 × IR sensors
- Entry sensor
- Exit sensor
- DHT temperature/humidity sensor
- Breadboard
- Jumper wires

## Planned Hardware Expansion

The project can later be expanded with:

- Relay module
- 5V DC motor with fan
- 3 × LEDs
- 3 × resistors
- Buzzer

These components are intended to provide automatic physical responses based on the collected sensor data.

---

# 👥 People Counting

Two IR sensors are used to determine the direction of movement.

The system uses a sequence-based approach rather than simply increasing or decreasing the counter whenever a sensor is triggered.

## Person Entering

```text
ENTRY SENSOR
     │
     ▼
EXIT SENSOR
     │
     ▼
People Inside + 1
```

### Example

```text
Before: People Inside = 5


ENTRY detected
        ↓
EXIT detected
        ↓


After: People Inside = 6
```

## Person Leaving

```text
EXIT SENSOR
     │
     ▼
ENTRY SENSOR
     │
     ▼
People Inside - 1
```

### Example

```text
Before: People Inside = 6


EXIT detected
        ↓
ENTRY detected
        ↓


After: People Inside = 5
```

## Sequence-Based Detection

The system attempts to distinguish between:

- A person entering
- A person leaving
- A single sensor being triggered accidentally
- An incomplete sensor sequence
- A sequence timeout

This is important because simply counting every IR trigger can produce incorrect occupancy values.

---

# 🌡️ Environmental Monitoring

The ESP32 reads environmental information from the DHT sensor.

The monitored parameters are:

- Temperature
- Humidity

## Example Reading

```text
People:     6
Temperature: 29.9 °C
Humidity:    64.3 %
```

These values are transmitted through Wi-Fi and recorded by the Python data logger.

---

# 📡 Wi-Fi Communication

The ESP32 provides Wi-Fi communication for the monitoring system.

The ESP32 exposes an HTTP endpoint containing the current sensor information.

Example:

```text
http://192.168.4.1/data
```

The endpoint provides data used by the Python logger.

Typical data includes:

- People
- Temperature
- Humidity

## Data Flow

```text
ESP32
  │
  │ HTTP
  ▼
192.168.4.1/data
  │
  ▼
Python Data Logger
```

---

# 📊 Data Format

The collected readings are stored in a structured format.

## Example

```text
Time                    People    Temperature    Humidity
----------------------------------------------------------------
2026-08-20 00:52:00        5          29.9          64.1
2026-08-20 00:52:02        5          29.9          64.2
2026-08-20 00:52:04        6          29.9          64.2
```

## Main Fields

| Field | Description |
|---|---|
| Time | Date and time of the reading |
| People | Number of people inside |
| Temperature | Temperature in °C |
| Humidity | Relative humidity in % |

---

# 📁 Excel Data Logging

The Python logger stores sensor readings in:

```text
industrial_iot_data.xlsx
```

The Excel file contains continuously changing runtime data.

## Example

```text
2026-08-20 00:51:48 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %
2026-08-20 00:51:50 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %
2026-08-20 00:51:52 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %
```

The logger continuously adds new readings.

The Excel file is intentionally excluded from Git because it is runtime data rather than application source code.

---

# 🖥️ Real-Time Web Dashboard

The Flask application reads the collected sensor data and presents it through a browser.

The dashboard provides:

- Current readings
- People inside
- Current temperature
- Current humidity
- Historical graphs
- Statistical information
- Smart analytics
- Automatic environmental analysis

Open the dashboard locally at:

```text
http://127.0.0.1:5000
```

---

# 📈 Dashboard Features

## Current People Count

The dashboard displays the latest number of people detected inside the monitored area.

### Example

```text
People Inside


6
```

## Current Temperature

The dashboard displays the latest temperature reading.

### Example

```text
Temperature


29.9 °C
```

## Current Humidity

The dashboard displays the latest humidity reading.

### Example

```text
Humidity


64.3 %
```

---

# 📊 Sensor History

The dashboard displays historical sensor data through graphs.

## People Graph

Shows changes in occupancy over time.

```text
People
  │
  │       ╭───╮
  │   ╭───╯   ╰────
  │───╯
  └──────────────────── Time
```

## Temperature Graph

Shows temperature changes over time.

```text
Temperature
     │
30.0 │       ╭──╮
29.9 │───────╯  ╰────
     │
     └──────────────── Time
```

## Humidity Graph

Shows humidity changes over time.

```text
Humidity
   │
65 │
64 │────╮────╭────
63 │    ╰────╯
   │
   └──────────────── Time
```

The graphs are generated using Chart.js.

---

# 🧠 Smart Analytics

The dashboard calculates statistics from the collected data.

Current analytics include:

- Average people
- Peak occupancy
- Average temperature
- Maximum temperature
- Minimum temperature
- Average humidity
- Maximum humidity
- Minimum humidity

## Example

```text
Average People


5.7


Peak Occupancy


6


Average Temperature


29.9 °C


Maximum Temperature


29.9 °C


Minimum Temperature


29.9 °C


Maximum Humidity


64.3 %


Minimum Humidity


64.1 %
```

---

# 🔎 Automatic Analysis

The dashboard automatically interprets the collected values.

## Example Occupancy Analysis

```text
Occupancy analysis:


The highest recorded occupancy is 6 people,
while the average occupancy is 5.7 people.
```

## Example Temperature Analysis

```text
Temperature analysis:


The temperature ranges from 29.9 °C to 29.9 °C,
with an average of 29.9 °C.
```

## Example Humidity Analysis

```text
Humidity analysis:


Humidity ranges from 64.1% to 64.3%.
```

The dashboard can also determine a general environmental condition.

## Example

```text
Current environment:


Warm environment
```

---

# 📡 Complete Data Flow

The complete system works as follows:

```text
       ┌──────────────────────┐
       │     IR Sensors       │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │        ESP32         │
       │                      │
       │ People Count         │
       │ Temperature          │
       │ Humidity             │
       └──────────┬───────────┘
                  │
                  │ Wi-Fi
                  ▼
       ┌──────────────────────┐
       │   Python Logger      │
       │   esp32_logger.py    │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │      Excel File      │
       │   .xlsx Runtime Data │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │    Flask Dashboard   │
       │     dashboard.py     │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────┐
       │      Analytics       │
       │                      │
       │ Live Data            │
       │ Graphs               │
       │ Statistics           │
       │ Automatic Analysis   │
       └──────────────────────┘
```

---

# 💻 Software

## ESP32

The ESP32 is the main embedded controller.

It handles:

- IR sensor input
- People counting
- DHT sensor readings
- Wi-Fi communication
- HTTP data serving

## Python

Python is used for:

- Receiving ESP32 data
- Logging sensor readings
- Writing data to Excel
- Running the web dashboard
- Performing data processing

## Flask

Flask provides the local web server used by the dashboard.

## OpenPyXL

OpenPyXL is used to read and write Excel `.xlsx` files.

## Requests

The Requests library is used by the Python data logger to communicate with the ESP32 through HTTP.

## Chart.js

Chart.js is used to display interactive graphs in the browser.

---

# 📂 Project Structure

```text
iiot/
│
├── dashboard.py
│   └── Flask web dashboard
│
├── dashboard_backup.py
│   └── Backup dashboard version
│
├── esp32_logger.py
│   └── ESP32 data logger
│
├── industrial_iot_data.xlsx
│   └── Runtime sensor data
│
├── .gitignore
│   └── Prevents runtime Excel data from being committed
│
└── README.md
    └── Project documentation
```

> **Note:** `industrial_iot_data.xlsx` is intentionally ignored by Git and therefore should not be pushed to the repository.

---

# 🛠️ Installation

## 1. Install Python

Check the installed Python version:

```powershell
python --version
```

Example:

```text
Python 3.12.10
```

---

# 📦 Install Required Python Packages

Run:

```powershell
python -m pip install requests openpyxl flask
```

The required packages are:

```text
requests
openpyxl
flask
```

---

# ▶️ Running the Data Logger

Open PowerShell in the project directory:

```powershell
cd C:\Users\admin\Desktop\iiot
```

Run:

```powershell
python esp32_logger.py
```

The logger should display readings similar to:

```text
=================================
 INDUSTRIAL IoT DATA LOGGER
=================================
Logging data from ESP32...
Press Ctrl+C to stop.


2026-08-20 00:51:48 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %
2026-08-20 00:51:50 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %
2026-08-20 00:51:52 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %
```

The readings are continuously stored in the Excel file.

---

# ▶️ Running the Dashboard

Open another PowerShell window.

Go to the project directory:

```powershell
cd C:\Users\admin\Desktop\iiot
```

Run:

```powershell
python dashboard.py
```

The Flask server should start.

Open the dashboard in a browser:

```text
http://127.0.0.1:5000
```

---

# 🔄 Running Both Components

The data logger and dashboard are separate Python processes.

## Terminal 1 — Data Logger

```powershell
cd C:\Users\admin\Desktop\iiot
python esp32_logger.py
```

## Terminal 2 — Dashboard

```powershell
cd C:\Users\admin\Desktop\iiot
python dashboard.py
```

Then open:

```text
http://127.0.0.1:5000
```

The data logger continuously updates the Excel file.

The dashboard reads the latest stored information and updates the displayed data.

---

# 🌐 ESP32 Data Endpoint

The ESP32 data can be accessed through:

```text
http://192.168.4.1/data
```

This provides the current sensor information directly from the ESP32.

The architecture is:

```text
ESP32
  │
  ▼
192.168.4.1/data
  │
  ▼
Python Logger
  │
  ▼
industrial_iot_data.xlsx
  │
  ▼
Flask Dashboard
```

---

# 📊 Example Monitoring Session

A typical monitoring session can produce data such as:

```text
People: 6
Temperature: 29.9 °C
Humidity: 64.3 %
```

The dashboard can then calculate:

```text
Average People:       5.7
Peak Occupancy:       6


Average Temperature:  29.9 °C
Maximum Temperature:  29.9 °C
Minimum Temperature:  29.9 °C


Maximum Humidity:     64.3 %
Minimum Humidity:     64.1 %
```

---

# 🔐 Git and Runtime Data

The Excel file contains continuously changing sensor data.

It is therefore intentionally excluded from version control.

The `.gitignore` file contains:

```gitignore
industrial_iot_data.xlsx
```

This means Git will track the application source code but not the continuously changing Excel database.

---

# 📦 Files to Commit

The main source files are:

```text
.gitignore
README.md
dashboard.py
dashboard_backup.py
esp32_logger.py
```

The runtime Excel file should remain local:

```text
industrial_iot_data.xlsx
```

---

# 🚀 Future Development

The project is designed to be expanded into a more complete Industrial IoT monitoring and automation platform.

Planned additions include:

- Automated ventilation
- Relay-controlled fan
- LED status indicators
- Temperature alarm
- Buzzer
- Advanced occupancy analytics
- Environmental comfort scoring
- Occupancy duration analysis
- Time-of-day analysis
- Trend analysis
- Historical reports
- Automatic alerts
- Sensor health monitoring

---

# 🌀 Automated Ventilation

A relay can be used to control the 5V DC fan.

## Example Logic

```text
Temperature / Occupancy
          │
          ▼
     Control Logic
          │
          ▼
       Relay
          │
          ▼
      5V DC Fan
```

The fan could eventually be controlled according to environmental conditions.

For example:

```text
High temperature
       │
       ▼
   Relay ON
       │
       ▼
     Fan ON
```

---

# 💡 LED Occupancy Indicator

Three LEDs can be used to represent occupancy levels.

## Example Concept

```text
┌──────────────────────────────┐
│       Occupancy Status       │
├──────────────────────────────┤
│                              │
│  GREEN   → Normal            │
│  YELLOW  → Moderate          │
│  RED     → High              │
│                              │
└──────────────────────────────┘
```

The exact thresholds can be configured later.

---

# 🔔 Temperature Alarm

A buzzer can eventually provide an audible warning when the temperature exceeds a configured threshold.

## Example

```text
Temperature
     │
     ▼
Threshold Check
     │
     ├───────────────┐
     │               │
 Normal           High
     │               │
     ▼               ▼
Buzzer OFF       Buzzer ON
```

---

# 🧠 Advanced Analytics Possibilities

The collected sensor data can be used for additional analysis.

Possible future dashboard features include:

- Occupancy Heatmaps
- Time-of-Day Analysis
- Occupancy Duration
- Environmental Comfort Scoring
- Trend Analysis

---

# 📍 Occupancy Heatmaps

Analyze when the monitored area is most occupied.

```text
Time of Day
     │
     ▼
┌─────────────────────────────┐
│ Occupancy Distribution      │
│                             │
│ Morning     █████            │
│ Afternoon   █████████        │
│ Evening     ████             │
└─────────────────────────────┘
```

---

# 🕐 Time-of-Day Analysis

Compare occupancy and environmental conditions during different parts of the day.

Possible periods:

- Morning
- Afternoon
- Evening
- Night

---

# ⏱️ Occupancy Duration

Calculate how long the area remains at different occupancy levels.

## Example

| Occupancy Level | Duration |
|---|---:|
| 0 people | 15 min |
| 1–3 people | 32 min |
| 4–6 people | 48 min |
| 7+ people | 10 min |

---

# 🌡️ Environmental Comfort Scoring

Temperature and humidity can be analyzed together to provide a simple environmental comfort indicator.

## Example Concept

```text
Temperature + Humidity
          │
          ▼
   Comfort Analysis
          │
          ▼
┌─────────────────────┐
│ Comfortable         │
│ Warm                │
│ Humid               │
│ Very Warm           │
└─────────────────────┘
```

---

# 📈 Trend Analysis

Historical data can be analyzed to identify whether:

- Temperature is rising
- Temperature is falling
- Humidity is rising
- Humidity is falling
- Occupancy is increasing
- Occupancy is decreasing

## Example

```text
Temperature Trend


29.4 → 29.5 → 29.7 → 29.8 → 29.9


                ↑
           Rising Trend
```

---

# 📈 Possible Future Dashboard Structure

```text
┌─────────────────────────────────────────────┐
│          INDUSTRIAL IoT MONITOR             │
├─────────────────────────────────────────────┤
│                                             │
│  PEOPLE       TEMPERATURE       HUMIDITY    │
│    6             29.9°C          64.3%      │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│              LIVE SENSOR DATA               │
│                                             │
│             📈 People Graph                 │
│                                             │
│             📈 Temperature Graph            │
│                                             │
│             📈 Humidity Graph               │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│              SMART ANALYTICS                │
│                                             │
│ Average Occupancy                           │
│ Peak Occupancy                              │
│ Average Temperature                         │
│ Temperature Range                           │
│ Humidity Range                              │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│             AUTOMATIC ANALYSIS              │
│                                             │
│ Occupancy Analysis                          │
│ Temperature Analysis                        │
│ Humidity Analysis                           │
│ Environmental Condition                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

# 🎯 Project Goal

The goal of this project is to create a small but expandable Industrial IoT monitoring platform that connects physical sensors with software-based data collection, storage, visualization, and analytics.

The overall concept is:

```text
┌────────────────────┐
│   Physical World   │
│                    │
│ IR Sensors         │
│ DHT Sensor         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│       ESP32        │
│                    │
│ Sensor Processing  │
│ People Counting    │
│ Wi-Fi              │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│       Python       │
│                    │
│ Data Collection    │
│ Data Processing    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│       Excel        │
│                    │
│ Runtime Data Store │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   Flask Dashboard  │
│                    │
│ Live Data          │
│ Graphs             │
│ Statistics         │
│ Analytics          │
└────────────────────┘
```

The project demonstrates how real-world sensor data can be:

```text
COLLECTED
    ↓
TRANSMITTED
    ↓
STORED
    ↓
ANALYZED
    ↓
VISUALIZED
    ↓
USED FOR AUTOMATION
```

---

# 🧩 Technology Stack

| Layer | Technology |
|---|---|
| Microcontroller | ESP32 |
| People Detection | 2 × IR Sensors |
| Environmental Sensor | DHT Sensor |
| Communication | Wi-Fi / HTTP |
| Data Collection | Python |
| HTTP Client | Requests |
| Data Storage | Excel .xlsx |
| Excel Library | OpenPyXL |
| Web Server | Flask |
| Graphs | Chart.js |
| Frontend | HTML / CSS / JavaScript |
| Version Control | Git |

---

# 📌 Current Project Status

## Completed

- [x] ESP32 setup
- [x] ESP32 serial communication
- [x] IR sensor integration
- [x] People counting logic
- [x] Entry/exit sequence detection
- [x] DHT sensor integration
- [x] Temperature reading
- [x] Humidity reading
- [x] ESP32 Wi-Fi communication
- [x] ESP32 /data endpoint
- [x] Python data logger
- [x] Excel data storage
- [x] Flask dashboard
- [x] Real-time dashboard updates
- [x] People graph
- [x] Temperature graph
- [x] Humidity graph
- [x] Statistical calculations
- [x] Automatic analysis
- [x] Git repository setup
- [x] Runtime Excel file excluded from Git

## Planned

- [ ] Relay integration
- [ ] 5V DC fan control
- [ ] LED occupancy indicators
- [ ] Buzzer alarm
- [ ] Advanced alerts
- [ ] Advanced analytics
- [ ] Additional dashboard features
- [ ] Long-term reporting

---

# ⚠️ Important Notes

The Excel file:

```text
industrial_iot_data.xlsx
```

is runtime data and is intentionally excluded from Git.

Do not remove the following line from `.gitignore` unless you intentionally want to version-control the generated sensor data:

```gitignore
industrial_iot_data.xlsx
```

The ESP32 must be accessible to the Python logger for data collection to continue.

The Flask dashboard depends on the Excel data generated by the logger.

Therefore, the normal operation is:

```text
ESP32
  ↓
Python Logger
  ↓
Excel
  ↓
Flask Dashboard
```

---

# 👨‍💻 Development Philosophy

The project is being developed incrementally.

Each hardware component is tested before integrating the next component.

The development approach is:

```text
ESP32
  ↓
IR Sensors
  ↓
People Counting
  ↓
DHT Sensor
  ↓
Wi-Fi
  ↓
Data Logging
  ↓
Excel
  ↓
Dashboard
  ↓
Analytics
  ↓
Relay
  ↓
Fan
  ↓
LEDs
  ↓
Buzzer
  ↓
Complete IoT Automation System
```

This modular approach makes it easier to identify hardware and software problems during development.

---

# 📜 License

This project can be adapted and extended for educational, experimental, and Industrial IoT development purposes.

---

# ⭐ Industrial IoT Monitoring Platform

```text
Sensors
   +
ESP32
   +
Wi-Fi
   +
Python
   +
Excel
   +
Flask
   +
Charts
   +
Analytics
   =
Industrial IoT Monitoring System
```

The project provides a foundation for building a larger IoT system capable of collecting real-world sensor data, storing it, analyzing it, visualizing it, and eventually using that information to control physical equipment automatically.
