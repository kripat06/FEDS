import time
import board
import pwmio
from adafruit_motor import motor
import busio
import digitalio
import adafruit_vl53l4cd
import adafruit_ssd1306
import math

# ------------------------ MOTOR 4--------------------------
EN_PIN_4 = board.GP10
en_pin_4 = pwmio.PWMOut(EN_PIN_4)

PWM_PIN_G = board.GP3
pwm_pin_g = pwmio.PWMOut(PWM_PIN_G)

PWM_PIN_H = board.GP2
pwm_pin_h = pwmio.PWMOut(PWM_PIN_H)

# ------------------------ MOTOR 3--------------------------
EN_PIN_3 = board.GP11
en_pin_3 = pwmio.PWMOut(EN_PIN_3)

PWM_PIN_E = board.GP4
pwm_pin_e = pwmio.PWMOut(PWM_PIN_E)

PWM_PIN_F = board.GP5
pwm_pin_f = pwmio.PWMOut(PWM_PIN_F)

# ------------------------ MOTOR 2--------------------------
EN_PIN_2 = board.GP14
en_pin_2 = pwmio.PWMOut(EN_PIN_2)

PWM_PIN_C = board.GP6
pwm_pin_c = pwmio.PWMOut(PWM_PIN_C)

PWM_PIN_D = board.GP7
pwm_pin_d = pwmio.PWMOut(PWM_PIN_D)

# ------------------------ MOTOR 1--------------------------
EN_PIN_1 = board.GP15
en_pin_1 = pwmio.PWMOut(EN_PIN_1)

PWM_PIN_A = board.GP8
pwm_pin_a = pwmio.PWMOut(PWM_PIN_A)

PWM_PIN_B = board.GP9
pwm_pin_b = pwmio.PWMOut(PWM_PIN_B)

# -----------------DISPLAY INIT-----------------------------
display_i2c = busio.I2C(board.GP27, board.GP26)

display = adafruit_ssd1306.SSD1306_I2C(128, 32, display_i2c)

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

display.rotate(False)  # rotate 180 degrees
# -----------------------------------------------
DIST_BTWN_SENSOR = 9.5

LEFT1_SENSOR_IDX = 2
LEFT2_SENSOR_IDX = 0


def go_back(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 65535
    pwm_b.duty_cycle = 0
    en.duty_cycle = 49151


def go_straight(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 0
    pwm_b.duty_cycle = 65535
    en.duty_cycle = 49151


def go_straight_slow(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 0
    pwm_b.duty_cycle = 65535
    en.duty_cycle = 40000


def go_back_slow(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 65535
    pwm_b.duty_cycle = 0
    en.duty_cycle = 40000


def stop(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 0
    pwm_b.duty_cycle = 0
    en.duty_cycle = 65535


def slide_right():
    go_back(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_back(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_g, pwm_pin_h, en_pin_4)


def slide_left():
    go_back(pwm_pin_g, pwm_pin_h, en_pin_4)
    go_back(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight(pwm_pin_a, pwm_pin_b, en_pin_1)


def brake():
    stop(pwm_pin_a, pwm_pin_b, en_pin_1)
    stop(pwm_pin_c, pwm_pin_d, en_pin_2)
    stop(pwm_pin_e, pwm_pin_f, en_pin_3)
    stop(pwm_pin_g, pwm_pin_h, en_pin_4)


def drive_back():
    go_back(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_back(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_back(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_back(pwm_pin_g, pwm_pin_h, en_pin_4)


def drive_forward():
    go_straight(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight(pwm_pin_g, pwm_pin_h, en_pin_4)


def drive_diagonal_right():
    go_straight(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight(pwm_pin_e, pwm_pin_f, en_pin_3)


def drive_diagonal_left():
    go_straight(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_g, pwm_pin_h, en_pin_4)


def left_pivot():
    go_back(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_back(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight(pwm_pin_g, pwm_pin_h, en_pin_4)


def right_pivot():
    go_straight(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_back(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_back(pwm_pin_g, pwm_pin_h, en_pin_4)


def setup_display():
    display.fill(1)
    display.show()
    time.sleep(2)
    display.fill(0)
    display.show()


def left_pivot():
    go_straight_full(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_back_full(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_back_full(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight_full(pwm_pin_g, pwm_pin_h, en_pin_4)


def right_pivot():
    go_back_slow(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight_slow(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight_slow(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_back_slow(pwm_pin_g, pwm_pin_h, en_pin_4)


def cw_5_deg():
    go_straight_slow(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_back_slow(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_back_slow(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight_slow(pwm_pin_g, pwm_pin_h, en_pin_4)
    time.sleep(0.2)
    brake()


def ccw_5_deg():
    go_back_slow(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight_slow(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight_slow(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_back_slow(pwm_pin_g, pwm_pin_h, en_pin_4)
    time.sleep(0.2)
    brake()


def self_correct(target):
    target = target * 10
    left1_distance = get_distance(LEFT1_SENSOR_IDX) * 10
    left2_distance = get_distance(LEFT2_SENSOR_IDX) * 10
    positioned = False
    if left1_distance > left2_distance:
        print("L1 > L2")
        while not positioned:
            if left1_distance in range(target - 30, target + 30) and left2_distance in range(target - 30, target + 30):
                brake()
                print("Posiitoned")
                positioned = True
            else:
                cw_5_deg()
                left1_distance = get_distance(LEFT1_SENSOR_IDX) * 10
                left2_distance = get_distance(LEFT2_SENSOR_IDX) * 10
                print("L1 " + str(left1_distance) + "    " + "L2 " + str(left2_distance))
            time.sleep(0.3)
    if left1_distance < left2_distance:
        print("L2 > L1")
        while not positioned:
            if left1_distance in range(target - 30, target + 30) and left2_distance in range(target - 30, target + 30):
                brake()
                print("Posiitoned")
                positioned = True
            else:
                ccw_5_deg()
                left1_distance = get_distance(LEFT1_SENSOR_IDX) * 10
                left2_distance = get_distance(LEFT2_SENSOR_IDX) * 10
                print("L1 " + str(left1_distance) + "    " + "L2 " + str(left2_distance))
            time.sleep(0.3)


def get_distance(sensorIndex):
    sensor = vl53l4cd[sensorIndex]
    distance = -1
    if sensor.distance != None:
        distance = sensor.distance
    sensor.clear_interrupt()
    return distance


setup_display()
FRONT_SENSOR_IDX = 1
front_distance = get_distance(FRONT_SENSOR_IDX)
reached = False
drive_forward()
while not reached:
    if front_distance <= 20:
        brake()
        display.fill(0)
        display.text("B at: " + str(front_distance), 0, 10, 10)
        print("B at: " + str(front_distance))
        display.show()
        reached = True
    else:
        front_distance = get_distance(FRONT_SENSOR_IDX)
        display.show()

go_right = False

left1_distance = get_distance(LEFT1_SENSOR_IDX)
left2_distance = get_distance(LEFT2_SENSOR_IDX)
slide_right()
while not go_right:
    if left1_distance and left2_distance >= 18:
        brake()
        display.fill(0)
        display.text("B at: " + str(left1_distance), 0, 10, 10)
        display.text("    : " + str(left2_distance), 0, 20, 10)
        print("B at: " + str(left1_distance), " " + str(left2_distance))
        display.show()
        go_right = True
    else:
        left1_distance = get_distance(LEFT1_SENSOR_IDX)
        left2_distance = get_distance(LEFT2_SENSOR_IDX)
        display.show()
self_correct(20)

'''        
def find_angle(a):
    c = math.sqrt(a + math.pow(DIST_BTWN_SENSOR,2))
    print("a = "  + str(a) )
    print("c = "+ str(c))
    angle = math.acos(a/c)
    print(str(angle))
    return angle

def self_correct():
    left1_distance = get_distance(LEFT1_SENSOR_IDX)
    left2_distance = get_distance(LEFT2_SENSOR_IDX)

    if left1_distance > left2_distance:
        angle = 90 - find_angle(left1_distance)
        print(str(angle))
        in_position = False
        while not in_position:
            left1_distance = get_distance(LEFT1_SENSOR_IDX)
            angle = 90 - find_angle(left1_distance)
            print(str(angle))
            if angle > 0:
                left_pivot()
                time.sleep(0.05)
            else:
                brake()
                in_position = True
    if left1_distance < left2_distance:
        angle = 90 - find_angle(left2_distance)
        print(str(angle))
        in_position = False
        while not in_position:
            left2_distance = get_distance(LEFT2_SENSOR_IDX)
            angle = 90 - find_angle(left2_distance)
            print(str(angle))
            if angle > 0:
                right_pivot()
                time.sleep(0.05)
            else:
                brake()
                in_position = True         
    else:
        display.text("Adjusted", 0, 10, 10)
        print("Adjusted")
    '''
