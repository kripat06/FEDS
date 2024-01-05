import haversine as hs
from haversine import Unit
from math import pi, cos

loc1=(0,5) # Top Left
loc2=(6,5) # Top Right
loc3=(6,0) # Bottom Right
loc4=(0,0) # Bottom Left

cam_fov = 5 #feet
cam_fov = cam_fov * 0.3048

r_earth = 6371000.0

top  = hs.haversine(loc1,loc2,unit=Unit.FEET)
side = hs.haversine(loc3,loc4,unit=Unit.FEET)


columns = top/cam_fov
iterations = 1

coordinates = []
# print(top)
# print(side)


print(coordinates)
coordinate_1 = loc1
coordinate_2 = loc4
while iterations <= columns:
    new_latitude  = coordinate_1[1]  + (cam_fov / r_earth) * (180 / pi)
    new_coordinates = (new_latitude, coordinate_1[1])
    coordinates.append(new_coordinates)
    new_longitude = new_coordinates[0] + ((coordinate_1[1]-coordinate_2[1]) / r_earth) * (180 / pi) / cos(new_coordinates[0] * pi/180);
    new_coordinates = (coordinate_1[0], new_longitude)
    coordinates.append(new_coordinates)
    iterations += 1
print(coordinates)
print("Old cords:" + str(loc1[0]) +"," + str(loc1[1]))
print("New cords:" + str(loc1[0]) +"," + str(new_latitude))