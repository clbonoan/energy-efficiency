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
