import numpy as np
import cv2
import math
import random
from sklearn import linear_model
import matplotlib.pyplot as plt
import os
import PIL
from operator import itemgetter

# URL & Google
import hashlib
import hmac
import base64
import urllib.parse as urlparse
import urllib.request as urlrequest

# -------------------------------------- File processing ------------------------------------------

def read_file(entry, folder):
    if entry.name.endswith(".jpg") and entry.is_file():
        pic = entry.name
        print("NAME: ", entry.name)

        pic_c = pic + '.txt'
        pic_s = pic_c + '-sorted.txt'

        infile = folder + pic_c
        sort_file = folder + pic_s

        # Get width / height of the given pic
        image = PIL.Image.open(folder + pic)
        width, height = image.size

    return infile, sort_file, pic, height, width


# --------------------------------------- Google API --------------------------------------------

def sign_url(input_url=None, secret=None):
    """ Sign a request URL with a URL signing secret.
      Usage:
      from urlsigner import sign_url
      signed_url = sign_url(input_url=my_url, secret=SECRET)
      Args:
      input_url - The URL to sign
      secret    - Your URL signing secret
      Returns:
      The signed request URL
  """

    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()


# Define area of interest (street)
def getStreet(street, post, city):
    locations = []
    for i in range(1, 10):
        tmp = street + ',' + str(i) + ',' + post + ',' + city
        locations.append(tmp)
    return locations


# Download images
def get_img(loc, saveloc, signed):
    url = signed
    file = loc + ".jpg"
    urlrequest.urlretrieve(url, os.path.join(saveloc, file))


# ----------------------------- Sorting -------------------------------------


def sort_y(file):  # Sort by Y

    with open(file, 'r') as first_file:
        rows = first_file.readlines()
        sorted_rows = sorted(rows, key=lambda x: float(x.split()[1]), reverse=False)
        with open(file + '-sorted.txt', 'w+') as second_file:
            second_file.truncate(0)
            for row in sorted_rows:
                second_file.write(row)


def sorted_array(file):  # Sort and create an array of coordinates
    object_list = []
    length_list = []
    height_list = []
    window_list = []
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

    # Find coordinates for left, right, center:
    for obj in object_list:

        x_center = obj[0] + ((obj[2] - obj[0]) / 2)
        y_center = obj[1] + ((obj[3] - obj[1]) / 2)

        x_left = obj[0] - 10
        y_left = y_center
        x_right = obj[2] + 10
        y_right = y_center

        obj.extend((x_center, y_center, x_left, y_left, x_right, y_right))  # add the coordinates to the object

        # Calculate and append length values for each window
        if obj[4] == 0.0 or obj[4] == 1.0:
            x_width = tmp[2] - tmp[0]
            y_height = tmp[3] - tmp[1]
            length = math.sqrt(x_width ** 2 + y_height ** 2)
            length_list.append(length)
            height_list.append(y_height)

        if obj[4] == 0.0:
            window_list.append(obj)

    return object_list, length_list, height_list, window_list


# Sorting s.t. bottom floor is 0
def sort_floors(floors):
    # Assign avg y-value to each floor
    for floor in floors:
        yy = []
        for obj in floor:
            yy.extend((obj[9], obj[7], obj[11]))
        y_list = np.array(yy)
        y_avg = sum(y_list) / len(y_list)
        floor.append(y_avg)
        #print("FLOOR Y: ", floor[len(floor)-1])

    #print("FlOORS UNSORTED: ", floors)

    # Insertion sort:
    for i in range(1, len(floors)):
        floor = floors[i]
        #print("KEY: ", floor)

        j = i - 1
        floor_0 = floors[j]
        while j >= 0 and floor[len(floor)-1] < floor_0[len(floor_0)-1]:
            floors[j + 1] = floors[j]
            j -= 1
        floors[j + 1] = floor

    print("FLOORS SORTED: ", floors)
    print("#Floors: ", len(floors))
    return floors


# Sorting objects within floors (y value)
def sort_floors_v2(floors):
    # Assign avg y-value to each floor
    for floor in floors:
        yy = []
        for obj in floor:
            yy.extend((obj[9], obj[7], obj[11]))
        y_list = np.array(yy)
        y_avg = sum(y_list) / len(y_list)
        floor.append(y_avg)

    # Sorts each floor in floors on y_avg value
    #print("floors before floor sort:", floors)
    floors = sorted(floors, key=lambda floor: floor[-1])
    #print("floors after floor sort:", floors)
    return floors


# Sorting objects within floors (x value)
def sort_objects(floors):
    for index, floor in enumerate(floors):
        #print("FLOOR BEFORE: ", floor)
        floor = sorted(floor, key=itemgetter(0))
        #print("FLOOR AFTER: ", floor)
        floors[index] = floor
    return floors

# ----------------------------- Floor utils -------------------------------------
# FLOOR DETECTION: Floor segmentation / detection - UTC algorithm


def multi_ransac(objects, height, width):  # RANSAC estimates for detecting floor lines
    f_list = []

    MIN_SAMPLES = 3

    xs, ys = [], []
    # TODO: Set scale (to ensure values between 0-100):
    scale = 100

    for obj in objects:
        # (center, left, right) coordinates for xs and ys
        xs.extend((obj[6] / scale, obj[8] / scale, obj[10] / scale))
        ys.extend((obj[7] / scale, obj[9] / scale, obj[11] / scale))

    xs = np.array(xs)
    ys = np.array(ys)

    plt.show()

    colors = "rgbcmykw"
    idx = 0

    while len(xs) > MIN_SAMPLES:
        # build design matrix for linear regressor
        X = np.ones((len(xs), 2))
        X[:, 1] = xs

        ransac = linear_model.RANSACRegressor(
            residual_threshold=.067, min_samples=MIN_SAMPLES
        )

        res = ransac.fit(X, ys)
        score = ransac.score(X, ys)

        # Score is misleading, as the R^2 is calculated with multiransac
            # --> many points will be outliers initially and reduced iteratively
        #print("Score: ", score)

        # vector of boolean values, describes which points belong
        # to the fitted line:
        inlier_mask = ransac.inlier_mask_

        # plot point cloud:
        xinlier = xs[inlier_mask]
        yinlier = ys[inlier_mask]
        #print("INLIERS x: ", xinlier)
        #print("INLIERS y: ", yinlier)

        # find and append object from object list, whose xs and ys correspond to inliers
        tmp_floor = []
        for obj in objects:
            for x in xinlier:
                if x == obj[6] / scale:
                    for y in yinlier:
                        if y == obj[7] / scale and obj not in tmp_floor:
                            tmp_floor.append(obj)
                            #print("tmp floor, iter: ", tmp_floor)
        #print("tmp floor: ", tmp_floor)
        if len(tmp_floor) > 1:
            f_list.append(tmp_floor)
        #print("floors: ", f_list)

        # circle through colors:
        color = colors[idx % len(colors)]
        idx += 1
        plt.plot(xinlier, yinlier, color + "*")

        # only keep the outliers:
        xs = xs[~inlier_mask]
        ys = ys[~inlier_mask]

    plt.show()

    return f_list


# OLD METHOD ( MIGHT BE USED LATER IDK)
def detect_floors(objects):  # Detecting floors on the facade from object coordinates
    f_list = []
    # Set constraint as input from another function
    constraint = 0.3  # should be based on relationship between x and y values

    tmp_floor = []

    # For each object, assign floor value:
    for index, ob in enumerate(objects):

        # For elements which are not the last two objects
        if index < len(objects) - 1:
            next_ob = objects[index + 1]

            # Object coordinates
            c_xx = ob[6]
            c_yy = ob[7]

            n_xx = next_ob[6]
            n_yy = next_ob[7]

            x_list = np.array([c_xx, n_xx])
            y_list = np.array([c_yy, n_yy])

            # Constraint calculation
            slope = np.polyfit(x_list, y_list, 1)[0]
            #print("SLOPE: ", slope)

            # Add the currently accumulated floor of objects to its entry in the f_list
            if abs(slope) > constraint:
                if not index == 0:
                    f_list.append(tmp_floor)
                    tmp_floor.clear()
                    #print("FLOOR LIST: ", f_list)
                else:
                    f_list.append([ob])

            # Continue adding objects to current floor
            else:
                tmp_floor.append(ob)
                #print("Current Floor: ", tmp_floor)

            #print("CURR ==> XX: ", c_xx, "     YY: ", c_yy)
            #print("NEXT ==> XX: ", n_xx, "     YY: ", n_yy)
            #print("SLOPE: ", slope)

        # The last two objects
        else:
            prev_ob = objects[index - 1]

            # Last object coordinates
            l_xx = ob[6]
            l_yy = ob[7]

            # Previous object coordinates
            p_xx = prev_ob[6]
            p_yy = prev_ob[7]

            x_pair = np.array([l_xx, p_xx])
            y_pair = np.array([l_yy, p_yy])

            # Line calculation
            slope = np.polyfit(x_pair, y_pair, 1)[0]

            if abs(slope) < constraint:
                tmp_floor.append(ob)
                f_list.append(tmp_floor)

            else:
                f_list.append([ob])

            print("LAST ==> XX: ", l_xx, "     YY: ", l_yy)
            print("PREVIOUS ==> XX: ", p_xx, "     YY: ", p_yy)
            print("SLOPE: ", slope)
            print(" --------- ")
        print("FLOOR LIST: ", f_list)
        print("FLOORS: ", len(f_list))

    return f_list


# -------------------------------- Error Correction ------------------------------------

# Removes faulty floors (by angle, distance, etc.)
def update_floors(floors, height):
    ys = []
    tmp_floors = floors
    for index, floor in enumerate(floors):
        xx = []
        yy = []
        tmp_floor = floor
        id = 0
        for obj in floor:

            if id < len(floor)-1:
                xx.extend((obj[8], obj[6], obj[10]))
                yy.extend((obj[9], obj[7], obj[11]))
                id += 1

        x_list = np.array(xx)
        y_list = np.array(yy)

        # Angle calculation - check (x deg):
        line = np.polyfit(x_list, y_list, 1)  # [0] is slope
        if abs(line[0]) > 0.3:  # May be chosen using statistics for each floor
            floors.pop(index)

        # Average Y value of floor -- Proximity check (dist between floors,  f1 - f2):
        ys.append(sum(y_list) / len(y_list))
        #print("Ys: ", ys)

    # TODO: Intersection calculation - remove obvious errors of intersecting floors
    #for tmp_floor in tmp_floors:
    #    print("TMPFLOOR: ", tmp_floor)

    # Distance calculation: (distance[0] is distance between floor_0 and floor_1)
    distances = []
    for index, y in enumerate(ys):
        # index not at last pos
        if index < len(ys) - 1:
            d = abs(ys[index + 1] - y)
            distances.append(d)
            print("Distance: ", d)

    # Combine floors that are closely aligned to one single floor
    for index, floor in enumerate(floors):
        print("FLOOR .remove: ", floor)
        if index < len(floors)-2 and len(floors) > 1:
            # Checks for overlapping images on both left and right side of image

            # Using | len(floors) - 3 | as this corresponds to the 2nd to last object (not including avg_y value)
            if floors[index][0][1] < floors[index + 1][0][3] and floors[index][len(floor) - 2][1] < floors[index + 1][len(floors[index+1]) - 2][3]:
                # Removes floor with fewer objects
                if len(floors[index]) <= len(floors[index + 1]):
                    floors.remove(floors[index])
                else:
                    floors.remove(floors[index+1])

    return floors

#TODO: Facade segmenter; segment facade based on the relative floor line distances ...

# --------------------------------- Plotting utils -------------------------------------
# Draw on building images for visualisation purposes


def draw_centers(objects, img):  # Draw centers of objects
    image = cv2.imread(img, cv2.IMREAD_COLOR)

    for obj in objects:
        image = cv2.circle(image, (int(obj[6]), int(obj[7])), radius=2, color=(0, 0, 255), thickness=-1)

    name = img + "-centers.jpg"

    if image is not None:
        cv2.imwrite(name, image)


def draw_floorlines(flrs, img, width):  # Draw floor lines
    line_list = []

    for index, floor in enumerate(flrs):
        xx = []
        yy = []
        for obj in floor:
            xx.extend((obj[8], obj[6], obj[10]))
            yy.extend((obj[9], obj[7], obj[11]))
        x_list = np.array(xx)
        y_list = np.array(yy)

        line = np.polyfit(x_list, y_list, 1)
        line_list.append(line)

    image = cv2.imread(img, cv2.IMREAD_COLOR)
    for line in line_list:
        start_p = (0, int(line[1]))
        end_p = (int(width), int(line[1]+(line[0]*width)))

        cv2.line(image, start_p, end_p, (0, 255, 255), 1)

    name = img + "-lines.jpg"

    if image is not None:
        cv2.imwrite(name, image)


def draw_lines_centers(objects, flrs, path, pic, output, width):
    line_list = []
    # Image path and name
    img = path + pic

    for index, floor in enumerate(flrs):
        xx = []
        yy = []

        id = 0
        for obj in floor:
            if id < len(floor) - 1:
                xx.extend((obj[8], obj[6], obj[10]))
                yy.extend((obj[9], obj[7], obj[11]))
                id += 1

        x_list = np.array(xx)
        y_list = np.array(yy)

        line = np.polyfit(x_list, y_list, 1)
        line_list.append(line)

    # DRAWING
    image = cv2.imread(img, cv2.IMREAD_COLOR)
    for line in line_list:
        start_p = (0, int(line[1]))
        end_p = (int(width), int(line[1] + (line[0] * width)))

        cv2.line(image, start_p, end_p, (0, 255, 255), 3)

    for obj in objects:
        image = cv2.circle(image, (int(obj[6]), int(obj[7])), radius=3, color=(0, 0, 255), thickness=-1)

    name = output + pic + "-lines_points.jpg"

    if image is not None:
        cv2.imwrite(name, image)


