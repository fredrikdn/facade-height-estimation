from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

import numpy as np
import json

# TODO: Can also create a query for each building ID using the bbox = footprint, to find contained/nearby address-node

with open('preprocessing/testaddresses.json', 'r', encoding='utf-8') as fa:
    nodes = json.load(fa)

with open('preprocessing/testbuildings.json', 'r', encoding='utf-8') as fw:
    ways = json.load(fw)

print("WAYS: ", len(ways["elements"]))
djscale = 1000000000

for i in range(0, len(ways["elements"])-1):
    b_id = ways["elements"][i]["id"]
    polygon = [[]]

    for j in range(0, len(ways["elements"][i]["nodes"])-1):
        polygon[0].append((ways["elements"][i]["geometry"][j]["lat"], ways["elements"][i]["geometry"][j]["lon"]))

    poly = Polygon(polygon)
    print(poly)

    for n in range(0, len(nodes["elements"]) - 1):
        n_lat = nodes["elements"][n]["lat"]
        n_lon = nodes["elements"][n]["lon"]

        point = Feature(geometry=Point((n_lat, n_lon)))

        if boolean_point_in_polygon(point, poly):
            print("INSIDE")

        else:
            print("OUTSIDE")
