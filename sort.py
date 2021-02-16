import os
import numpy as np
import time

start_time = time.time()

file = 'output/heidelberg-1.jpg.txt'

with open(file, 'r') as first_file:
    rows = first_file.readlines()
    sorted_rows = sorted(rows, key=lambda x: float(x.split()[0]), reverse=False)
    with open(file + '-sorted.txt', 'w+') as second_file:
        second_file.truncate(0)
        for row in sorted_rows:
            second_file.write(row)

print("--- %s seconds ---" % (time.time() - start_time))