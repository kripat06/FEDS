import haversine as hs
from haversine import Unit
import math
import matplotlib.pyplot as plt
import pandas as pd
from math import sin, cos, sqrt, atan2, radians

loc1=(37.5697512,-122.0605587) # Top Left
loc4=(37.5697512,-122.0604028) # Bottom Left
loc2=(37.5696898,-122.0605587) # Top Right
loc3=(37.5696898,-122.0604028) # Bottom Right
BBox = ((-122.06077, -122.05954, 37.57000, 37.56939))

cam_fov = 5 #feet
cam_fov_m = cam_fov/3.281 #meters
cam_fov_gps = 0.00005 #3.33 meters

r_earth = 6371000.0
field_names = ['Latitude','Longitude']

top  = hs.haversine(loc1,loc2,unit=Unit.FEET)
side = hs.haversine(loc3,loc4,unit=Unit.FEET)

map_path = 'D:\projects\gps_pathfinding\map.png'
bbox_path = 'D:\projects\gps_pathfinding\\bounding_border.csv'
columns = top/cam_fov
columns = math.trunc(columns)

iterations = 1

coordinates = []
latitudes = []
longitudes =[]

def generate_coordinates():
    iterations = 1
    while iterations < columns:
        if iterations ==1:
            latitudes.append(loc1[0])
            latitudes.append(loc2[0])
            longitudes.append(loc1[1])
            longitudes.append(loc2[1])
        coordinates.append((str(loc1[0]), str(loc1[1] + cam_fov_gps * iterations)))
        print(loc1[1] + cam_fov_gps * iterations - loc2[1])
        print(loc2[0], loc2[1])
        if loc2[1] - loc1[1] + cam_fov_gps * iterations >= 0.000001:
            latitudes.append(loc1[0])
            longitudes.append(loc1[1] + cam_fov_gps * iterations)

            coordinates.append((str(loc2[0]), str(loc2[1] + cam_fov_gps * iterations)))
            print(coordinates)

            latitudes.append(loc2[0])
            longitudes.append(loc2[1] + cam_fov_gps * iterations)

        else:
            break

        print(iterations)
        iterations = iterations + 1
    return coordinates

def coord_distance(coord_1, coord_2):
    lat1 = radians(coord_1[0])
    lon1 = radians(coord_1[1])
    lat2 = radians(coord_2[0])
    lon2 = radians(coord_2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = 6373.0 * c
    return distance

def plot_points(latitudes, longitudes, coordinates):
    map = plt.imread(map_path)
    border = pd.read_csv(bbox_path)

    fig, ax = plt.subplots(figsize=(8, 7))

    i = 1

    for x in coordinates:
        ax.scatter(longitudes, latitudes, zorder=1, alpha=0.2, c='b', s=10)
        print(x[0])
        print(x[1])
    ax.scatter(border.Longitude, border.Latitude, zorder=1, alpha=0.2, c='r', s=10)

    ax.set_title('Plotting Spatial Data')
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    plt.imshow(map, zorder=0, extent=BBox, aspect='equal')
    plt.show()

coords = generate_coordinates()
plot_points(latitudes, longitudes, coords)


