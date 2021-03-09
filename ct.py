import math
import time
import numpy as np
import cv2
from sklearn.linear_model import LinearRegression

import PIL
from PIL import Image

from myutils import *
from heightutils import *

start_time = time.time()
runtime = 0

# Processing of the images:
imgs = "testimg/"
folder = 'output/'
pic = 'trondheim-testo.jpg'

pic_c = pic + '.txt'
pic_s = pic_c + '-sorted.txt'

infile = folder + pic_c

image = PIL.Image.open(folder + pic)

sort_file = folder + pic_s

# Lists
objects = []  # row: (0:x1, 1:y1, 2:x2, 3:y2, 4:class (Window: 0.0; Door: 1.0; Balcony: 2.0),
# 5:threshold, 6:x_center, 7:y_center, 8:x_left, 9:y_left, 10:x_right, 11:y_right)


lengths = []
heights = []  # list of heights (y value)
windows = []

# Get width / height of the given pic
width, height = image.size

if __name__ == '__main__':
    sort_y(infile)

    objects, length, height, windows = sorted_array(sort_file)
    #floors = detect_floors(windows)
    floors = multiransac(windows, height, width)

    draw_centers(windows, folder+pic)
    draw_floorlines(floors, folder+pic, width)

    draw_lines_centers(windows, floors, folder+pic, width)
    runtime = (time.time() - start_time)
    print("--- %s seconds ---" % runtime)
