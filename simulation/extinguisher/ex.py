# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example uses an L9110 H-bridge driver to run a DC Motor using two PWM pins.
#  https://www.adafruit.com/product/4489

# Hardware setup:
#   DC motor via L9110 H-bridge driver on two PWM pins that are on their own channels
#   e.g., RP2040 Pico pins GP28, GP27

import time
import board
import pwmio
from adafruit_motor import motor
import busio
import digitalio
import adafruit_vl53l4cd
#import adafruit_ssd1306
import math


import time
import board
import pwmio
import busio
import digitalio
import adafruit_vl53l4cd
import math
import os

# Define the I2C pins.
i2c = busio.I2C(board.GP17, board.GP16)  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the buil t-in STEMMA QT connector on a microcontroller

xshut = [
    # Update the D6 and D5 pins to match the pins to which you wired your sensor XSHUT pins.
    digitalio.DigitalInOut(board.GP18),
    digitalio.DigitalInOut(board.GP19),
    digitalio.DigitalInOut(board.GP20),
    digitalio.DigitalInOut(board.GP21),
    digitalio.DigitalInOut(board.GP27),
    digitalio.DigitalInOut(board.GP26)
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
    
#Calibration is decent
MOTOR_1_SLIDE_CALIB = 55000
MOTOR_2_CALIB = 38000
MOTOR_3_CALIB = 38000 #65535
MOTOR_4_CALIB = 38000

MOTOR_1_ST_CALIB = 40000
MOTOR_1_B_CALIB = 40000

FRONT_L_SENSOR_IDX = 6
FRONT_R_SENSOR_IDX = 3
RIGHT_F_SENSOR_IDX = 4
RIGHT_B_SENSOR_IDX = 1
BACK_L_SENSOR_IDX = 5
BACK_R_SENSOR_IDX = 2

frontL = FRONT_L_SENSOR_IDX - 1 #So it has right index (1->0, 2->1, 3->2, etc.)
frontR = FRONT_R_SENSOR_IDX - 1 
rightF = RIGHT_F_SENSOR_IDX - 1 
rightB = RIGHT_B_SENSOR_IDX - 1
backL = BACK_L_SENSOR_IDX - 1
backR = BACK_R_SENSOR_IDX - 1 

#------------------------ MOTOR 4--------------------------
EN_PIN_4 = board.GP10
en_pin_4 = pwmio.PWMOut(EN_PIN_4)

PWM_PIN_G = board.GP3  
pwm_pin_g = pwmio.PWMOut(PWM_PIN_G)

PWM_PIN_H = board.GP2
pwm_pin_h = pwmio.PWMOut(PWM_PIN_H)

def go_straight_motor_4():
    pwm_pin_g.duty_cycle = 65535
    pwm_pin_h.duty_cycle = 0
    en_pin_4.duty_cycle = MOTOR_4_CALIB

def go_back_motor_4():
    pwm_pin_g.duty_cycle = 0
    pwm_pin_h.duty_cycle = 65535
    en_pin_4.duty_cycle = MOTOR_4_CALIB

#------------------------ MOTOR 3--------------------------
EN_PIN_3 = board.GP11
en_pin_3 = pwmio.PWMOut(EN_PIN_3)

PWM_PIN_E = board.GP4  
pwm_pin_e = pwmio.PWMOut(PWM_PIN_E)

PWM_PIN_F = board.GP5
pwm_pin_f = pwmio.PWMOut(PWM_PIN_F)

def go_straight_motor_3():
    pwm_pin_e.duty_cycle = 65535
    pwm_pin_f.duty_cycle = 0
    en_pin_3.duty_cycle = MOTOR_3_CALIB

def go_back_motor_3():
    pwm_pin_e.duty_cycle = 0
    pwm_pin_f.duty_cycle = 65535
    en_pin_3.duty_cycle = MOTOR_3_CALIB

#------------------------ MOTOR 2--------------------------
EN_PIN_2 = board.GP12
en_pin_2 = pwmio.PWMOut(EN_PIN_2)

PWM_PIN_C = board.GP6  
pwm_pin_c = pwmio.PWMOut(PWM_PIN_C)

PWM_PIN_D = board.GP7
pwm_pin_d = pwmio.PWMOut(PWM_PIN_D)

def go_straight_motor_2():
    pwm_pin_c.duty_cycle = 65535
    pwm_pin_d.duty_cycle = 0
    en_pin_2.duty_cycle = MOTOR_2_CALIB

def go_back_motor_2():
    pwm_pin_c.duty_cycle = 0
    pwm_pin_d.duty_cycle = 65535
    en_pin_2.duty_cycle = MOTOR_2_CALIB

#------------------------ MOTOR 1--------------------------
EN_PIN_1 = board.GP13
en_pin_1 = pwmio.PWMOut(EN_PIN_1)

PWM_PIN_A = board.GP8 
pwm_pin_a = pwmio.PWMOut(PWM_PIN_A)

PWM_PIN_B = board.GP9
pwm_pin_b = pwmio.PWMOut(PWM_PIN_B)

def go_straight_motor_1():
    pwm_pin_a.duty_cycle = 0
    pwm_pin_b.duty_cycle = 65535
    en_pin_1.duty_cycle = MOTOR_1_ST_CALIB

def go_back_motor_1():
    pwm_pin_a.duty_cycle = 65535
    pwm_pin_b.duty_cycle = 0
    en_pin_1.duty_cycle = MOTOR_1_B_CALIB
    
def slide_right():
    go_straight_motor_3()
    go_straight_motor_1()
    go_back_motor_2()
    go_back_motor_4()
    
def slide_left():
    go_back_motor_3()
    go_back_motor_1()
    go_straight_motor_2()
    go_straight_motor_4()

def drive_backward():
    go_straight_motor_1()
    go_straight_motor_2()
    go_straight_motor_3()
    go_straight_motor_4()

def drive_forward():
    go_back_motor_1()
    go_back_motor_2()
    go_back_motor_3()
    go_back_motor_4()
    
def drive_forward_slow():
    pwm_pin_a.duty_cycle = 65535
    pwm_pin_b.duty_cycle = 0
    en_pin_1.duty_cycle = MOTOR_1_B_CALIB - 8000

    pwm_pin_c.duty_cycle = 0
    pwm_pin_d.duty_cycle = 65535
    en_pin_2.duty_cycle = 31000
    
    pwm_pin_e.duty_cycle = 0
    pwm_pin_f.duty_cycle = 65535
    en_pin_3.duty_cycle = 31000
    
    pwm_pin_h.duty_cycle = 65535
    pwm_pin_g.duty_cycle = 0
    en_pin_4.duty_cycle = 31000

def drive_backward_slow():
    pwm_pin_a.duty_cycle = 0
    pwm_pin_b.duty_cycle = 65535
    en_pin_1.duty_cycle = MOTOR_1_ST_CALIB - 8000

    pwm_pin_c.duty_cycle = 65535
    pwm_pin_d.duty_cycle = 0
    en_pin_2.duty_cycle = 31000
    
    pwm_pin_e.duty_cycle = 65535
    pwm_pin_f.duty_cycle = 0
    en_pin_3.duty_cycle = 31000
    
    pwm_pin_h.duty_cycle = 0
    pwm_pin_g.duty_cycle = 65535
    en_pin_4.duty_cycle = 31000

def stop(pwm_a, pwm_b, en):
    pwm_a.duty_cycle = 0
    pwm_b.duty_cycle = 0
    en.duty_cycle = 65535
    
def brake():
    stop(pwm_pin_a, pwm_pin_b, en_pin_1)
    stop(pwm_pin_c, pwm_pin_d, en_pin_2)
    stop(pwm_pin_e, pwm_pin_f, en_pin_3)
    stop(pwm_pin_g, pwm_pin_h, en_pin_4)

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

def cw():
    go_straight_motor_1()
    go_back_motor_2()
    go_back_motor_3()
    go_straight_motor_4()

    
def ccw():
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

block_coords = {1:(4,0), 2:(4,1), 3:(4,2), 4:(3,2), 5:(3,1), 6:(3,0), 7:(2,0), 8:(2,1), 9:(2,2), 10:(1,2), 11:(1,1), 12:(1,0)}
'''
     1 ->  4, 0
     2 ->  4, 1
     3 ->  4, 2
     4 ->  3, 2
     5 ->  3, 1
     6 ->  3, 0
     7 ->  2, 0
     8 ->  2, 1
     9 ->  2, 2
    10 ->  1, 2
    11 ->  1, 1
    12 ->  1, 0
    
'''

laser = digitalio.DigitalInOut(board.GP14)
laser.direction = digitalio.Direction.OUTPUT


def go_right(target_distance):
    reached = False
    slide_right()
    current_distance = get_average_distance(rightB)
    while not reached:
        print("CD: "+ str(current_distance) + "  " + "TD: " + str(target_distance))
        if current_distance <= target_distance:
            brake()
            print("----------------------------------------------------Exited---------------------------------")
            reached = True
        else:
            current_distance = get_average_distance(rightB)

def go_forward(stop_distance):
    reached = False
    current_distance = get_average_distance(frontL)
    drive_forward()                
    while not reached:
        if current_distance <= stop_distance:
            brake()
            reached = True
        else:
            current_distance = get_average_distance(frontL)

def go_forward_slow_block():
    reached = False
    current_distance = get_average_distance(backL)
    stop_distance = current_distance -20
    current_distance = get_average_distance(frontL)
    drive_forward_slow()                
    while not reached:
        if current_distance <= stop_distance:
            brake()
            reached = True
        else:
            current_distance = get_average_distance(frontL)
    side_self_correct(0.1)

def go_backward_slow_block():
    reached = False
    current_distance = get_average_distance(backL)
    stop_distance = current_distance - 20
    current_distance = get_average_distance(backL)
    drive_backward_slow()                
    while not reached:
        if current_distance <= stop_distance:
            brake()
            reached = True
        else:
            current_distance = get_average_distance(backL)
    time.sleep(0.05)
    side_self_correct(0.1)
    
def start_position():
    go_right(32)
    back_self_correct(0.1)
    touch_back_wall()
    
def move_right(y_pos):
    if y_pos > 0:
        delta = y_pos * 5 * 2.54
        target_distance = RIGHT_CORNER_START_CONSTANT - delta
        go_right(target_distance)

def touch_back_wall():
    drive_backward()
    previous_distance = get_average_distance(backL)
    time.sleep(0.1)
    reached = False
    while not reached:
        current_distance = get_average_distance(backL)
        if current_distance >= previous_distance:
            brake()
            reached = True
        time.sleep(0.1)
        previous_distance = current_distance

def touch_left_wall():
    slide_left()
    previous_distance = get_average_distance(rightB)
    time.sleep(0.1)
    reached = False
    while not reached:
        current_distance = get_average_distance(rightB)
        if current_distance <= previous_distance:
            brake()
            reached = True
        time.sleep(0.1)
        previous_distance = current_distance

def side_self_correct(ERROR):
    F = get_average_distance(rightF)
    B = get_average_distance(rightB)
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
                ccw_5_deg()
                F = get_average_distance(rightF)
                B = get_average_distance(rightB)
    elif F > B:
        #print("F > B")
        while not positioned:
            delta = F - B
            if delta < ERROR:
                positioned = True
                print("F > B delta= " + str(delta))
            else:
                cw_5_deg()
                F = get_average_distance(rightF)
                B = get_average_distance(rightB)
    F = get_average_distance(rightF)
    B = get_average_distance(rightB)
    print("END:" "F: " + str(F) + " B: " + str(B))

def move_forward_to_edge(stop_distance):
    reached = False
    current_distance = get_average_distance(backL)
    drive_forward()                
    while not reached:
        if current_distance >= stop_distance:
            brake()
            reached = True
        else:
            current_distance = get_average_distance(backL)
    #back_self_correct(0.1)

def move_forward(x_pos):
    current_distance = get_average_distance(backL)
    target_distance = current_distance + (x_pos - 1)* 5 * 2.54
    if target_distance > 0:
        go_forward(target_distance)
    side_self_correct(0.1)



def turn_on_laser():
    print("ON!")
    laser.value = True 

def turn_off_laser():
    print("OFF!")
    laser.value = False 

def nudge_right():
    slide_right()
    time.sleep(0.09)
    brake()
    
RIGHT_CORNER_START_CONSTANT = 31
    
def extinguish(block_number):
    x_position = 3
    y_position = 1
    time.sleep(0.01)
    # come to start position from Rest Position
    start_position()
    
    # move right to Y position as per the value
    move_right(y_position)
      
    # come to edge of Y start position
    move_forward_to_edge(5)
    
    # Go To X - 1 Position
    move_forward(x_position)
    
    # Start the Laser
    turn_on_laser()
    
    # slowly Move 1 1/2 Block forward
    # slowly_move_forward(1 1/2 block)
    go_forward_slow_block()
    # Move slightly to right by 5 MM
    nudge_right()
    
    # Slowly move Back 1 1/2 Block
    # slowly_move_back(1 1/2 block)
    go_backward_slow_block()
    # Turn Off Laser
    turn_off_laser()
    
    # Go back X - 1 Position
    
    # Back-off from the edge of Y Start position
    touch_back_wall()
    
    touch_left_wall()
    
    touch_back_wall()

    
#DONE = False

#while not DONE:
    # Polls to check if any block on fire
    # If No go to sleep for 5 seconds and try again
    # If yes, extinguish it
    # extinguish(blockNumber) 

extinguish(4)
#slow_move_forward()
#touch_left_wall()
#touch_back_wall()
