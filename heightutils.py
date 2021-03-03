import numpy as np
import cv2

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

            # Add the currently accumulated floor to its corresponding floor in f_list
            if abs(slope) > constraint:
                if not index == 0:
                    f_list.append(tmp_floor)
                    tmp_floor = []
                    print("FLOOR LIST: ", f_list)
                else:
                    f_list.append([ob])

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


def draw_centers(objects, img):
    image = cv2.imread(img, cv2.IMREAD_COLOR)

    for obj in objects:
        image = cv2.circle(image, int((obj[6]), int(obj[7])), radius=0, color=(255, 0, 0), thickness=-1)

    cv2.imwrite(image, "-centers.jpg")


def draw_floorlines(flrs):
    facade = flrs

    line_list = []

    for index, floor in enumerate(facade):
        xx = []
        yy = []
        for obj in floor:
            xx.append(obj[6])
            yy.append(obj[7])
        x_list = np.array(xx)
        y_list = np.array(yy)

        line = np.polyfit(x_list, y_list, 1)
        line_list.append(line)



