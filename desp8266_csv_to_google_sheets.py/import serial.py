import serial
import serial.tools.list_ports
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

BAUD = 115200
SHEET_NAME = "Building_Live_Data"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_KEY_FILE = os.path.join(BASE_DIR, "JSON_KEY_FILE.json")

def choose_port():
    ports = list(serial.tools.list_ports.comports())
    for i, p in enumerate(ports):
        print(f"[{i}] {p.device}")
    return ports[int(input("Select COM port: "))].device

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

port = choose_port()
ser = serial.Serial(port, BAUD, timeout=1)
time.sleep(2)

header_written = False
print("Live logging started...")

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        if "GPS" in line:
            print(line)
            continue

        values = line.split(",")

        if not header_written and "total_height" in line.lower():
            sheet.insert_row(values, 1)
            header_written = True
            continue

        if header_written and len(values) >= 7:
            sheet.append_row(values)
            print("Row:", values)

except KeyboardInterrupt:
    ser.close()
    print("Stopped")
