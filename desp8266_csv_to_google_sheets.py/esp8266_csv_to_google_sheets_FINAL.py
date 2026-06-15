import serial
import serial.tools.list_ports
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ================= USER SETTINGS =================
BAUD = 115200
GOOGLE_SHEET_NAME = "Building_Live_Data"

# 🔴 PUT YOUR REAL JSON FILE PATH HERE (IMPORTANT)
JSON_KEY_FILE = r"C:\Users\ADMIN\Downloads\my-project-123456.json"
# =================================================


def choose_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("❌ No COM ports found")
        return None

    print("Available COM ports:")
    for i, p in enumerate(ports):
        print(f"[{i}] {p.device}")

    choice = input("Select COM port (index or COM7): ").strip()

    if choice.isdigit():
        return ports[int(choice)].device

    for p in ports:
        if p.device.upper() == choice.upper():
            return p.device

    return None


# ========== GOOGLE SHEETS AUTH ==========
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

print("🔐 Connecting to Google Sheets...")
creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scope)
client = gspread.authorize(creds)

sheet = client.open(GOOGLE_SHEET_NAME).sheet1
print("✅ Google Sheets connected")


# ========== SERIAL CONNECTION ==========
port = choose_port()
if port is None:
    print("❌ Invalid COM port")
    exit()

ser = serial.Serial(port, BAUD, timeout=1)
time.sleep(2)

print("✅ Serial connected")
print("✅ Live logging started (Ctrl+C to stop)")


header_written = False

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        values = line.split(",")

        # WRITE HEADER
        if not header_written and "lat" in line.lower():
            sheet.insert_row(values, 1)
            header_written = True
            print("🟢 Header written to Google Sheet")
            continue

        # WRITE DATA ROW
        if header_written:
            sheet.append_row(values)
            print("➡ Row added:", values)

except KeyboardInterrupt:
    ser.close()
    print("\n🛑 Stopped safely. Data saved to Google Sheets.")
