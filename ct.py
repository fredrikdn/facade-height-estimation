import time
from heightutils import *
from rules import *
from geocoding import *

start_time = time.time()
runtime = 0
totaltime = 0


# File and image processing:
csv = 'results/results.csv'
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
            # File handling:
            infile, sort_file, pic, height, width = read_file(entry, folder)

            # Create lists and segment/detect floors:
            objects, lengths, heights, windows = sorted_array(infile)
            floors = multi_ransac(windows, height, width)
            floors = sort_objects(floors)
            floors = sort_floors_v2(floors)
            update_floors(floors, height)

            # Estimate height:
            height = estimate_height(floors)

            # Geocode address:
            lat, lng, address = get_loc(pic)
            #print(lat)

            # Add entry to CSV file:
            write_csv(csv, address, lat, lng, height)
            update_csv(csv)

            # Visualisation - drawing:
            draw_lines_centers(windows, floors, path, pic, vis, width)
            # draw_centers(windows, path+pic)
            # draw_floorlines(floors, path+pic, width)

            # Metrics:
            runtime = (time.time() - start_time)
            print("--- %s seconds ---" % runtime)
            print("   ")

totaltime = (time.time() - start_time)
print("--- Total: %s seconds ---" % totaltime)
print("COUNTER TERRORIST WIN")