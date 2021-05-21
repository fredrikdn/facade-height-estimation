import time
from heightutils import *
from rules import *
from tester import *

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
            # File processing: (input is a folder of images, Google img - should be named with address)
            infile, sort_file, pic, height, width, bid, address = read_file(entry, folder)
            building_type = get_building_type(bid)
            #building_footprint = get_building_footprint(bid)
            print("BID: ", bid)

            # Create lists and segment/detect floors:
            objects, lengths, heights, windows = sorted_array(infile)
            try:
                floors = multi_ransac(windows, height, width)
            except ValueError:
                print("RANSAC could not find a valid consensus set")

            #  Sorting & Error correction:
            floors = sort_objects(floors)
            floors = sort_floors_v2(floors)
            floors = remove_avg_y(floors)

            floors = remove_misaligned(floors)
            floors = remove_redundant(floors)

            floors = sort_objects(floors)
            floors = sort_floors_v2(floors)
            floors = remove_avg_y(floors)

            # Rules - Estimate height:
            # Also passes entry.name (address, building ID)

            height = estimate_height(floors, bid, building_type)

            # Add entry to CSV file: ( + building_id, footprint...)
            update_csv_v2(csv, bid, height)

            # Visualisation - drawing:
            draw_lines_centers(windows, floors, path, pic, vis, width)
            # draw_centers(windows, path+pic)
            # draw_floorlines(floors, path+pic, width)

            # Metrics:
            runtime = (time.time() - start_time)
            print("--- %s seconds ---" % runtime)
            print("   ")

trim_csv(csv)
totaltime = (time.time() - start_time)
print("--- Total: %s seconds ---" % totaltime)
print("COUNTER TERRORIST WIN")