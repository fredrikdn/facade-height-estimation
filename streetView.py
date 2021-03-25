from heightutils import *

pitch = '20'
heading = '0'
size = '640x500'
#location = 'Elgsetergate55,Trondheim'

API_KEY = 'AIzaSyBjbBw8oK8YI8Lnc4ExA-98VU4zmswp2i4'
#request = 'https://maps.googleapis.com/maps/api/streetview?size='+size+'&location='+location+'&heading='+heading+'&pitch='+pitch+'&size=456x456&key=' + API_KEY
totallynotasecret = 'HgCroea_Pd-P48CASC7mA5QfcNk='

#signed_request = 'https://maps.googleapis.com/maps/api/streetview?location=60.425997830817806,5.6270301941489&size=456x456&key=AIzaSyBjbBw8oK8YI8Lnc4ExA-98VU4zmswp2i4&signature=d1CxJKNKGGbNlZlSWsxurQS4pOo='

myloc = 'googleimages/'

# TODO: locations should be gathered from a selected region (i.e. Trondheim) at intervals of x meters in any direction
locations = [
             '63.43087328085278,10.416326917556141',
             '63.43341787203097,10.417870540615437'
             ]


if __name__ == "__main__":

    for loc in locations:

        # TODO: Framework for Python - request with express.js server to return google.maps.getPhotographerPov()
        # This is typically the driving direction for the image
        heading = ''
        request = 'https://maps.googleapis.com/maps/api/streetview?size=' + size + '&location=' + loc + '&heading=' + \
                  heading + '&pitch=' + pitch + '&size=456x456&key=' + API_KEY

        # structure URL and download the image from street view
        input_url = request
        secret = totallynotasecret
        signed = sign_url(input_url, secret)
        print("Signed URL: " + signed)
        get_img(loc, myloc, signed)
