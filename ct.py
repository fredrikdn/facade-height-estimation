import math
import time
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

# Lists
sorted_list = []
length_list = []

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
        sorted_list.append(tmp)

        # Calculate and append diagonal length
        if tmp[4] == 0.0:
            x = tmp[2] - tmp[0]
            y = tmp[3] - tmp[1]
            length = math.sqrt(x**2 + y**2)
            length_list.append(length)
print(sorted_list)

# Average window size
avg_diagonal = sum(length_list) / len(length_list)
print('Window diagonal avg: ', avg_diagonal)

#TODO: Arrange image into horizontal strips

#strip = height /

for coords in sorted_list:
    x1 = coords[0]
    x2 = coords[2]

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