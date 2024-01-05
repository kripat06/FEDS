import time
import board
import busio
import digitalio
import adafruit_vl53l1x
import pwmio
from adafruit_motor import motor
import adafruit_ssd1306

PWM_PIN_C = board.GP17  # pick any pwm pins on their own channels
PWM_PIN_D = board.GP16

PWM_PIN_A = board.GP14  # pick any pwm pins on their own channels
PWM_PIN_B = board.GP15

pwm_a = pwmio.PWMOut(PWM_PIN_A, frequency=50)
pwm_b = pwmio.PWMOut(PWM_PIN_B, frequency=50)
motor1 = motor.DCMotor(pwm_a, pwm_b) #Left Motor

pwm_c = pwmio.PWMOut(PWM_PIN_C, frequency=50)
pwm_d = pwmio.PWMOut(PWM_PIN_D, frequency=50)
motor2 = motor.DCMotor(pwm_c, pwm_d) #Right Motor

# Define the I2C pins.
i2c = busio.I2C(board.GP21, board.GP20)  # uses board.SCL and board.SDA
display_i2c = busio.I2C(board.GP7, board.GP6)

display = adafruit_ssd1306.SSD1306_I2C(128, 32, display_i2c)

motor2_offset = 0.15

xshut = [
    # Update the D6 and D5 pins to match the pins to which you wired your sensor XSHUT pins.
    digitalio.DigitalInOut(board.GP26),
    digitalio.DigitalInOut(board.GP27),
    # Add more VL53L1X sensors by defining their XSHUT pins here.
]

for shutdown_pin in xshut:
    # Set the shutdown pins to output, and pull them low.
    shutdown_pin.switch_to_output(value=False)
    # These pins are active when Low, meaning:
    #   If the output signal is LOW, then the VL53L1X sensor is off.
    #   If the output signal is HIGH, then the VL53L1X sensor is on.
# All VL53L1X sensors are now off.

# Create a list to be used for the array of VL53L1X sensors.
vl53l1x = []
# Change the address of the additional VL53L1X sensors.
for pin_number, shutdown_pin in enumerate(xshut):
    # Turn on the VL53L1X sensors to allow hardware check.
    shutdown_pin.value = True
    # Instantiate the VL53L1X I2C object and insert it into the vl53l1x list.
    # This also performs VL53L1X hardware check.
    sensor_i2c = adafruit_vl53l1x.VL53L1X(i2c)
    vl53l1x.append(sensor_i2c)
    # This ensures no address change on one sensor board, specifically the last one in the series.
    if pin_number < len(xshut) - 1:
        # The default address is 0x29. Update it to an address that is not already in use.
        sensor_i2c.set_address(pin_number + 0x30)

# Print the various sensor I2C addresses to the serial console.
if i2c.try_lock():
    print("Sensor I2C addresses:", [hex(x) for x in i2c.scan()])
    i2c.unlock()

# Start ranging for sensor data collection.
for sensor in vl53l1x:
    sensor.start_ranging()
    print("Started Ranging")

def start_motors():
    motor1.throttle = 0.7
    motor2.throttle = 0.85 #motor 2 offset is +0.15

def go_straight():
    distance_data = []
    for sensor_number, sensor in enumerate(vl53l1x):
        if sensor.data_ready:
            print("Sensor {}: {}".format(sensor_number + 1, sensor.distance))
            sensor.clear_interrupt()
            distance_data.append(sensor.distance)
            if sensor_number + 1 == 1:
                display.text('Front: {}'.format(str(sensor.distance)), 0, 0, 10)
            else:
                display.text('Back: {}'.format(str(sensor.distance)), 0, 10, 10)
    standard_speed = 0.7
    sensor1 = distance_data[1] #Front Sensor
    sensor2 = distance_data[0] #Back Sensor
    if sensor1 and sensor2 == 10.0:
        motor1.throttle = standard_speed
        motor2.throttle = standard_speed + motor2_offset
        display.text('Good', 0, 20, 10)
    elif sensor1 > 10:
        motor1.throttle = standard_speed - 0.2
        motor2.throttle = standard_speed + motor2_offset
        display.text('Right wheel fast', 0, 20, 10)
    elif sensor2 > 10:
        motor1.throttle = standard_speed
        motor2.throttle = standard_speed + motor2_offset - 0.2
        display.text('Left wheel fast', 0, 20, 10)
    display.show()

while True:
    display.fill(0)
    time.sleep(1)
    print("Started")
    go_straight()





