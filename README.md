# Smart Bulb Energy Saver with Raspberry Pi and Python

This project reduces energy waste by automating a smart bulb using a Raspberry Pi and Python. By combining motion detection, presence sensing, and ambient light measurement, 
the system intelligently controls lighting based on real-time room conditions.

## Features

- Automated smart bulb control via Python scripts
- Motion detection using PIR and mmWave sensors
- Ambient light measurement using BH1750 lux sensor
- Zigbee2MQTT integration with a Sonoff Zigbee 3.0 USB dongle
- Local control — no cloud services required
- Energy-efficient lighting based on presence and brightness

## Hardware Requirements

- Raspberry Pi 4 Model B
- Philips Hue Smart Bulb (or Zigbee-compatible bulb)
- Sonoff Zigbee 3.0 USB Dongle Plus (ZBDongle-E)
- PIR Motion Sensor
- mmWave Presence Sensor
- BH1750 Light Sensor (I2C)
- Breadboard, jumper wires, heatsink and fan, and light socket adapter

## Software Requirements

- Python 3.11.2
- MQTT broker (e.g., Mosquitto)
- Required Python libraries:
  - `paho-mqtt`
  - `time`
 
Install dependencies:

```bash
pip install paho-mqtt
