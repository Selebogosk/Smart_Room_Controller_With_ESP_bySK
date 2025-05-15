import flet as ft
import requests
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Server URL
SERVER_URL = "http://192.168.1.65:5000"

async def main(page: ft.Page):
    logger.debug("Initializing Flet app")
    page.title = "🌟 Smart Room Dashboard 🌟"
    page.bgcolor = "#0d47a1"  # Hex color for stability (blue_900)
    page.padding = 20
    page.window_width = 800
    page.window_height = 600
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#00b8d4",  # Cyan 400
            secondary="#ffb300",  # Amber 300
            background="#0d47a1",  # Blue 900
        )
    )

    # Backend communication
    def fetch_data():
        try:
            logger.debug(f"Fetching data from {SERVER_URL}/dashboard")
            response = requests.get(f"{SERVER_URL}/dashboard", timeout=5)  # Added timeout
            response.raise_for_status()
            data = response.json()
            return data if data else {"light_intensity": 0.0, "motion": 0, "temperature": 25.0, "humidity": 50.0, "led_override": False, "led_manual": False, "fan_override": False, "fan_manual": False, "fan_speed": 0}
        except Exception as e:
            logger.error(f"Fetch data failed: {e}")
            return None

    def update_control(data):
        try:
            logger.debug(f"Sending control data: {data}")
            response = requests.post(f"{SERVER_URL}/control", json=data, timeout=5)  # Added timeout
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Update control failed: {e}")

    # Update UI
    def update_ui(e=None):
        logger.debug("Updating UI")
        data = fetch_data()
        if data:
            light_level_text.value = f"💡 Light Intensity: {data.get('light_intensity', 0.0):.1f}%"
            motion_text.value = f"🏃 Motion: {'Detected 🟢' if data.get('motion', 0) else 'None 🔴'}"
            temp_text.value = f"🌡️ Temp: {data.get('temperature', 25.0):.1f} °C"
            humidity_text.value = f"💧 Humidity: {data.get('humidity', 50.0):.1f} %"
            led_switch.value = data.get("led_manual", False) if data.get("led_override", False) else False
            fan_switch.value = data.get("fan_manual", False) if data.get("fan_override", False) else False
            fan_slider.value = data.get("fan_speed", 0)
        else:
            logger.warning("No data to update UI")
            light_level_text.value = "💡 Light Intensity: N/A"
            motion_text.value = "🏃 Motion: N/A"
            temp_text.value = "🌡️ Temp: N/A"
            humidity_text.value = "💧 Humidity: N/A"
        page.update()

    # Event listeners
    def led_toggle(e):
        update_control({"led_override": True, "led_manual": e.control.value})
        update_ui()

    def fan_toggle(e):
        update_control({"fan_override": True, "fan_manual": e.control.value})
        update_ui()

    def fan_speed_change(e):
        update_control({"fan_speed": int(e.control.value)})
        update_ui()

    # UI controls
    title = ft.Text(
        "🌟 Smart Room Control 🌟",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="#4dd0e1",  # Cyan 200
        text_align=ft.TextAlign.CENTER
    )

    light_level_text = ft.Text("💡 Light Intensity: 0.0%", size=20, color="#ffca28")  # Amber 200
    motion_text = ft.Text("🏃 Motion: None 🔴", size=20, color="#ef9a9a")  # Red 200
    temp_text = ft.Text("🌡️ Temp: 25.0 °C", size=20, color="#ffab91")  # Orange 200
    humidity_text = ft.Text("💧 Humidity: 50.0 %", size=20, color="#90caf9")  # Blue 200

    led_switch = ft.Switch(
        label="💡 LED Override",
        on_change=led_toggle,
        active_color="#00b8d4",  # Cyan 400
        inactive_thumb_color="#bdbdbd",  # Grey 600
    )
    fan_switch = ft.Switch(
        label="🌀 Fan Override",
        on_change=fan_toggle,
        active_color="#ffb300",  # Amber 400
        inactive_thumb_color="#bdbdbd",  # Grey 600
    )

    fan_slider = ft.Slider(
        min=0,
        max=100,
        divisions=100,
        label="🌀 Fan Speed: {value}%",
        on_change=fan_speed_change,
        active_color="#ffa726",  # Amber 300
        inactive_color="#0d47a1",  # Blue 800
        thumb_color="#ffb300",  # Amber 600
    )

    # Arrange controls
    sensor_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("📊 Sensor Data", size=24, weight=ft.FontWeight.BOLD, color="#b2ebf2"),  # Cyan 300
                light_level_text,
                motion_text,
                temp_text,
                humidity_text
            ], spacing=10),
            padding=20,
            bgcolor="#0a2e5a",  # Blue 800
            border_radius=10
        ),
        elevation=5
    )

    control_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("🎮 Controls", size=24, weight=ft.FontWeight.BOLD, color="#b2ebf2"),  # Cyan 300
                led_switch,
                fan_switch,
                ft.Text("🌡️ Fan Speed Knob", size=18, color="#ffca28"),  # Amber 200
                fan_slider
            ], spacing=15),
            padding=20,
            bgcolor="#0a2e5a",  # Blue 800
            border_radius=10
        ),
        elevation=5
    )

    page.add(
        ft.Container(
            content=ft.Column([
                title,
                ft.Row([sensor_card, control_card], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            gradient=ft.LinearGradient(
                colors=["#0d47a1", "#006064"],  # Blue 900 to Cyan 900
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1)
            ),
            padding=20
        )
    )
    logger.debug("UI added to page")

    # Periodic refresh (1s)
    async def periodic_update():
        while True:
            logger.debug("Periodic update triggered")
            update_ui()
            await asyncio.sleep(1)

    page.run_task(periodic_update)
    logger.debug("Periodic update task started")

if __name__ == "__main__":
    ft.app(target=main)