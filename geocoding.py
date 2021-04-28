import googlemaps
import json


def get_loc(filename):
    API_KEY = 'AIzaSyArcyZT0a2xlsXCDsyUX0Zure6kCYgeVYU'
    gmaps = googlemaps.Client(key=API_KEY)

    address = filename.split('.jpg')[0]

    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    print(geocode_result)

    file = json.dumps(geocode_result)
    loc = json.loads(file)

    location = loc[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']

    #print("Location: ", location)
    #print("Lat: ", lat)
    #print("Lng: ", lng)

    return lat, lng
