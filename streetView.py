from heightutils import *
from osm_addresses import *

pitch = '20'
heading = ''
size = '640x640'
#location = 'Elgsetergate55,Trondheim'

API_KEY = 'AIzaSyBjbBw8oK8YI8Lnc4ExA-98VU4zmswp2i4'
#request = 'https://maps.googleapis.com/maps/api/streetview?size='+size+'&location='+location+'&heading='+heading+'&pitch='+pitch+'&size=456x456&key=' + API_KEY
totallynotasecret = 'HgCroea_Pd-P48CASC7mA5QfcNk='

#signed_request = 'https://maps.googleapis.com/maps/api/streetview?location=60.425997830817806,5.6270301941489&size=456x456&key=AIzaSyBjbBw8oK8YI8Lnc4ExA-98VU4zmswp2i4&signature=d1CxJKNKGGbNlZlSWsxurQS4pOo='

myloc = 'googleimages/'  # Savelocation for imagery
addr_file = 'preprocessing/addresses.json'  # Addresses from OSM
csv = 'results/kluwerserror.csv'

# TODO: get address from CSV file of pip
# locations/addresses gathered from a selected region (i.e. Trondheim)
csv_list = read_csv(csv)  # structure_data(addr_file)
print(csv_list)

# Get all images of buildings from Google street view from selected region
if __name__ == "__main__":
    for entry in csv_list:
        print("ENTRY: ", entry)
        request = 'https://maps.googleapis.com/maps/api/streetview?size=' + size + '&location=' + entry[1] + '&heading=' + \
                  heading + '&pitch=' + pitch + '&key=' + API_KEY

        # structure URL and download the image from street view
        input_url = request
        secret = totallynotasecret
        signed = sign_url(input_url, secret)
        print("...")

        get_img(entry[1] + '_' + entry[0], myloc, signed)
