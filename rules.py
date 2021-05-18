import math

# Predefined Values (meters)
avg_floor = 2.5
avg_ServiceFloor = 3.0
avg_Door = 2.0

basement_height = 0.5


# Calculate window size
def window_size(floors):
    size_list = []
    avg_list = []
    for floor in floors:
        w_floor = []
        for obj in floor:
            y_dist = obj[3] - obj[1]
            w_floor.append(y_dist)
        avg_size = sum(w_floor) / len(w_floor)
        avg_list.append(avg_size)

        size_list.append(w_floor)
    print(avg_list)
    b = s = 0
    basement = store = False
    for i in range(1, len(avg_list)):
        if avg_list[0] < avg_list[i] / 1.8:
            b = b + 1
        if avg_list[0] / 2 > avg_list[i]:
            s = s + 1
    # Check for basement / storefront type
    if b == len(avg_list) - 1 and len(avg_list) > 1:
        basement = True
    if s == len(avg_list) - 1 and len(avg_list) > 1:
        store = True

    return basement, store


def estimate_height(floors):
    # window size rules
    basement, store = window_size(floors)
    print("BOOL: ", basement)

    if basement:
        height = (len(floors)-1) * avg_floor + basement_height
        print("BASEMENT BRO")
    elif store:
        height = (len(floors)-1) * avg_floor + avg_ServiceFloor
    else:
        height = len(floors) * avg_floor

    print("Estimated Height: {} meters".format(height))
    return height

