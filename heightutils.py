import numpy as np
import cv2
import math

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

            # Calculate and append length values for each window
            if tmp[4] == 0.0:
                x_diag = tmp[2] - tmp[0]
                y_diag = tmp[3] - tmp[1]
                length = math.sqrt(x_diag ** 2 + y_diag ** 2)
                length_list.append(length)
                height_list.append(y_diag)

    for obj in object_list:
        x_center = obj[0] + ((obj[2] - obj[0]) / 2)
        y_center = obj[1] + ((obj[3] - obj[1]) / 2)
        obj.extend((x_center, y_center))  # add the center point coordinate to the object

    for o in object_list:
        if o[4] == 0.0:
            window_list.append(o)

    return object_list, length_list, height_list, window_list


# ----------------------------- Floor utils -------------------------------------
# FLOOR DETECTION
# Partition data into layers (floors) - x_center [6], y_center [7]
# Floor segmentation / detection - UTC algorithm


def detect_floors(objects):  # Detecting floors on the facade from object coordinates
    f_list = []
    # Set constraint as input from another function
    constraint = 0.1  # should be based on relationship between x and y values

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

            # Add the currently accumulated floor of objects to its entry in the f_list
            if abs(slope) > constraint:
                if not index == 0:
                    f_list.append(tmp_floor)
                    tmp_floor.clear()
                    print("FLOOR LIST: ", f_list)
                else:
                    f_list.append([ob])

            # Continue adding objects to current floor
            else:
                tmp_floor.append(ob)
                print("Current Floor: ", tmp_floor)

            print("CURR ==> XX: ", c_xx, "     YY: ", c_yy)
            print("NEXT ==> XX: ", n_xx, "     YY: ", n_yy)
            print("SLOPE: ", slope)

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
            xx.append(obj[6])
            yy.append(obj[7])
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


def draw_lines_centers(objects, flrs, img, width):
    line_list = []

    for index, floor in enumerate(flrs):
        xx = []
        yy = []
        for obj in floor:
            xx.append(obj[6])
            yy.append(obj[7])
        x_list = np.array(xx)
        y_list = np.array(yy)

        line = np.polyfit(x_list, y_list, 1)
        line_list.append(line)

    # DRAWING
    image = cv2.imread(img, cv2.IMREAD_COLOR)
    for line in line_list:
        start_p = (0, int(line[1]))
        end_p = (int(width), int(line[1] + (line[0] * width)))

        cv2.line(image, start_p, end_p, (0, 255, 255), 1)

    for obj in objects:
        image = cv2.circle(image, (int(obj[6]), int(obj[7])), radius=2, color=(0, 0, 255), thickness=-1)

    name = img + "-lines_points.jpg"

    if image is not None:
        cv2.imwrite(name, image)


