from heightutils import *

pitch = '20'
heading = ''
size = '640x640'
#location = 'Elgsetergate55,Trondheim'

API_KEY = 'AIzaSyBjbBw8oK8YI8Lnc4ExA-98VU4zmswp2i4'
#request = 'https://maps.googleapis.com/maps/api/streetview?size='+size+'&location='+location+'&heading='+heading+'&pitch='+pitch+'&size=456x456&key=' + API_KEY
totallynotasecret = 'HgCroea_Pd-P48CASC7mA5QfcNk='

#signed_request = 'https://maps.googleapis.com/maps/api/streetview?location=60.425997830817806,5.6270301941489&size=456x456&key=AIzaSyBjbBw8oK8YI8Lnc4ExA-98VU4zmswp2i4&signature=d1CxJKNKGGbNlZlSWsxurQS4pOo='

myloc = 'googleimages/'

# TODO: locations/addresses should be gathered from a selected region (i.e. Trondheim)
locations = [
              #'raadyrlia,8,1270,oslo'# Points at the building with the corresponding address / given coordinate
             ]


if __name__ == "__main__":
    locations = getStreet('gloeshaugveien', 'trondheim', '7030')
    for loc in locations:

        request = 'https://maps.googleapis.com/maps/api/streetview?size=' + size + '&location=' + loc + '&heading=' + \
                  heading + '&pitch=' + pitch + '&key=' + API_KEY

        # structure URL and download the image from street view
        input_url = request
        secret = totallynotasecret
        signed = sign_url(input_url, secret)
        print("...")
        #print("Signed URL: " + signed)
        get_img(loc, myloc, signed)
