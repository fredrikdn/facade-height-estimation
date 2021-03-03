import math
import time
import numpy as np
import cv2
from sklearn.linear_model import LinearRegression

import PIL
from PIL import Image

from myutils import *
from heightutils import *

# Iterate through the set of processed images

folder = 'output/'
pic = 'heidelberg-1.jpg'
pic_c = pic + '.txt'
pic_s = pic_c + '-sorted.txt'

image = PIL.Image.open(folder + pic)

file = 'output/' + pic_s
start_time = time.time()
runtime = 0

# Calculations and assigning of objects into a sorted list

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

# TODO: Arrange image into network of objects and floors

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


if __name__ == '__main__':
    floors = detect_floors(window_list)
    draw_floorlines(floors)
    draw_centers(window_list, folder+pic)
    runtime = (time.time() - start_time)
    print("--- %s seconds ---" % runtime)