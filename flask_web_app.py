from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import subprocess
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for Flet frontend communication

# Data storage for sensor and control states
state = {
    "light_intensity": 0.0,  # Light intensity from solar panel (0-100%)
    "motion": 0,             # Motion detection (0 or 1)
    "temperature": 25.0,     # Temperature in °C (default to typical room temp)
    "humidity": 50.0,        # Humidity in % (default to typical indoor humidity)
    "led_override": False,   # Override automatic LED control
    "led_manual": False,     # Manual LED state (on/off)
    "fan_override": False,   # Override automatic fan control
    "fan_manual": False,     # Manual fan state (on/off)
    "fan_speed": 0           # Fan speed (0-100%)
}

# Simple HTML Dashboard for monitoring
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Room Backend Dashboard</title>
    <meta http-equiv="refresh" content="1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
        }
        p {
            font-size: 16px;
            margin: 10px 0;
            color: #555;
        }
        .label {
            font-weight: bold;
            color: #007bff;
        }
        .timestamp {
            font-size: 14px;
            color: #888;
            margin-top: 20px;
        }
        a {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart Room Backend Dashboard</h1>
        <p><span class="label">Light Intensity:</span> {{ state['light_intensity']|round(1) }}%</p>
        <p><span class="label">Motion:</span> {{ 'Detected' if state['motion'] else 'None' }}</p>
        <p><span class="label">Temperature:</span> {{ state['temperature']|round(1) if state['temperature'] != -1 else 'Error' }} °C</p>
        <p><span class="label">Humidity:</span> {{ state['humidity']|round(1) if state['humidity'] != -1 else 'Error' }} %</p>
        <p><span class="label">LED Override:</span> {{ state['led_override'] }}</p>
        <p><span class="label">LED Manual:</span> {{ state['led_manual'] }}</p>
        <p><span class="label">Fan Override:</span> {{ state['fan_override'] }}</p>
        <p><span class="label">Fan Manual:</span> {{ state['fan_manual'] }}</p>
        <p><span class="label">Fan Speed:</span> {{ state['fan_speed'] }}%</p>
        <p class="timestamp">Last Updated: {{ timestamp }}</p>
        <a href="/simulate">Simulate ESP32 Data</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Render the HTML dashboard with current state and timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HTML_TEMPLATE, state=state, timestamp=timestamp)

@app.route('/esp/update', methods=['POST'])
def esp_update():
    """Receive sensor data from ESP32 and update state."""
    data = request.json
    state["light_intensity"] = data.get("light_intensity", state["light_intensity"])
    state["motion"] = data.get("motion", state["motion"])
    state["temperature"] = data.get("temperature", state["temperature"])
    state["humidity"] = data.get("humidity", state["humidity"])
    print(f"ESP Update: {data}")
    return jsonify({"status": "success"})

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Provide current state to Flet frontend."""
    return jsonify(state)

@app.route('/control', methods=['POST'])
def control():
    """Receive control commands from Flet and update state."""
    data = request.json
    state["led_override"] = data.get("led_override", state["led_override"])
    state["led_manual"] = data.get("led_manual", state["led_manual"])
    state["fan_override"] = data.get("fan_override", state["fan_override"])
    state["fan_manual"] = data.get("fan_manual", state["fan_manual"])
    state["fan_speed"] = data.get("fan_speed", state["fan_speed"])
    print(f"Control Update: {data}")
    return jsonify({"status": "success"})

@app.route('/simulate', methods=['GET'])
def simulate():
    """Simulate ESP32 sensor data for testing."""
    state["light_intensity"] = random.uniform(0, 100)  # Random light intensity (0-100%)
    state["motion"] = random.randint(0, 1)            # Random motion (0 or 1)
    state["temperature"] = random.uniform(20, 30)     # Random temperature (20-30°C)
    state["humidity"] = random.uniform(40, 60)        # Random humidity (40-60%)
    print(f"Simulated Update: {state}")
    return jsonify({"status": "simulated"})

def run_flet():
    """Launch Flet frontend (app.py) as a separate process."""
    subprocess.Popen(["python", "app.py"], shell=True)

if __name__ == "__main__":
    run_flet()  # Start Flet app
    app.run(host='0.0.0.0', port=5000, debug=True)