import time
import board
import busio
import digitalio
import adafruit_vl53l4cd

i2c = busio.I2C(board.GP17, board.GP16) 

xshut = [
    digitalio.DigitalInOut(board.GP18),
    digitalio.DigitalInOut(board.GP19),
    digitalio.DigitalInOut(board.GP20)
]

for shutdown_pin in xshut:
    shutdown_pin.switch_to_output(value=False)

# Create a list to be used for the array of VL53L1X sensors.
vl53l4cd = []

# Change the address of the additional VL53L1X sensors.
for pin_number, shutdown_pin in enumerate(xshut):
    # Turn on the VL53L1X sensors to allow hardware check.
    shutdown_pin.value = True
    # Instantiate the VL53L1X I2C object and insert it into the vl53l1x list.
    # This also performs VL53L1X hardware check.
    sensor_i2c = adafruit_vl53l4cd.VL53L4CD(i2c)
    vl53l4cd.append(sensor_i2c)
    # This ensures no address change on one sensor board, specifically the last one in the series.
    if pin_number < len(xshut) - 1:
        # The default address is 0x29. Update it to an address that is not already in use.
        sensor_i2c.set_address(pin_number + 0x30)

# Print the various sensor I2C addresses to the serial console.
if i2c.try_lock():
    print("Sensor I2C addresses:", [hex(x) for x in i2c.scan()])
    i2c.unlock()

# Start ranging for sensor data collection.
for sensor in vl53l4cd:
    sensor.start_ranging()
#-----------------------------------------------

LEFT_F_SENSOR_IDX = 2
LEFT_B_SENSOR_IDX = 0
FRONT_SENSOR_IDX = 1

def get_distance(sensorIndex):
    sensor = vl53l4cd[sensorIndex]
    distance = -1
    if sensor.distance != None:
        distance = sensor.distance
    sensor.clear_interrupt()
    return distance

while True:
    F = get_distance(LEFT_F_SENSOR_IDX)
    B = get_distance(LEFT_B_SENSOR_IDX)
    T = get_distance(FRONT_SENSOR_IDX)
    print("F: " + str(F) + " " + "B: " + str(B) + " " + "T: " + str(T))
    time.sleep(1)

