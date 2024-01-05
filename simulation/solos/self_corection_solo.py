import time
import board
import pwmio
from adafruit_motor import motor
import busio
import digitalio
import adafruit_vl53l4cd
import adafruit_ssd1306
import math

#------------------------ MOTOR 4--------------------------
EN_PIN_4 = board.GP10
en_pin_4 = pwmio.PWMOut(EN_PIN_4)

PWM_PIN_G = board.GP3  
pwm_pin_g = pwmio.PWMOut(PWM_PIN_G)

PWM_PIN_H = board.GP2
pwm_pin_h = pwmio.PWMOut(PWM_PIN_H)

#------------------------ MOTOR 3--------------------------
EN_PIN_3 = board.GP11
en_pin_3 = pwmio.PWMOut(EN_PIN_3)

PWM_PIN_E = board.GP4  
pwm_pin_e = pwmio.PWMOut(PWM_PIN_E)

PWM_PIN_F = board.GP5
pwm_pin_f = pwmio.PWMOut(PWM_PIN_F)

#------------------------ MOTOR 2--------------------------
EN_PIN_2 = board.GP14
en_pin_2 = pwmio.PWMOut(EN_PIN_2)

PWM_PIN_C = board.GP6  
pwm_pin_c = pwmio.PWMOut(PWM_PIN_C)

PWM_PIN_D = board.GP7
pwm_pin_d = pwmio.PWMOut(PWM_PIN_D)

#------------------------ MOTOR 1--------------------------
EN_PIN_1 = board.GP15
en_pin_1 = pwmio.PWMOut(EN_PIN_1)

PWM_PIN_A = board.GP8 
pwm_pin_a = pwmio.PWMOut(PWM_PIN_A)

PWM_PIN_B = board.GP9
pwm_pin_b = pwmio.PWMOut(PWM_PIN_B)

#-----------------DISPLAY INIT-----------------------------
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
    
display.rotate(False)   # rotate 180 degrees
#-----------------------------------------------

LEFT_F_SENSOR_IDX = 2
LEFT_B_SENSOR_IDX = 0
FRONT_SENSOR_IDX = 1

def go_back(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 65535
    pwm_b.duty_cycle = 0
    en.duty_cycle = 40000

def go_straight(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 0
    pwm_b.duty_cycle = 65535
    en.duty_cycle = 40000
    
def go_straight_slow(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 0
    pwm_b.duty_cycle = 65535
    en.duty_cycle = 30000
    
def go_back_slow(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 65535
    pwm_b.duty_cycle = 0
    en.duty_cycle = 30000
    
def go_back_fast(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 65535
    pwm_b.duty_cycle = 0
    en.duty_cycle = 45000

def go_straight_fast(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 0
    pwm_b.duty_cycle = 65535
    en.duty_cycle = 45000
    
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
    go_straight(pwm_pin_g, pwm_pin_h, en_pin_4)
    go_straight(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_a, pwm_pin_b, en_pin_1)
    
def drive_diagonal_right():
    go_straight(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight(pwm_pin_e, pwm_pin_f, en_pin_3)
    
def drive_diagonal_left():
    go_straight(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_g, pwm_pin_h, en_pin_4)
    
def setup_display():
    display.fill(1)
    display.show()
    time.sleep(2)
    display.fill(0)
    display.show()
    
def cw():
    go_straight(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_back(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_back(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight(pwm_pin_g, pwm_pin_h, en_pin_4)

    
def ccw():
    go_back(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_back(pwm_pin_g, pwm_pin_h, en_pin_4)
    
def ccw_5_deg():
    go_straight(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_back(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_back(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight(pwm_pin_g, pwm_pin_h, en_pin_4)
    time.sleep(0.015)
    brake()
    
def cw_5_deg():
    go_back(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_straight(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_back(pwm_pin_g, pwm_pin_h, en_pin_4)
    time.sleep(0.015)
    brake()
    
def slide_left_5mm():
    slide_left()
    time.sleep(0.02)
    brake()
    
def slide_right_5mm():
    slide_right()
    time.sleep(0.02)
    brake()
    
def drive_back_5mm():
    go_back_slow(pwm_pin_a, pwm_pin_b, en_pin_1)
    go_back_slow(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_back_slow(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_back_slow(pwm_pin_g, pwm_pin_h, en_pin_4)
    time.sleep(0.05)
    brake()
    
def drive_forward_5mm():
    go_straight_slow(pwm_pin_g, pwm_pin_h, en_pin_4)
    go_straight_slow(pwm_pin_e, pwm_pin_f, en_pin_3)
    go_straight_slow(pwm_pin_c, pwm_pin_d, en_pin_2)
    go_straight_slow(pwm_pin_a, pwm_pin_b, en_pin_1)
    time.sleep(0.05)
    brake()
    
def get_distance(sensorIndex):
    sensor = vl53l4cd[sensorIndex]
    distance = -1
    if sensor.distance != None:
        distance = sensor.distance
    sensor.clear_interrupt()
    return distance

def get_average_distance(sensorIndex):
    d1 = get_distance(sensorIndex)
    d2 = get_distance(sensorIndex)
    d3 = get_distance(sensorIndex)
    d4 = get_distance(sensorIndex)
    d5 = get_distance(sensorIndex)
    d = (d1 + d2 + d3 + d4 + d5) / 5
    return round(d,3)

def fix_error_prone(OFFSET):
    F = get_average_distance(LEFT_F_SENSOR_IDX)
    B = get_average_distance(LEFT_B_SENSOR_IDX)
    positioned = False
    while not positioned:
        delta = B - F
        if abs(delta) <= OFFSET:
            positioned = True
            print("B > F delta= " + str(delta))

        else:
            ccw_5_deg()
            F = get_average_distance(LEFT_F_SENSOR_IDX)
            B = get_average_distance(LEFT_B_SENSOR_IDX)

def self_correct(ERROR):
    F = get_average_distance(LEFT_F_SENSOR_IDX)
    B = get_average_distance(LEFT_B_SENSOR_IDX)
    T = get_average_distance(FRONT_SENSOR_IDX)
    print("START:" "F: " + str(F) + " B: " + str(B) + " T: " + str(T))
    positioned = False
    if B > F:
        #print("F > B")
        while not positioned:
            delta = B - F
            if delta <= ERROR:
                positioned = True
                print("B > F delta= " + str(delta))

            else:
                cw_5_deg()
                F = get_average_distance(LEFT_F_SENSOR_IDX)
                B = get_average_distance(LEFT_B_SENSOR_IDX)
    elif F > B:
        #print("F > B")
        while not positioned:
            delta = F - B
            if delta < ERROR:
                positioned = True
                print("F > B delta= " + str(delta))
            else:
                ccw_5_deg()
                F = get_average_distance(LEFT_F_SENSOR_IDX)
                B = get_average_distance(LEFT_B_SENSOR_IDX)
    F = get_average_distance(LEFT_F_SENSOR_IDX)
    B = get_average_distance(LEFT_B_SENSOR_IDX)
    T = get_average_distance(FRONT_SENSOR_IDX)
    print("END:" "F: " + str(F) + " B: " + str(B) + " T: " + str(T))

def rotational_B_more_F(F, B):
    while not positioned:
        delta = B - F
        if delta <= ERROR:
            positioned = True
            print("B > F delta= " + str(delta))

        else:
            cw_5_deg()
            F = get_average_distance(LEFT_F_SENSOR_IDX)
            B = get_average_distance(LEFT_B_SENSOR_IDX)
            
def rotational_F_more_B(F, B):
    #print("F > B")
    while not positioned:
        delta = F - B
        if delta < ERROR:
            positioned = True
            print("F > B delta= " + str(delta))
        else:
            ccw_5_deg()
            F = get_average_distance(LEFT_F_SENSOR_IDX)
            B = get_average_distance(LEFT_B_SENSOR_IDX)
            
def lateral_self_correct(ERROR, DISTANCE):
    print("----------LATERAL-----------")
    aligned = False
    B = get_average_distance(LEFT_B_SENSOR_IDX)
    if B > DISTANCE:
        slide_left_5mm()
        while not aligned:
            if B >= DISTANCE:
                B = get_average_distance(LEFT_B_SENSOR_IDX)
                slide_left_5mm()
            else:
                aligned = True
                time.sleep(0.1)

    elif B < DISTANCE:
        slide_right_5mm()
        while not aligned:
            if B <= DISTANCE:
                B = get_average_distance(LEFT_B_SENSOR_IDX)
                slide_right_5mm()
            else:
                aligned = True
                time.sleep(0.1)

    else:
        print("aligned")
    B = get_average_distance(LEFT_B_SENSOR_IDX)
    F = get_average_distance(LEFT_F_SENSOR_IDX)
    T = get_average_distance(FRONT_SENSOR_IDX)
    print("LATERALED:" "F: " + str(F) + " B: " + str(B) + " T: " + str(T))
    
def front_self_correct(ERROR, stop_distance):
    reached = False
    current_distance = get_distance(FRONT_SENSOR_IDX) + 1
    drive_forward()
    if current_distance > stop_distance:
        while not reached:
            if current_distance - stop_distance <= ERROR:
                brake()
                reached = True
                print("North CD: "+str(current_distance) + " ")
            else:
                drive_forward_5mm()
                current_distance = get_distance(FRONT_SENSOR_IDX) + 1
                #print("North CD: "+str(current_distance) + " ")
    elif stop_distance > current_distance:
        while not reached:
            if stop_distance - current_distance <= ERROR:
                brake()
                reached = True
                print("North CD: "+str(current_distance) + " ")
            else:
                drive_back_5mm()
                current_distance = get_distance(FRONT_SENSOR_IDX) + 1
                #print("North CD: "+str(current_distance) + " ")
            
setup_display()
'''self_correct(0.1)
self_correct(0.1)
lateral_self_correct(0.1, 18.75)
self_correct(0.1)
self_correct(0.1)



time.sleep(0.5)
self_correct(0.1, error_prone = True, OFFSET = 10)
self_correct(0.1)
self_correct(0.1)
front_self_correct(0.1, 5.5)
self_correct(0.1)
self_correct(0.1)
lateral_self_correct(0.1, 45)
lateral_self_correct(0.1, 45)
self_correct(0.1)
self_correct(0.1)'''
self_correct(0.1)
self_correct(0.1)
go_north(33)
self_correct(0.1)
self_correct(0.1)
lateral_self_correct(0.1, 5.5)
lateral_self_correct(0.1, 5.5)
self_correct(0.1)
self_correct(0.1)
