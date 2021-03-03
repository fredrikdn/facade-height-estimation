import os
import numpy as np
import time

start_time = time.time()

img = "output/trondheim-test.jpg.txt"


def sort_y(file):

    # Sorted on y-value
    with open(file, 'r') as first_file:
        rows = first_file.readlines()
        sorted_rows = sorted(rows, key=lambda x: float(x.split()[1]), reverse=False)
        with open(file + '-sorted.txt', 'w+') as second_file:
            second_file.truncate(0)
            for row in sorted_rows:
                second_file.write(row)


sort_y(img)
print("--- %s seconds ---" % (time.time() - start_time))