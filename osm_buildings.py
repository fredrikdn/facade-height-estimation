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
    );
    out center geom;
    """.format(minlat=boundingbox[0], minlon=boundingbox[1], maxlat=boundingbox[2], maxlon=boundingbox[3])


    response = requests.get(overpass_url,
                            params={'data': overpass_query})

    data = response.json()

    # Write file
    with open(location + 'buildings.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    study_area = [63.412924, 10.3993103, 63.4151645, 10.4051818]  # minlat, minlon, maxlat, maxlon
    get_buildings(study_area)

