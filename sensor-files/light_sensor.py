# module for light sensor

import smbus
import time

# BH1750 I2C address (default 0x23)
DEVICE = 0x23
# command to start continuous high-res mode
POWER_ON = 0x01
RESET = 0x07
CONT_H_RES_MODE = 0x10

# use I2C bus 1
bus = smbus.SMBus(1)

# initialize BH1750
bus.write_byte(DEVICE, POWER_ON)
bus.write_byte(DEVICE, RESET)
bus.write_byte(DEVICE, CONT_H_RES_MODE)

def read_lux():
    try: 
        data = bus.read_i2c_block_data(DEVICE, CONT_H_RES_MODE)
        light_level = (data[0] << 8) | data[1]  # convert to lux
        return light_level / 1.2    # BH1750 scaling factor
    except Exception as e:
        print(f"BH1750 read error: {e}")
        return None

def calculate_brightness(lux, min_lux=10.0, max_lux=15.0, min_brightness=15.0):
    # map raw lux to brightness (30 - 254)
    # map:
    # >= 50 -> 0 (OFF)
    # 13-50 -> scale brigtness from 254 (bright) down to min_brightness
    # <= 13 -> 254 (max brightness)
    if lux is None:
        return 0
    if lux >= max_lux:
        return 0    # room is bright enough
    elif lux <= min_lux:
        return 254  # room is dark -> full brightness
    else:
        # produce a value from 0 to 1 (represent how dark the room is)
        # if lux = 80 -> scale = 0 -> brightness = 0
        # if lux = 15 -> scale = 1 -> brightness = 254
        # if lux = 50 -> scale = 0.4615 -> brightness = 117
        scale = (max_lux - lux) / (max_lux - min_lux)
        # convert a normalized brightness scale (0 to 1) into range Philips hue uses
        # 0 (off) -> 254 (100% brightness)
        # map bulb brightnes (0 to 1) to (0 to 254)
        brightness = int(scale * (254 - min_brightness) + min_brightness)
        return brightness
