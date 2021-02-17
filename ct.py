import math
import time
import numpy as np
import cv2

import PIL
from PIL import Image

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
object_list = []  # row: (x1, y1, x2, y2, class, threshold, x_center, y_center)
length_list = []
y_list = []

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
            y_list.append(y_diag)

# Average diagonal and height
avg_diagonal = sum(length_list) / len(length_list)
avg_height = sum(y_list) / len(y_list)
y_max = max(y_list)

print('Window diagonal avg: ', avg_diagonal)
print('Window height avg: ', avg_height)
print('Window max height: ', y_max)

#TODO: Arrange image into network of objects and floors --- "strips"

# Object center coordinate
for obj in object_list:
    x_center = obj[0] + ((obj[2] - obj[0]) / 2)
    y_center = obj[1] + ((obj[3] - obj[1]) / 2)
    obj.extend((x_center, y_center))  # add the center point coordinate to the object

print(object_list)
# LinReg line detection

"""
img = cv2.imread('dave.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = width  # set to image width
maxLineGap = avg_height  # avg window height
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('houghlines5.jpg',img)
"""

"""
# Strip size
strip_list = []

strip_threshold = avg_height + (y_max - avg_height)
y0 = height

for obj in sorted_list:
    if obj[1] > strip_threshold and obj[3] < y0:
        a = 1

"""
#TODO: For each strip: calculate crucial values s.a. avg size, no. windows, presence of object types, ...

'''
sort by coords:
    check if line is within threshold:

sort by type and size:
    round, square, big small ...

calculate the threshold for closeness of windows (i.e. small pixel diff from top to bottom of two distinct windows)
-> calculate the relative size of windows / diagonal length, find threshold based on this

for (x + 10; y++):
    if(x > xy1 && x < xy2 && not a vertical line && check for window type):
        counter ++
        
        


!! Height of building - cross check with camera parameters of the TK-car photos of facades ++ ground truth data
'''


# Calculate the size (ratio) of a given window

runtime = (time.time() - start_time)
print("--- %s seconds ---" % runtime)