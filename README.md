# Building Height Measurement Using ESP8266, GPS & ADXL345

## Overview

This project measures building height using:

- ESP8266 NodeMCU
- GPS Module (NEO-6M)
- ADXL345 Accelerometer
- Python GUI Control System
- Google Sheets Cloud Logging

The system calculates horizontal distance using GPS and tilt angle using the ADXL345 sensor. Building height is calculated using trigonometric formulas and displayed in real time.

---

## Features

✅ GPS-based distance measurement

✅ ADXL345 tilt angle calculation

✅ Automatic building height calculation

✅ GPS signal strength indication

✅ LED status monitoring

✅ Manual distance fallback mode

✅ Google Sheets live logging

✅ Python GUI Control System

✅ Confidence/Error Analysis

---

## Hardware Required

| Component | Quantity |
|------------|----------|
| ESP8266 NodeMCU | 1 |
| GPS NEO-6M Module | 1 |
| ADXL345 Accelerometer | 1 |
| LED | 1 |
| 220Ω Resistor | 1 |
| Breadboard | 1 |
| Jumper Wires | As required |

---

## Circuit Connections

### GPS Module

GPS TX → ESP8266 D6 (GPIO12)

GPS RX → ESP8266 D5 (GPIO14)

GPS VCC → 3.3V / 5V

GPS GND → GND

### ADXL345

ADXL345 SDA → ESP8266 D2 (GPIO4)

ADXL345 SCL → ESP8266 D1 (GPIO5)

ADXL345 VCC → 3.3V

ADXL345 GND → GND

### LED

ESP8266 D4 (GPIO2) → 220Ω → LED → GND

---

## Working Principle

1. ESP8266 captures GPS coordinates.
2. ADXL345 measures tilt angle.
3. GPS calculates horizontal distance.
4. Building height is calculated using:

Height = Distance × tan(θ) + Sensor Height

5. Data is sent to Python.
6. Python logs data to Google Sheets.
7. Confidence analysis is performed.

---

## GPS Status Indicator

| GPS Status | LED |
|------------|-----|
| Searching | Fast Blink |
| Weak Fix | Slow Blink |
| Strong Fix | Solid ON |

---

## Example Output

time_s,status,distance_m,tilt_deg,total_height_m

12,AUTO,18.45,28.60,11.90

14,AUTO,18.46,28.55,11.88

16,AUTO,18.44,28.62,11.92

---

## Software Requirements

- Arduino IDE
- Python 3.10+
- Google Sheets API
- gspread
- pyserial
- oauth2client

---

## Install Python Packages

pip install pyserial gspread oauth2client

---

## Future Improvements

- WiFi cloud dashboard
- Mobile application
- GPS averaging filter
- Advanced calibration
- Building mapping system

---

## Author

Kausik K

Electronics and Communication Engineering
