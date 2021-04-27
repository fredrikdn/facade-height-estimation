import math

# Predefined Values (meters)
avg_Floor = 2.5
avg_Roof = avg_Floor
avg_ServiceFloor = 3.0
avg_Door = 2.0

# Calculate window size
size_list = []

# New attributes
num_floors = 0
basement = False
door = -1
coords = 'something'
block = False
shop = False

#def define_facade(floors):


#def rules():


def estimate_height(floors):
    height = len(floors)*avg_Floor
    #Add extra height if facade contains shop
    #if building_attr[5]:
        #height += 0.5
    #Add roof height
    #height = (building_attr[0]-1) * avg_Floor
    print("Estimated Height: {} meters".format(height))
    return height

