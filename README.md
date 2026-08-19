Hardware

The current project uses:

ESP32 development board
2 × IR sensors
Entry sensor
Exit sensor
DHT temperature/humidity sensor
Breadboard
Jumper wires

The planned hardware expansion includes:

Relay module
5V DC motor with fan
3 × LEDs
3 × resistors
Buzzer
Main Features
1. People Counting

Two IR sensors are used to determine the direction of movement.

Person entering
ENTRY → EXIT

The people count increases by one.

Person leaving
EXIT → ENTRY

The people count decreases by one.

The system uses a sequence-based approach instead of simply increasing or decreasing the count whenever a sensor is triggered.

This helps distinguish between:

A person entering
A person leaving
A single sensor being triggered accidentally
An incomplete sensor sequence
2. Environmental Monitoring

The ESP32 reads:

Temperature
Humidity

These values are periodically sent to the monitoring system.

Example:

People: 6
Temperature: 29.9 °C
Humidity: 64.3 %
3. Wi-Fi Communication

The ESP32 provides Wi-Fi connectivity for communication with the monitoring system.

The data can be accessed through the ESP32's HTTP interface.

Example endpoint:

http://192.168.4.1/data

The endpoint provides the latest sensor information to the Python data logger and dashboard.

4. Excel Data Logging

Sensor readings are continuously stored in:

industrial_iot_data.xlsx

The stored information includes:

Field	Description
Time	Date and time of reading
People	Number of people inside
Temperature	Temperature in °C
Humidity	Relative humidity in %

Example:

Time                    People    Temperature    Humidity
2026-08-20 00:52:00        5          29.9          64.1
2026-08-20 00:52:02        5          29.9          64.2
2026-08-20 00:52:04        6          29.9          64.2

The Excel file is intentionally excluded from Git because it contains continuously changing runtime data.

5. Real-Time Web Dashboard

A Flask web application reads the stored sensor data and presents it through a browser.

The dashboard provides:

Current readings
People inside
Current temperature
Current humidity
Historical graphs
People over time
Temperature over time
Humidity over time
Statistical information
Average people
Peak occupancy
Average temperature
Maximum temperature
Minimum temperature
Average humidity
Maximum humidity
Minimum humidity
6. Smart Analytics

The dashboard performs automatic analysis of the collected data.

Examples include:

Occupancy analysis:
The highest recorded occupancy is 6 people,
while the average occupancy is 5.7 people.

Temperature analysis:

The temperature ranges from 29.9 °C to 29.9 °C,
with an average of 29.9 °C.

Humidity analysis:

Humidity ranges from 64.1% to 64.3%.

The dashboard can also determine the general environmental condition, such as:

Warm environment
Software
ESP32

The ESP32 runs the embedded monitoring program and handles:

IR sensor input
People counting
DHT sensor readings
Wi-Fi communication
HTTP data serving
Python

Python is used for:

Receiving ESP32 data
Logging sensor readings
Writing data to Excel
Running the web dashboard
Flask

Flask provides the local web server for the dashboard.

OpenPyXL

OpenPyXL is used to read and write Excel files.

Requests

The Requests library is used by the Python data logger to communicate with the ESP32.

Chart.js

Chart.js is used to display interactive graphs in the browser.

Project Files
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
└── .gitignore
    └── Prevents Excel runtime data from being committed

industrial_iot_data.xlsx is intentionally ignored by Git.

Installation
1. Install Python

Check the installed Python version:

python --version

Example:

Python 3.12.10
2. Install required Python packages
python -m pip install requests openpyxl flask
Running the Data Logger

Open PowerShell in the project directory:

cd C:\Users\admin\Desktop\iiot

Run:

python esp32_logger.py

The logger should display readings similar to:

=================================
 INDUSTRIAL IoT DATA LOGGER
=================================
Logging data from ESP32...
Press Ctrl+C to stop.


2026-08-20 00:51:48 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %
2026-08-20 00:51:50 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %
2026-08-20 00:51:52 | People: 4 | Temp: 29.9 C | Humidity: 64.2 %

The readings are stored in the Excel file.

Running the Dashboard

Open another PowerShell window.

Go to the project directory:

cd C:\Users\admin\Desktop\iiot

Run:

python dashboard.py

The Flask server should start.

Open the dashboard in a browser:

http://127.0.0.1:5000
Data Flow

The complete data flow is:

IR Sensors
     │
     ▼
   ESP32
     │
     ├── People Count
     │
     ├── Temperature
     │
     └── Humidity
     │
     ▼
   Wi-Fi
     │
     ▼
Python Data Logger
     │
     ▼
Excel File
     │
     ▼
Flask Dashboard
     │
     ├── Live Readings
     ├── Graphs
     ├── Statistics
     └── Automatic Analysis
Current Example

A typical monitoring session can produce data such as:

People: 6
Temperature: 29.9 °C
Humidity: 64.3 %

The dashboard then calculates information such as:

Average People: 5.7
Peak Occupancy: 6
Average Temperature: 29.9 °C
Maximum Temperature: 29.9 °C
Minimum Temperature: 29.9 °C
Maximum Humidity: 64.3 %
Minimum Humidity: 64.1 %
Future Development

The project is designed to be expanded.

Planned additions include:

Automated ventilation

A relay will control a 5V DC fan based on environmental conditions and occupancy.

Visual warning system

Three LEDs can represent different occupancy levels.

Example:

Green   → Normal occupancy
Yellow  → Moderate occupancy
Red     → High occupancy
Temperature alarm

A buzzer can activate when the temperature exceeds a defined threshold.

Example:

Temperature >= threshold
        │
        ▼
     Buzzer ON
Advanced analytics

Future dashboard features can include:

Occupancy heatmaps
Time-of-day analysis
Environmental comfort scoring
Occupancy duration analysis
Temperature trend prediction
Humidity trend prediction
Daily/weekly reports
Automatic alerts
Sensor health monitoring
Important Note

The Excel file is runtime data and is intentionally excluded from version control.

The .gitignore file contains:

industrial_iot_data.xlsx

This keeps the Git repository focused on the actual application source code rather than continuously changing sensor data.

Project Goal

The goal of this project is to create a small but expandable Industrial IoT monitoring platform that connects physical sensors with:

Embedded Systems
        +
Wi-Fi
        +
Python
        +
Data Storage
        +
Web Dashboard
        +
Data Analytics

The project demonstrates how real-world sensor data can be collected, transmitted, stored, analyzed, and visualized as a complete IoT system.



### Then save it as


```text
C:\Users\admin\Desktop\iiot\README.md

After saving it, run:

git add README.md
git status

Don't commit yet. Show me the git status output and we'll make sure the README and your updated dashboard are the files going into the first commit.
