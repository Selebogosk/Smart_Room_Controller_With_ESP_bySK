#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <NewPing.h>

// WiFi and Server Configuration
#define WIFI_SSID "Kico SK"
#define WIFI_PASSWORD "Robotics23"
#define SERVER_URL "http://192.168.1.65:5000/esp/update"

// Pin Definitions for ESP32-S
#define DHTPIN 15
#define DHTTYPE DHT11
#define TRIGGER_PIN 13
#define ECHO_PIN 12
#define LIGHT_PIN 4
#define FAN_PIN 18
#define LED_PIN 19
#define MAX_DISTANCE 200

// Initialize Sensors
DHT dht(DHTPIN, DHTTYPE);
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  Serial.begin(115200);
  
  pinMode(FAN_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(FAN_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  
  dht.begin();

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    StaticJsonDocument<200> doc;

    // Read sensor data
    float lightIntensity = analogRead(LIGHT_PIN) / 4095.0 * 100.0;
    Serial.print("Raw ADC Value: ");
    Serial.println(analogRead(LIGHT_PIN)); // Debug ADC
    unsigned int distance = sonar.ping_cm();
    Serial.print("Ultrasonic Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
    int motion = (distance > 0 && distance < 50) ? 1 : 0;
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read DHT sensor!");
      temperature = -1;
      humidity = -1;
    }

    doc["light_intensity"] = lightIntensity;
    doc["motion"] = motion;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;

    String jsonStr;
    serializeJson(doc, jsonStr);

    Serial.print("WiFi Status: ");
    Serial.println(WiFi.status());
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonStr);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Response from Flask: " + response);
    } else {
      Serial.print("HTTP Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();

    digitalWrite(LED_PIN, motion ? HIGH : LOW);
    digitalWrite(FAN_PIN, temperature > 28.0 ? HIGH : LOW);

    Serial.print("Sensor data sent: ");
    serializeJson(doc, Serial);
    Serial.println();
  } else {
    Serial.println("WiFi disconnected");
  }

  delay(1000);
}