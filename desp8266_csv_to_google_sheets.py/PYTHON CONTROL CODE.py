import serial
import serial.tools.list_ports
import time

BAUD = 115200

def choose_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No COM ports found")
        exit()

    print("Available COM ports:")
    for i, p in enumerate(ports):
        print(f"[{i}] {p.device}")

    choice = input("Select COM port: ").strip()
    if choice.isdigit():
        return ports[int(choice)].device

    for p in ports:
        if p.device.upper() == choice.upper():
            return p.device

    print("Invalid port")
    exit()

# ---------- SERIAL ----------
port = choose_port()
ser = serial.Serial(port, BAUD, timeout=1)
time.sleep(2)

print("\nCONTROL SYSTEM STARTED")
print("Commands:")
print("  auto")
print("  manual <distance_in_meters>")
print("  exit\n")

try:
    while True:
        # Read ESP8266 messages safely
        if ser.in_waiting:
            msg = ser.readline().decode(errors="ignore").strip()
            if msg:
                print("ESP:", msg)

        # User command
        cmd = input(">> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "auto":
            ser.write(b"AUTO\n")
            print("Sent AUTO mode command")

        elif cmd.startswith("manual"):
            try:
                distance = cmd.split()[1]
                ser.write(f"MANUAL={distance}\n".encode())
                print(f"Sent MANUAL distance = {distance} m")
            except IndexError:
                print("Usage: manual <distance_in_meters>")

except KeyboardInterrupt:
    print("\nStopped by user")

ser.close()
print("Serial closed")
