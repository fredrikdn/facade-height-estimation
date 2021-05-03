import requests
import json

location = 'preprocessing/addresses.json'


# Fetch addresses from OSM based on area, area code and street
def get_location(area, areacode, street):
    overpass_url = "http://overpass-api.de/api/interpreter"
    if street != '':
        overpass_query = """
        [out:json];
        area["ISO3166-2"="{ac}"];
        (node["addr:street"="{st}"](area);
         way["addr:street"="{st}"](area);
         rel["addr:street"="{st}"](area);
        );
        out center;
        """.format(ac=areacode, st=street)

    else:
        overpass_query = """
        [out:json];
        area["ISO3166-2"="{ac}"];
        (node["addr:city"="{a}"](area);
         way["addr:city"="{a}"](area);
         rel["addr:city"="{a}"](area);
        );
        out center;
        """.format(ac=areacode, a=area)

    response = requests.get(overpass_url,
                            params={'data': overpass_query})

    data = response.json()

    # Write file
    with open(location, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Create addresses in correct format
def structure_data(location):
    with open(location, encoding='utf-8') as f:
        data = json.load(f)

    address_list = []

    for i in range(0, len(data["elements"]) - 1):
        try:
            street = data["elements"][i]["tags"]["addr:street"]
        except KeyError:
            print("Address not found")
            continue
        try:
            num = data["elements"][i]["tags"]["addr:housenumber"]
        except KeyError:
            print("Address not found")
            continue
        try:
            post = data["elements"][i]["tags"]["addr:postcode"]
        except KeyError:
            print("Address not found")
            continue
        try:
            city = data["elements"][i]["tags"]["addr:city"]
        except KeyError:
            print("Address not found")
            continue

        tmp = street + "," + num + "," + post + "," + city
        tmp = ''.join(tmp.split())
        tmp = tmp.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
        print("Addr: ", tmp)
        address_list.append(tmp)
        #print(address_list)

    return address_list


if __name__ == '__main__':
    # List all addresses within the given area and areacode (and streetname)
    get_location('Trondheim', 'NO-50', 'Klæbuveien')
    structure_data(location=location)
