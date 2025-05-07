import subprocess

def turn_on():
    subprocess.run([
        "mosquitto_pub", "-h", "localhost",
        "-t", "zigbee2mqtt/hue-bulb/set",
        "-m", '{"state": "ON"}'
        ])
    print("Bulb ON")

def turn_off():
    subprocess.run([
        "mosquitto_pub", "-h", "localhost",
        "-t", "zigbee2mqtt/hue-bulb/set",
        "-m", '{"state": "OFF"}'
        ])
    print("Bulb OFF")

def set_bulb_brightness(brightness):
    # brightness should be in range 0-254
    payload = f'{{"state": "ON", "brightness": {brightness}}}'
    subprocess.run([
        "mosquitto_pub", "-h", "localhost",
        "-t", "zigbee2mqtt/hue-bulb/set",
        "-m", payload
    ])
    print(f"Bulb brightness set to {brightness}")
