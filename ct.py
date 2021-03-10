import time
from heightutils import *

start_time = time.time()
runtime = 0

# Processing of the images:
path = "testimg/"
folder = 'output/'
vis = 'visualisations/'
target = 'trondheim-test.jpg'

# Lists
objects = []  # row: (0:x1, 1:y1, 2:x2, 3:y2, 4:class (Window: 0.0; Door: 1.0; Balcony: 2.0),
# 5:threshold, 6:x_center, 7:y_center, 8:x_left, 9:y_left, 10:x_right, 11:y_right)
lengths = []  # length of object diagonals
heights = []  # list of heights (y value)
windows = []  # window list


if __name__ == '__main__':
    # TODO: Works for reading the last file, make it work on the whole directory
    infile, sort_file, pic, height, width = read_img(path, folder, target)

    sort_y(infile)

    objects, length, height, windows = sorted_array(sort_file)
    floors = multi_ransac(windows, height, width)
    print("FLOORS: ", len(floors))
    # TODO: Update floor list, remove misclassified objects
    update_floors(floors)
    print("UPDATED FLOORS: ", len(floors))

    #draw_centers(windows, path+pic)
    #draw_floorlines(floors, path+pic, width)
    draw_lines_centers(windows, floors, path, pic, vis, width)
    runtime = (time.time() - start_time)
    print("--- %s seconds ---" % runtime)
