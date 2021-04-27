import time
from heightutils import *
from rules import *

start_time = time.time()
runtime = 0
totaltime = 0


# Processing of the images:
path = 'googleimages/'
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
    with os.scandir(path) as it:
        for entry in it:
            infile, sort_file, pic, height, width = read_file(entry, folder)
            #sort_y(infile)

            # Create lists and segment/detect floors:
            objects, lengths, heights, windows = sorted_array(infile)
            #print("OBJECTS: ", objects)
            #print("WINDOWS: ", windows)

            floors = multi_ransac(windows, height, width)
            #print("#FLOORS: ", len(floors))
            floors = sort_objects(floors)
            floors = sort_floors_v2(floors)
            update_floors(floors, height)
            #print("UPDATED #FLOORS: ", len(floors))

            # Estimate height:

            estimate_height(floors)
            #draw_centers(windows, path+pic)
            #draw_floorlines(floors, path+pic, width)

            draw_lines_centers(windows, floors, path, pic, vis, width)
            runtime = (time.time() - start_time)
            print("--- %s seconds ---" % runtime)
            print("   ")

totaltime = (time.time() - start_time)
print("--- Total: %s seconds ---" % totaltime)
print("COUNTER TERRORIST WIN")