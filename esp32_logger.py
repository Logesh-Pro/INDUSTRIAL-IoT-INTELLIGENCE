import requests
import openpyxl
from datetime import datetime
import time
import os

ESP32_URL = "http://192.168.4.1/data"

file_name = "industrial_iot_data.xlsx"

# Create Excel file if it doesn't exist
if os.path.exists(file_name):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
else:
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    sheet.append([
        "Time",
        "People Inside",
        "Temperature (C)",
        "Humidity (%)"
    ])

    workbook.save(file_name)


print("=================================")
print(" INDUSTRIAL IoT DATA LOGGER")
print("=================================")
print("Logging data from ESP32...")
print("Press Ctrl+C to stop.")
print()

while True:

    try:

        response = requests.get(ESP32_URL, timeout=3)

        values = response.text.strip().split(",")

        if len(values) == 3:

            people = int(values[0])
            temperature = float(values[1])
            humidity = float(values[2])

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sheet.append([
                now,
                people,
                temperature,
                humidity
            ])

            workbook.save(file_name)

            print(
                now,
                "| People:",
                people,
                "| Temp:",
                temperature,
                "C | Humidity:",
                humidity,
                "%"
            )

    except Exception as e:

        print("ESP32 connection error:", e)

    time.sleep(2)