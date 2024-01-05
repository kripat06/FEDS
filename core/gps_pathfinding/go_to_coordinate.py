import time
import os
import platform
import sys
import math

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil


targetAltitude = 1
manualArm = True
############DRONEKIT#################
vehicle = connect('/dev/ttyAMA0', baud=57600, wait_ready=True)

#########FUNCTIONS###########
def arm_and_takeoff(targetHeight):
    while vehicle.is_armable != True:
        print("Waiting for vehicle to become armable.")
        time.sleep(1)
    print("Vehicle is now armable")

    vehicle.mode = VehicleMode("GUIDED")

    while vehicle.mode != 'GUIDED':
        print("Waiting for drone to enter GUIDED flight mode")
        time.sleep(1)
    print("Vehicle now in GUIDED MODE. Have fun!!")

    if manualArm == False:
        vehicle.armed = True
        while vehicle.armed == False:
            print("Waiting for vehicle to become armed.")
            time.sleep(1)
    else:
        if vehicle.armed == False:
            print("Exiting script. manualArm set to True but vehicle not armed.")
            print("Set manualArm to True if desiring script to arm the drone.")
            return None
    print("Look out! Props are spinning!!")

    vehicle.simple_takeoff(targetHeight)  ##meters

    while True:
        print("Current Altitude: %d" % vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= .95 * targetHeight:
            break
        time.sleep(1)
    print("Target altitude reached!!")

    return None
def get_distance_meters(targetLocation,currentLocation):
	dLat=targetLocation.lat - currentLocation.lat
	dLon=targetLocation.lon - currentLocation.lon
	
	return math.sqrt((dLon*dLon)+(dLat*dLat))*1.113195e5


arm_and_takeoff(targetAltitude)

a_location = LocationGlobalRelative(37.5697265, -122.0604765, 1)

vehicle.airspeed = 0.5 #m/s

# Set the target location in global-relative frame
print("Moving to coords")

vehicle.simple_goto(a_location)
time.sleep(10)

vehicle.mode = VehicleMode("LAND")

while vehicle.mode != 'LAND':
    time.sleep(1)
    print("Waiting for drone to land")
print("Drone in land mode. Exiting script.")
