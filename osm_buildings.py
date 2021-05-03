import requests
import json

location = 'preprocessing/'
overpass_url = "http://overpass-api.de/api/interpreter"


# Get building footprints and attached tags/variables
def get_buildings(area, areacode):

    overpass_query = """
    [out:json];
    area["ISO3166-2"="{ac}"];
    (
     way["building"](area);
    );
    out center geom;
    """.format(a=area, ac=areacode)

    response = requests.get(overpass_url,
                            params={'data': overpass_query})

    data = response.json()

    # Write file
    with open(location + 'buildings.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    get_buildings('Trondheim', 'NO-50')

