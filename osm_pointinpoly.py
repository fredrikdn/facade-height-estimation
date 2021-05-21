import requests
import json
from heightutils import *
from osm_addresses import *
from osm_buildings import *


location = 'preprocessing/'
results = 'results/'
overpass_url = "http://overpass-api.de/api/interpreter"


# Find bounding box for each building footprint
def get_bbox(loc, i):
    with open(loc + 'buildings.json', encoding='utf-8') as f:
        data = json.load(f)

    try:
        bid = data["elements"][i]["id"]
    except KeyError:
        print("BID not found")

    try:
        min_lat = data["elements"][i]["bounds"]["minlat"]

    except KeyError:
        print("Min lat not found")

    try:
        min_lon = data["elements"][i]["bounds"]["minlon"]

    except KeyError:
        print("Min lon not found")

    try:
        max_lon = data["elements"][i]["bounds"]["maxlon"]

    except KeyError:
        print("Max lat not found")

    try:
        max_lat = data["elements"][i]["bounds"]["maxlat"]

    except KeyError:
        print("Max lon not found")

    bbox = [min_lat, min_lon, max_lat, max_lon]

    return bbox, bid


def point_in_poly(boundingbox, bid):
    overpass_query = """
       [out:json];
       (
        node["addr:city"="Trondheim"]({minlat},{minlon},{maxlat},{maxlon});
       );
       out center geom;
       """.format(minlat=boundingbox[0], minlon=boundingbox[1], maxlat=boundingbox[2], maxlon=boundingbox[3])

    # Get json data
    try:
        response = requests.get(overpass_url,
                                params={'data': overpass_query})
    except json.decoder.JSONDecodeError:
        print("No address-node returned")

    try:
        data = response.json()
        print("data: ", data)
    except json.decoder.JSONDecodeError:
        print("Data is None")
        return

    if len(data["elements"]) > 0:

        try:
            city = data["elements"][0]["tags"]["addr:city"]

        except KeyError:
            print("City not found")

        try:
            post = data["elements"][0]["tags"]["addr:postcode"]

        except KeyError:
            print("Postcode not found")

        try:
            street = data["elements"][0]["tags"]["addr:street"]

        except KeyError:
            print("Street not found")

        try:
            num = data["elements"][0]["tags"]["addr:housenumber"]

        except KeyError:
            print("House number not found")

        try:
            address = format_address(city, post, street, num)
        except UnboundLocalError:
            print("Unable to get address")
            return
        height = 0

        # Write CSV file: entry = (building_id, address, b_type, height)
        write_csv(results + 'test_results.csv', bid, address, height)

    else:
        print("No address-node contained in bbox")


if __name__ == '__main__':
    with open('preprocessing/buildings.json', encoding='utf-8') as f:
        data = json.load(f)
    for i in range(0, len(data["elements"]) - 1):
        bbox, bid = get_bbox(location, i)  # the ith element
        print("...")
        point_in_poly(bbox, bid)

