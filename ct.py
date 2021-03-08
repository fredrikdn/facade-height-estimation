import math
import time
import numpy as np
import cv2
from sklearn.linear_model import LinearRegression

import PIL
from PIL import Image

from myutils import *
from heightutils import *

# Processing of the images:
imgs = "testimg/"
folder = 'output/'
pic = 'trondheim-test.jpg'

pic_c = pic + '.txt'
pic_s = pic_c + '-sorted.txt'

infile = folder + pic_c

image = PIL.Image.open(folder + pic)

sort_file = folder + pic_s

start_time = time.time()
runtime = 0

# Lists
objects = []  # row: (0:x1, 1:y1, 2:x2, 3:y2, 4:class (Window: 0.0; Door: 1.0; Balcony: 2.0),
                    # 5:threshold, 6:x_center, 7:y_center)

lengths = []
heights = []  # list of heights (y value)
windows = []

# Get width / height of the given pic
width, height = image.size

print("width: ", width)
print("height: ", height)

# Average diagonal and height
"""
avg_diagonal = sum(length_list) / len(length_list)
avg_height = sum(height_list) / len(height_list)
y_max = max(height_list)

print('Window diagonal avg: ', avg_diagonal)
print('Window height avg: ', avg_height)
print('Window max height: ', y_max)
"""


if __name__ == '__main__':
    #sort_y(infile)

    objects, length, height, windows = sorted_array(sort_file)
    #floors = detect_floors(windows)
    floors = multiransac(windows, height, width)

    draw_centers(windows, folder+pic)
    draw_floorlines(floors, folder+pic, width)

    draw_lines_centers(windows, floors, folder+pic, width)
    runtime = (time.time() - start_time)
    print("--- %s seconds ---" % runtime)
