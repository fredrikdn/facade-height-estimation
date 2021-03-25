import math

#Predefined Values (meters)
avg_Floor = 2.5
avg_Roof = avg_Floor
avg_ServiceFloor = 3.0
avg_Door = 2.0

#Calculate window size
size_list = []

#New attributes
height = 0
num_floors = 0
basement = False
door = -1
coords = 'something'
block = False
shop = False

def define_building(floor_List):

    for index, floor in enumerate(floor_List):
        window_size = []
        # Rule 1: Gabled roof with single window
        if len(floor_List) > 1 & len(floor[0]) == 1:
            num_floors == len(floor_List)
        else:
            num_floors == len(floor_List) +1
        # Rule 3: More than 3 windows implies block
        if len(floor_List) > 3:
            block = True

        for obj in floor:
            # Detecting door on facade
            if obj[4] == 1.0:
                door = len(floor_List) - index
        #Sperating size of windows into floors
            else:
                window_size.append(obj[12])
        window_size.append(size_list)

    #Only apply following rules if building have more than 1 floor
    if len(floor_List) > 1:
        #Rule 4: Checking for small windows at lowest floor
        avg_sum = sum(map(sum, size_list))
        if sum(size_list[len(size_list)])/len(size_list[len(size_list)]) < avg_sum/2:
            basement = True
        #Rule 2: Checking for big windows at lowest floor
        if sum(size_list[len(size_list)])/len(size_list[len(size_list)]) > avg_sum*1.5:
            shop = True

    return [num_floors, basement, door, coords, block, shop]



def estimate_height(building_attr):

    height = building_attr[0]*avg_Floor
    #Add extra height if facade contains shop
    if building_attr[5]:
        height += 0.5
    #Add roof height
    #height = (building_attr[0]-1) * avg_Floor

    return height

