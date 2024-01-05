import time
import board
import pwmio
from adafruit_motor import motor
import busio
import digitalio
import adafruit_vl53l4cd
import math
import os
import ssl
import wifi
import socketpool
import microcontroller
import adafruit_requests
import neopixel
import json

num_pixels = 1

# Define the I2C pins.
i2c = busio.I2C(board.GP17, board.GP16)  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the buil t-in STEMMA QT connector on a microcontroller

xshut = [
    # Update the D6 and D5 pins to match the pins to which you wired your sensor XSHUT pins.
    digitalio.DigitalInOut(board.GP1),
    digitalio.DigitalInOut(board.GP18),
    digitalio.DigitalInOut(board.GP19),
    digitalio.DigitalInOut(board.GP21),
    digitalio.DigitalInOut(board.GP22),
    digitalio.DigitalInOut(board.GP27)
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
vl53l4cd = []

# Change the address of the additional VL53L1X sensors.
for pin_number, shutdown_pin in enumerate(xshut):
    # Turn on the VL53L1X sensors to allow hardware check.
    shutdown_pin.value = True
    # Instantiate the VL53L1X I2C object and insert it into the vl53l1x list.
    # This also performs VL53L1X hardware check.
    sensor_i2c = adafruit_vl53l4cd.VL53L4CD(i2c)
    sensor_i2c.timing_budget = 11 
    sensor_i2c.inter_measurement = 0
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

FRONT_L_SENSOR_IDX = 2
FRONT_R_SENSOR_IDX = 3
LEFT_F_SENSOR_IDX = 1
LEFT_B_SENSOR_IDX = 4
BACK_L_SENSOR_IDX = 5
BACK_R_SENSOR_IDX = 0

'''frontL = vl53l4cd[FRONT_L_SENSOR_IDX]
frontR = vl53l4cd[FRONT_R_SENSOR_IDX]
leftF = vl53l4cd[LEFT_F_SENSOR_IDX]
leftB = vl53l4cd[LEFT_B_SENSOR_IDX]
backL = vl53l4cd[BACK_L_SENSOR_IDX]
backR = vl53l4cd[BACK_R_SENSOR_IDX]'''

frontL = FRONT_L_SENSOR_IDX
frontR = FRONT_R_SENSOR_IDX
leftF = LEFT_F_SENSOR_IDX
leftB = LEFT_B_SENSOR_IDX
backL = BACK_L_SENSOR_IDX
backR = BACK_R_SENSOR_IDX


MOTOR_1_SLIDE_CALIB = 55000
MOTOR_2_CALIB = 38000
MOTOR_3_CALIB = 38000 #65535
MOTOR_4_CALIB = 45000

MOTOR_1_ST_CALIB = 45000
MOTOR_1_B_CALIB = 45000

#------------------------ MOTOR 4--------------------------
EN_PIN_4 = board.GP10
en_pin_4 = pwmio.PWMOut(EN_PIN_4)

PWM_PIN_G = board.GP3  
pwm_pin_g = pwmio.PWMOut(PWM_PIN_G)

PWM_PIN_H = board.GP2
pwm_pin_h = pwmio.PWMOut(PWM_PIN_H)

def go_straight_motor_4():
    pwm_pin_g.duty_cycle = 0
    pwm_pin_h.duty_cycle = 65535
    en_pin_4.duty_cycle = MOTOR_4_CALIB

def go_back_motor_4():
    pwm_pin_g.duty_cycle = 65535
    pwm_pin_h.duty_cycle = 0
    en_pin_4.duty_cycle = MOTOR_4_CALIB

#------------------------ MOTOR 3--------------------------
EN_PIN_3 = board.GP11
en_pin_3 = pwmio.PWMOut(EN_PIN_3)

PWM_PIN_E = board.GP4  
pwm_pin_e = pwmio.PWMOut(PWM_PIN_E)

PWM_PIN_F = board.GP5
pwm_pin_f = pwmio.PWMOut(PWM_PIN_F)

def go_straight_motor_3():
    pwm_pin_e.duty_cycle = 0
    pwm_pin_f.duty_cycle = 65535
    en_pin_3.duty_cycle = MOTOR_3_CALIB

def go_back_motor_3():
    pwm_pin_e.duty_cycle = 65535
    pwm_pin_f.duty_cycle = 0
    en_pin_3.duty_cycle = MOTOR_3_CALIB

#------------------------ MOTOR 2--------------------------
EN_PIN_2 = board.GP12
en_pin_2 = pwmio.PWMOut(EN_PIN_2)

PWM_PIN_C = board.GP6  
pwm_pin_c = pwmio.PWMOut(PWM_PIN_C)

PWM_PIN_D = board.GP7
pwm_pin_d = pwmio.PWMOut(PWM_PIN_D)

def go_straight_motor_2():
    pwm_pin_c.duty_cycle = 0
    pwm_pin_d.duty_cycle = 65535
    en_pin_2.duty_cycle = MOTOR_2_CALIB

def go_back_motor_2():
    pwm_pin_c.duty_cycle = 65535
    pwm_pin_d.duty_cycle = 0
    en_pin_2.duty_cycle = MOTOR_2_CALIB

#------------------------ MOTOR 1--------------------------
EN_PIN_1 = board.GP13
en_pin_1 = pwmio.PWMOut(EN_PIN_1)

PWM_PIN_A = board.GP8 
pwm_pin_a = pwmio.PWMOut(PWM_PIN_A)

PWM_PIN_B = board.GP9
pwm_pin_b = pwmio.PWMOut(PWM_PIN_B)


def slide_left():
    go_straight_motor_3()
    go_straight_motor_1()
    go_back_motor_2()
    go_back_motor_4()
    
def slide_right():
    go_back_motor_3()
    go_back_motor_1()
    go_straight_motor_2()
    go_straight_motor_4()


def go_straight_motor_1():
    pwm_pin_a.duty_cycle = 65535
    pwm_pin_b.duty_cycle = 0
    en_pin_1.duty_cycle = MOTOR_1_ST_CALIB

def go_back_motor_1():
    pwm_pin_a.duty_cycle = 0
    pwm_pin_b.duty_cycle = 65535
    en_pin_1.duty_cycle = MOTOR_1_B_CALIB

def drive_forward():
    go_straight_motor_1()
    go_straight_motor_2()
    go_straight_motor_3()
    go_straight_motor_4()

def drive_backward():
    go_back_motor_1()
    go_back_motor_2()
    go_back_motor_3()
    go_back_motor_4()

def slide_left_5mm():
    slide_left()
    time.sleep(0.02)
    brake()

def slide_right_5mm():
    slide_right()
    time.sleep(0.02)
    brake()

def go_straight_motor_1():
    pwm_pin_a.duty_cycle = 65535
    pwm_pin_b.duty_cycle = 0
    en_pin_1.duty_cycle = MOTOR_1_ST_CALIB

def go_back_motor_1():
    pwm_pin_a.duty_cycle = 0
    pwm_pin_b.duty_cycle = 65535
    en_pin_1.duty_cycle = MOTOR_1_B_CALIB

def get_distance(sensorIndex):
    distance = -1
    sensor = vl53l4cd[sensorIndex]
    time.sleep(0.005)
    if sensor.distance != None:
        try:
            distance = sensor.distance
            sensor.clear_interrupt()
        except OSError as ose:
            distance = -1
            print("---------OSE------------")
        except Exception as e:
            distance = -1
            print("----------E-----------")
    return distance

def get_average_distance(sensor):
    d1 = conditional_retry(get_distance(sensor), sensor)
    time.sleep(0.001)
    d2 = conditional_retry(get_distance(sensor), sensor)
    time.sleep(0.001)
    d3 = conditional_retry(get_distance(sensor), sensor)
    time.sleep(0.001)
    d4 = conditional_retry(get_distance(sensor), sensor)
    time.sleep(0.001)
    d5 = conditional_retry(get_distance(sensor), sensor)
    count = 5;
    if d1 < 0:
        d1 = 0
        count = count - 1
    elif d2 < 0:
        d2 = 0
        count = count - 1
    elif d3 < 0:
        d3 = 0
        count = count - 1
    elif d4 < 0:
        d4 = 0
        count = count - 1
    elif d5 < 0:
        d5 = 0
        count = count - 1
        
    d = (d1 + d2 + d3 + d4 + d5) / count
    return round(d,3)

def conditional_retry(distance, sensor):
    if distance < 0:
        time.sleep(0.005)
        distance = get_distance(sensor)
    return distance

def stop(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 0
    pwm_b.duty_cycle = 0
    en.duty_cycle = 65535
    
def brake():
    stop(pwm_pin_a, pwm_pin_b, en_pin_1)
    stop(pwm_pin_c, pwm_pin_d, en_pin_2)
    stop(pwm_pin_e, pwm_pin_f, en_pin_3)
    stop(pwm_pin_g, pwm_pin_h, en_pin_4)

def ccw():
    go_straight_motor_1()
    go_back_motor_2()
    go_back_motor_3()
    go_straight_motor_4()

    
def cw():
    go_back_motor_1()
    go_straight_motor_2()
    go_straight_motor_3()
    go_back_motor_4()

def ccw_5_deg():
    ccw()
    time.sleep(0.02)
    brake()
def cw_5_deg():
    cw()
    time.sleep(0.02)
    brake()

def side_self_correct(ERROR):
    F = get_average_distance(leftF)
    B = get_average_distance(leftB)
    print("START:" "F: " + str(F) + " B: " + str(B))
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
                F = get_average_distance(leftF)
                B = get_average_distance(leftB)
    elif F > B:
        #print("F > B")
        while not positioned:
            delta = F - B
            if delta < ERROR:
                positioned = True
                print("F > B delta= " + str(delta))
            else:
                ccw_5_deg()
                F = get_average_distance(leftF)
                B = get_average_distance(leftB)
    F = get_average_distance(leftF)
    B = get_average_distance(leftB)
    print("END:" "F: " + str(F) + " B: " + str(B))

def front_self_correct(ERROR):
    L = get_average_distance(frontL)
    R = get_average_distance(frontR)
    print("START:" "L: " + str(L) + " R: " + str(R))
    positioned = False
    if L > R:
        #print("F > B")
        while not positioned:
            delta = L - R
            if delta <= ERROR:
                positioned = True
                print("B > F delta= " + str(delta))

            else:
                cw_5_deg()
                L= get_average_distance(frontL)
                R = get_average_distance(frontR)
    elif R > L:
        #print("F > B")
        while not positioned:
            delta = R - L
            if delta < ERROR:
                positioned = True
                print("F > B delta= " + str(delta))
            else:
                ccw_5_deg()
                L= get_average_distance(frontL)
                R = get_average_distance(frontR)
    L = get_average_distance(frontL)
    R = get_average_distance(frontR)
    print("END:" "L: " + str(L) + " R: " + str(R))

def back_self_correct(ERROR):
    L = get_average_distance(backL)
    R = get_average_distance(backR)
    print("START:" "L: " + str(L) + " R: " + str(R))
    positioned = False
    if L > R:
        #print("F > B")
        while not positioned:
            delta = L - R
            if delta <= ERROR:
                positioned = True
                print("B > F delta= " + str(delta))

            else:
                ccw_5_deg()
                L= get_average_distance(backL)
                R = get_average_distance(backR)
    elif R > L:
        #print("F > B")
        while not positioned:
            delta = R - L
            if delta < ERROR:
                positioned = True
                print("F > B delta= " + str(delta))
            else:
                cw_5_deg()
                L= get_average_distance(backL)
                R = get_average_distance(backR)
    L = get_average_distance(backL)
    R = get_average_distance(backR)
    print("END:" "L: " + str(L) + " R: " + str(R))

def lateral_self_correct(DISTANCE):
    print("----------LATERAL-----------")
    aligned = False
    B = get_average_distance(leftB)
    if B > DISTANCE:
        slide_left_5mm()
        while not aligned:
            if B >= DISTANCE:
                B = get_average_distance(leftB)
                slide_left_5mm()
            else:
                aligned = True
                brake()
            
    elif B < DISTANCE:
        slide_right_5mm()
        while not aligned:
            if B <= DISTANCE:
                B = get_average_distance(leftB)
                slide_right_5mm()
            else:
                aligned = True
                brake()

    else:
        print("aligned")
    B = get_average_distance(leftB)



def go_north(stop_distance):
    reached = False
    current_distance = get_average_distance(frontL)
    drive_forward()                
    while not reached:
        if current_distance <= stop_distance:
            brake()
            reached = True
            current_distance = get_distance(frontL)
            #print("FINAL CD: "+str(current_distance) + " ")
        else:
            current_distance = get_distance(frontL)
            #print("North CD: "+str(current_distance) + " ")

def go_east(stop_distance):
    reached = False
    current_distance = get_average_distance(leftB)
    slide_right()                
    while not reached:
        if current_distance >= stop_distance:
            brake()
            reached = True
            #print("North CD: "+str(current_distance) + " ")
        else:
            current_distance = get_average_distance(leftB)
            #print("North CD: "+str(current_distance) + " ")
        time.sleep(0.01)

def go_west(stop_distance):
    reached = False
    current_distance = get_average_distance(leftB)
    slide_left()                
    while not reached:
        if current_distance <= stop_distance:
            brake()
            reached = True
            #print("North CD: "+str(current_distance) + " ")
        else:
            current_distance = get_average_distance(leftB)
            #print("North CD: "+str(current_distance) + " ")
        time.sleep(0.01)

def go_south_front_sensor(stop_distance):
    reached = False
    current_distance = get_average_distance(frontL)
    drive_backward()                
    while not reached:
        if current_distance >= stop_distance:
            brake()
            reached = True
            #print("North CD: "+str(current_distance) + " ")
        else:
            current_distance = get_average_distance(frontL)
            #print("North CD: "+str(current_distance) + " ")

def go_south_back_sensor(stop_distance):
    reached = False
    current_distance = get_average_distance(backL)
    drive_backward()                
    while not reached:
        if current_distance <= stop_distance:
            brake()
            reached = True
            #print("North CD: "+str(current_distance) + " ")
        else:
            current_distance = get_average_distance(backL)
            #print("North CD: "+str(current_distance) + " ")
        time.sleep(0.01)

NUM_PIXELS = 1
pixels = neopixel.NeoPixel(board.GP15, NUM_PIXELS, brightness=0.1, auto_write=False)

GREEN = (255, 0, 0)
YELLOW = (255, 150, 0)
RED = (0, 255, 0)
RESET = (0, 0, 0)

esp32 = digitalio.DigitalInOut(board.GP14)
esp32.direction = digitalio.Direction.OUTPUT


check_ready_url = "https://yvlxqeprd7.execute-api.us-west-2.amazonaws.com/dev-feds-upload-api/check-ready"
check_picture_url = "https://yvlxqeprd7.execute-api.us-west-2.amazonaws.com/dev-feds-upload-api/check-upload"

#  connect to SSID
wifi.radio.connect("ORBI12", "sweetoboe525")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

def take_picture():
    color_chase(YELLOW, 0.1)  # Increase the number to slow down the color chase
    esp32.value = True
    time.sleep(0.5)
    esp32.value = False
    uploaded = False
    while not uploaded:
        upload = check_for_picture_upload()
        if upload == True:
            uploaded = False
            break
        else:
            time.sleep(1)
            
def check_for_picture_upload():
    ready = False
    while not ready:
        #  run adafruit quotes
        print("Fetching text from %s" % check_picture_url)
        #  gets the quote from adafruit quotes
        response = requests.get(check_picture_url)
        #  prints the response to the REPL
        print("Text Response: ", response.text)
        if response.text == "True":
            color_chase(GREEN, 0.1)  # Increase the number to slow down the color chase
            ready = True
            break
        else:
            color_chase(RESET, 0.5)  # Increase the number to slow down the color chase
        response.close()
        time.sleep(1)
    return ready

def wait_for_ready():
    ready = False
    while not ready:
        response = requests.get(check_ready_url)
        if response.text== "True":
            color_chase(GREEN, 0.1)  # Increase the number to slow down the color chase
            ready = True
            break
        else:
            color_chase(RESET, 0.5)  # Increase the number to slow down the color chase
        response.close()            
        time.sleep(3)
    return ready

navigation_state_url = "https://yvx6t8lrvg.execute-api.us-west-1.amazonaws.com/dev/api/navigationstate"

def check_navigation_status():
    ready = False
    while not ready:
        print("Fetching state from %s" % navigation_state_url)
        response = requests.get(navigation_state_url)
        response_as_json = response.json()
        response.close()
        print("State Response: ", response_as_json["navigate_flag"])
        ready = response_as_json["navigate_flag"]
        time.sleep(1)
    return ready

headers = {
    'Content-Type': 'application/json'
}

def mark_navigation_complete():
    payload = json.dumps({"id":1 , "navigate_flag":False})
    print(payload)
    response = requests.post(navigation_state_url, headers=headers, data=payload)
    response.close()

#esp32.value = False
wait_for_ready()
esp32_ready = True
running = True
if esp32_ready == True:
    while running:
        navigation_state = check_navigation_status()
        if navigation_state == True:
            go_north(33)
            take_picture()
            
            go_north(21)
            take_picture()
            
            go_north(7)
            front_self_correct(0.1)
            take_picture()
            
            go_east(18)
            side_self_correct(0.1)
            front_self_correct(0.1)
            take_picture()

            go_south_front_sensor(16)
            side_self_correct(0.1)
            time.sleep(1)
            take_picture()

            go_south_front_sensor(30)
            side_self_correct(0.1)
            time.sleep(1)
            take_picture()

            go_east(31)
            front_self_correct(0.1)
            lateral_self_correct(31)
            time.sleep(1)
            take_picture()

            go_north(21)
            side_self_correct(0.1)
            back_self_correct(0.1)
            time.sleep(1)
            take_picture()

            go_north(7)
            front_self_correct(0.1)
            side_self_correct(0.1)
            lateral_self_correct(31)
            time.sleep(1)
            take_picture()

            go_east(44)
            front_self_correct(0.1)
            lateral_self_correct(43)
            time.sleep(1)
            take_picture()

            go_south_front_sensor(17)
            back_self_correct(0.1)
            time.sleep(1)
            take_picture()

            go_south_front_sensor(30)
            back_self_correct(0.1)
            time.sleep(1)
            take_picture()

            go_south_front_sensor(44)
            back_self_correct(0.1)
            time.sleep(1)

            go_west(5)
            back_self_correct(0.1)
            lateral_self_correct(5)
            side_self_correct(0.1)
            
            mark_navigation_complete()
            