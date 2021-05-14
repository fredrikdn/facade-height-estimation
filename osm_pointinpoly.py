import requests
import json

location = 'preprocessing/'
overpass_url = "http://overpass-api.de/api/interpreter"


# Find bounding box for each building footprint
def get_bbox(loc, i):
    with open(loc + 'test_buildings.json', encoding='utf-8') as f:
        data = json.load(f)

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

    return bbox


def point_in_poly(boundingbox, loc):
    overpass_query = """
       [out:json];
       (
        node["addr:city"="Trondheim"]({minlat},{minlon},{maxlat},{maxlon});
       );
       out center geom;
       """.format(minlat=boundingbox[0], minlon=boundingbox[1], maxlat=boundingbox[2], maxlon=boundingbox[3])


    #  WRITES ADDRESS NODE TO JSON FILE FOR NOW...
    response = requests.get(overpass_url,
                            params={'data': overpass_query})

    data = response.json()

    # Write file
    with open(loc + 'test_output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Write CSV file: entry = (building_id, address)


if __name__ == '__main__':
    bbox = get_bbox(location, 0)  # the ith (0th) element
    print("BBOX: ", bbox)
    point_in_poly(bbox, location)
