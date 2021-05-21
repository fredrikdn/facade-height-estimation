import requests
import json

location = 'preprocessing/'
overpass_url = "http://overpass-api.de/api/interpreter"


# Get building footprints and attached tags/variables
def get_buildings(boundingbox):

    overpass_query = """
    [out:json];
    (
     way["building"]({minlat},{minlon},{maxlat},{maxlon});
     relation["building"]({minlat},{minlon},{maxlat},{maxlon});
    );
    out center geom;
    """.format(minlat=boundingbox[0], minlon=boundingbox[1], maxlat=boundingbox[2], maxlon=boundingbox[3])

    response = requests.get(overpass_url,
                            params={'data': overpass_query})

    data = response.json()

    # Write file
    with open(location + 'buildings.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_building_type(bid):
    b_type = ''
    with open('preprocessing/buildings.json', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(0, len(data["elements"]) - 1):
        if data["elements"][i]["id"] == bid:
            try:
                b_type = data["elements"][i]["tags"]["building"]
            except KeyError:
                print("Building type not found")

            if b_type == "yes":
                try:
                    b_type = data["elements"][i]["tags"]["amenity"]
                except KeyError:
                    print("Building type (amenity) not found")
        building_type = b_type
    return building_type


def get_building_footprint(bid):
    footprint_list = []
    with open('preprocessing/buildings.json', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(0, len(data["elements"]) - 1):
        if data["elements"][i]["id"] == bid:
            for j in range(0, len(data["elements"][i]["geometry"]) - 1):
                latlon = [data["elements"][i]["geometry"][j]["lat"], data["elements"][i]["geometry"][j]["lon"]]
                footprint_list.append(latlon)

    return footprint_list


if __name__ == '__main__':
    # Gloeshaugveien ==: 63.412924, 10.3993103, 63.4151645, 10.4051818

    study_area = [63.433230, 10.393283, 63.434910, 10.404889]  # minlat, minlon, maxlat, maxlon
    get_buildings(study_area)
    #b_type = get_building_type(38050098)
    #footprint_list = get_building_footprint(38050098)
    #print("FOOTPRINTS: ", footprint_list)

    #print("TYPE: ", b_type)
