import serial

ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
ser.write(bytes.fromhex("FDFCFBFA0800120000006400000004030201"))

def get_mmwave_distance():
    # returns distance in cm from mmwave sensor output line
    # returns None if data is invalid or not parseable
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print("Raw Data:", line)

        if line.startswith("Range"):
            distance_cm = int(line.split("Range")[1].strip())
            print(f"Distance detected: ({distance_cm} cm)")
            return distance_cm
    except Exception as e:
        print("Error parsing distance:", e)
    return None
