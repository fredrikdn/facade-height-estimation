import math
import time
import numpy as np
import cv2
from sklearn.linear_model import LinearRegression

import PIL
from PIL import Image

from myutils import *

# Iterate through the set of processed images

folder = 'output/'
pic = 'heidelberg-1.jpg'
pic_c = pic + '.txt'
pic_s = pic_c + '-sorted.txt'

image = PIL.Image.open(folder + pic)

file = 'output/' + pic_s
start_time = time.time()
runtime = 0

#TODO: Calculations and assigning of objects into a sorted list

# Lists
object_list = []  # row: (0:x1, 1:y1, 2:x2, 3:y2, 4:class (Window: 0.0; Door: 1.0; Balcony: 2.0),
                    # 5:threshold, 6:x_center, 7:y_center)

length_list = []
height_list = []  # list of heights (y value)

# Get width / height of the given pic
width, height = image.size


# Create a sorted list (array)
with open(file, 'r') as sorted_file:
    rows = sorted_file.readlines()
    # for each processed object; do:
    for row in rows:
        splt = row.split()
        tmp = []
        i = 0
        for s in splt:
            tmp.append(float(s))
            i = i + 1
        object_list.append(tmp)

        # Calculate and append length values for each window
        if tmp[4] == 0.0:
            x_diag = tmp[2] - tmp[0]
            y_diag = tmp[3] - tmp[1]
            length = math.sqrt(x_diag**2 + y_diag**2)
            length_list.append(length)
            height_list.append(y_diag)

#TODO: Arrange image into network of objects and floors --- "strips"

# OBJECT MANIPULATION: coordinates, center, etc.

for obj in object_list:
    x_center = obj[0] + ((obj[2] - obj[0]) / 2)
    y_center = obj[1] + ((obj[3] - obj[1]) / 2)
    obj.extend((x_center, y_center))  # add the center point coordinate to the object

# WINDOW MANIPULATION

# Average diagonal and height
avg_diagonal = sum(length_list) / len(length_list)
avg_height = sum(height_list) / len(height_list)
y_max = max(height_list)

print('Window diagonal avg: ', avg_diagonal)
print('Window height avg: ', avg_height)
print('Window max height: ', y_max)

window_list = []
for o in object_list:
    if o[4] == 0.0:
        window_list.append(o)

# FLOOR DETECTION
# Partition data into layers (floors) - x_center [6], y_center [7]
# Floor segmentation / detection - UTC algorithm


def detect_floors(objects):
    f_list = []
    # Set constraint as input from another function
    constraint = 0.1  # should be based on relationship between x and y values

    tmp_floor = []

    # For each object, assign floor value:
    for index, ob in enumerate(objects):

        # For elements which are not the last two objects
        if index < len(objects) - 1:
            next_ob = objects[index + 1]

            # Object coordinates
            c_xx = ob[6]
            c_yy = ob[7]

            n_xx = next_ob[6]
            n_yy = next_ob[7]

            x_list = np.array([c_xx, n_xx])
            y_list = np.array([c_yy, n_yy])

            # Constraint calculation
            slope = np.polyfit(x_list, y_list, 1)[0]

            # Add the currently accumulated floor to its corresponding floor in f_list
            if abs(slope) > constraint:
                if not index == 0:
                    f_list.append(tmp_floor)
                    tmp_floor = []
                    print("FLOOR LIST: ", f_list)
                else:
                    f_list.append([ob])

            else:
                tmp_floor.append(ob)
                print("Current Floor: ", tmp_floor)

            print("CURR ==> XX: ", c_xx, "     YY: ", c_yy)
            print("NEXT ==> XX: ", n_xx, "     YY: ", n_yy)
            print("SLOPE: ", slope)

        # The last two objects
        else:
            prev_ob = objects[index - 1]

            # Last object coordinates
            l_xx = ob[6]
            l_yy = ob[7]

            # Previous object coordinates
            p_xx = prev_ob[6]
            p_yy = prev_ob[7]

            x_pair = np.array([l_xx, p_xx])
            y_pair = np.array([l_yy, p_yy])

            # Line calculation
            slope = np.polyfit(x_pair, y_pair, 1)[0]

            if abs(slope) < constraint:
                tmp_floor.append(ob)
                f_list.append(tmp_floor)

            else:
                f_list.append([ob])

            print("LAST ==> XX: ", l_xx, "     YY: ", l_yy)
            print("PREVIOUS ==> XX: ", p_xx, "     YY: ", p_yy)
            print("SLOPE: ", slope)
            print(" --------- ")
        print("FLOOR LIST: ", f_list)
        print("FLOORS: ", len(f_list))

    return f_list


def draw_floorlines(floors):
    facade = floors

    line_list = []

    for index, floor in enumerate(facade):
        xx = []
        yy = []
        for obj in floor:
            xx.append(obj[6])
            yy.append(obj[7])
        x_list = np.array(xx)
        y_list = np.array(yy)

        line = np.polyfit(x_list, y_list, 1)
        line_list.append(line)
        



if __name__ == '__main__':
    floors = detect_floors(window_list)
    draw_floorlines(floors)
    runtime = (time.time() - start_time)
    print("--- %s seconds ---" % runtime)