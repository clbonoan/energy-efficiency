import paho.mqtt.client as mqtt
import json
from datetime import datetime, timedelta

# MQTT settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "zigbee2mqtt/smart-plug"

# Tracking variables
last_timestamp = None
energy_kwh = 0.0
power_sum = 0.0
reading_count = 0
last_logged_power = None
last_log_time = None
log_interval = timedelta(seconds=5)  # Always log every 5 seconds

def on_message(client, userdata, message):
    global last_timestamp, energy_kwh, power_sum, reading_count
    global last_logged_power, last_log_time

    payload = message.payload.decode('utf-8')

    try:
        data = json.loads(payload)
        power = float(data.get('power', 0))
        voltage = data.get('voltage', 'N/A')
        current = data.get('current', 'N/A')
        timestamp = datetime.now()

        # Calculate energy
        if last_timestamp is not None:
            elapsed_seconds = (timestamp - last_timestamp).total_seconds()
            elapsed_hours = elapsed_seconds / 3600.0
            energy_kwh += (power * elapsed_hours) / 1000.0

        last_timestamp = timestamp
        power_sum += power
        reading_count += 1
        average_power = power_sum / reading_count

        should_log = False

        # Log if time interval has passed
        if last_log_time is None or (timestamp - last_log_time) >= log_interval:
            should_log = True

        # Or log if there's a significant power change
        if last_logged_power is None or abs(power - last_logged_power) > 0.1:
            should_log = True

        if should_log:
            log_line = (
                f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Power: {power:.2f} W, Voltage: {voltage} V, Current: {current} A, "
                f"Avg Power: {average_power:.2f} W, Est. Energy: {energy_kwh:.6f} kWh\n"
            )

            print(log_line.strip())

            with open("energy_log.txt", "a") as log_file:
                log_file.write(log_line)

            last_logged_power = power
            last_log_time = timestamp

    except Exception as e:
        print(f"Error processing the message: {e}")

# MQTT setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)

print("Listening for MQTT messages...")
client.loop_forever()

