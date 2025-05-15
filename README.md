# Smart Room IoT Dashboard

This repository contains the code for a Smart Room system that integrates an ESP32 with various sensors and actuators, a Flask-based backend to manage sensor data, and a Flet frontend to control and monitor the system. This project is aimed at creating an interactive and smart environment where sensors such as a DHT11 (temperature and humidity), ultrasonic sensor (motion detection), and light intensity sensor can be monitored, and devices like an LED and fan can be controlled.

---

## Project Structure

1. **ESP32 Firmware** - Collects sensor data and sends it to the backend.
2. **Flask Server** - Handles incoming data from the ESP32 and serves a simple web-based dashboard.
3. **Flet App** - A frontend application for controlling and viewing real-time sensor data.

---

## Features

* **Sensors:**

  * Light intensity
  * Motion detection (using ultrasonic sensor)
  * Temperature and humidity (using DHT11)

* **Actuators:**

  * LED control
  * Fan control (manual and automatic speed control)

* **Backend:**

  * Flask-based server that receives sensor data from the ESP32 and serves it via a simple HTML dashboard.
  * Data storage and manipulation for control states such as LED and fan control.

* **Frontend (Flet App):**

  * Real-time dashboard to display sensor data.
  * Controls for LED and fan override and manual operation.

---

## Requirements

* **ESP32** with support for Arduino IDE.

* **Libraries:**

  * `WiFi.h` - WiFi support for ESP32
  * `HTTPClient.h` - HTTP communication
  * `ArduinoJson.h` - JSON serialization
  * `DHT.h` - Temperature and humidity sensor support
  * `NewPing.h` - Ultrasonic sensor support

* **Backend:**

  * Python 3.x
  * Flask (`flask`, `flask_cors`)
  * Flet (`flet`)

---

## Setup Instructions

### 1. ESP32 Firmware

The firmware on the ESP32 connects to the Wi-Fi network, reads sensor data, and sends it to the Flask server.

* **Configure Wi-Fi credentials and Flask server URL in the ESP32 code:**

  ```cpp
  #define WIFI_SSID "your_wifi_ssid"
  #define WIFI_PASSWORD "your_wifi_password"
  #define SERVER_URL "http://<your_server_ip>:5000/esp/update"
  ```

* Upload the code to the ESP32 using the Arduino IDE.

### 2. Flask Backend

* Clone the repository:

  ```bash
  git clone https://github.com/yourusername/smart-room-iot-dashboard.git
  cd smart-room-iot-dashboard
  ```

* Install dependencies:

  ```bash
  pip install flask flask_cors
  ```

* Run the Flask server:

  ```bash
  python app.py
  ```

  The server will run on `http://0.0.0.0:5000`.

### 3. Flet Frontend

* Install the Flet package:

  ```bash
  pip install flet
  ```

* Run the Flet app:

  ```bash
  python flet_app.py
  ```

  The Flet app will create a dashboard for monitoring and controlling the smart room devices.

---

## API Endpoints

* **`/esp/update`** (POST):

  * Receives sensor data from the ESP32 (light intensity, motion, temperature, humidity) and updates the backend state.

* **`/dashboard`** (GET):

  * Provides the current sensor state as a JSON object for the Flet frontend.

* **`/control`** (POST):

  * Allows the Flet frontend to control the LED and fan manually or override their automatic behavior.

* **`/simulate`** (GET):

  * Simulates random sensor data for testing.

---

# Schematic



## Dashboard

Once the system is set up and running, navigate to the Flet app or Flask dashboard to view and control the system:

### Key Metrics:

* **Light Intensity:** Displays the percentage of light detected by the sensor.
* **Motion:** Indicates whether motion is detected based on the ultrasonic sensor.
* **Temperature:** Displays the room temperature in °C.
* **Humidity:** Displays the room humidity in percentage.

### Controls:

* **LED Override:** Manually control the LED based on the motion sensor or temperature.
* **Fan Override:** Manually control the fan and adjust its speed.

---

## Customization

* You can modify the behavior of the LED and fan in the Flask server by adjusting the control states.
* To change the sensor pins, update the pin definitions in the ESP32 code:

  ```cpp
  #define DHTPIN 15
  #define TRIGGER_PIN 13
  #define ECHO_PIN 12
  ```

---

## Troubleshooting

* **ESP32 Connection Issues:**

  * Ensure the Wi-Fi credentials are correctly configured.
  * Check if the Flask server is reachable from the ESP32.

* **Sensor Reading Failures:**

  * Ensure all sensors are correctly connected to the ESP32 and powered properly.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to contribute to this project by opening issues or submitting pull requests. Happy building! 🌟
