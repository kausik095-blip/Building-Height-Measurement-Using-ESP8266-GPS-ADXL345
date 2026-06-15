#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

// ================= USER SETTINGS =================
#define SENSOR_HEIGHT 1.5        // meters
#define GPS_TIMEOUT_MS 60000     // 60 seconds
#define SAT_AVG_COUNT 5          // averaging window
// =================================================

// ---------- PINS ----------
#define GPS_RX 12   // D6
#define GPS_TX 14   // D5

// ---------- OBJECTS ----------
SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
TinyGPSPlus gps;
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

// ---------- VARIABLES ----------
double baseLat = 0, baseLon = 0;
bool baseCaptured = false;

bool manualMode = false;
double manualDistance = 0;

unsigned long startTime;
unsigned long lastSend = 0;

// Satellite averaging
int satBuffer[SAT_AVG_COUNT];
int satIndex = 0;

// ---------- GPS DISTANCE ----------
double gpsDistance(double lat1, double lon1, double lat2, double lon2) {
  const double R = 6371000.0;
  double dLat = radians(lat2 - lat1);
  double dLon = radians(lon2 - lon1);
  lat1 = radians(lat1);
  lat2 = radians(lat2);
  double a = sin(dLat/2)*sin(dLat/2) +
             cos(lat1)*cos(lat2)*sin(dLon/2)*sin(dLon/2);
  return R * 2 * atan2(sqrt(a), sqrt(1 - a));
}

int averageSatellites(int current) {
  satBuffer[satIndex++] = current;
  if (satIndex >= SAT_AVG_COUNT) satIndex = 0;

  int sum = 0;
  for (int i = 0; i < SAT_AVG_COUNT; i++) sum += satBuffer[i];
  return sum / SAT_AVG_COUNT;
}

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600);
  Wire.begin(4, 5);

  accel.begin();
  accel.setRange(ADXL345_RANGE_16_G);

  startTime = millis();

  Serial.println("SYSTEM STARTED");
  Serial.println("MODE=AUTO (GPS)");
  Serial.println("time,mode,distance,tilt,total_height");
}

void loop() {

  // -------- READ SERIAL COMMANDS FROM PYTHON --------
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("MANUAL=")) {
      manualDistance = cmd.substring(7).toFloat();
      manualMode = true;
      Serial.println("MODE=MANUAL");
    }
    if (cmd == "AUTO") {
      manualMode = false;
      baseCaptured = false;
      startTime = millis();
      Serial.println("MODE=AUTO (GPS)");
    }
  }

  // -------- GPS PROCESSING --------
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  bool gpsFix = gps.location.isValid();
  int sats = gps.satellites.isValid() ? gps.satellites.value() : 0;
  int avgSats = averageSatellites(sats);

  // -------- GPS TIMEOUT --------
  if (!gpsFix && !manualMode && millis() - startTime > GPS_TIMEOUT_MS) {
    manualMode = true;
    Serial.println("GPS TIMEOUT – SWITCH TO MANUAL MODE");
  }

  double distance = 0;

  if (!manualMode && gpsFix && avgSats >= 5) {
    if (!baseCaptured) {
      baseLat = gps.location.lat();
      baseLon = gps.location.lng();
      baseCaptured = true;
      delay(2000);
      return;
    }
    distance = gpsDistance(baseLat, baseLon,
                            gps.location.lat(),
                            gps.location.lng());
  } else if (manualMode) {
    distance = manualDistance;
  } else {
    return; // waiting for GPS
  }

  if (millis() - lastSend < 2000) return;
  lastSend = millis();

  // -------- ADXL345 --------
  sensors_event_t event;
  accel.getEvent(&event);

  float ax = event.acceleration.x / 9.81;
  float ay = event.acceleration.y / 9.81;
  float az = event.acceleration.z / 9.81;

  float tiltRad = atan(ax / sqrt(ay * ay + az * az));
  float tiltDeg = tiltRad * 180.0 / PI;

  float totalHeight = (distance * tan(tiltRad)) + SENSOR_HEIGHT;

  Serial.print(millis()/1000); Serial.print(",");
  Serial.print(manualMode ? "MANUAL" : "AUTO"); Serial.print(",");
  Serial.print(distance,2); Serial.print(",");
  Serial.print(tiltDeg,2); Serial.print(",");
  Serial.println(totalHeight,2);
}
