from heightutils import *
from js import get_heading

pitch = '20'
heading = ''
size = '640x500'
#location = 'Elgsetergate55,Trondheim'

API_KEY = 'AIzaSyBjbBw8oK8YI8Lnc4ExA-98VU4zmswp2i4'
#request = 'https://maps.googleapis.com/maps/api/streetview?size='+size+'&location='+location+'&heading='+heading+'&pitch='+pitch+'&size=456x456&key=' + API_KEY
totallynotasecret = 'HgCroea_Pd-P48CASC7mA5QfcNk='

#signed_request = 'https://maps.googleapis.com/maps/api/streetview?location=60.425997830817806,5.6270301941489&size=456x456&key=AIzaSyBjbBw8oK8YI8Lnc4ExA-98VU4zmswp2i4&signature=d1CxJKNKGGbNlZlSWsxurQS4pOo='

myloc = 'streetview/googleimages/'

# TODO: locations should be gathered from a selected region (i.e. Trondheim) at intervals of x meters in any direction
locations = [
             'ovrebakklandet11trondheim'  # Points at the building with the corresponding address / given coordinate
             ]

if __name__ == "__main__":

    for loc in locations:

        # TODO: Framework for Python - request (?with express.js server?) to return google.maps.getPhotographerPov()
        # This is typically the driving direction for the image

        #heads = get_heading(loc)  # 2 headings --> for loop
        #heading = heads[0]
        request = 'https://maps.googleapis.com/maps/api/streetview?size=' + size + '&location=' + loc + '&heading=' + \
                  heading + '&pitch=' + pitch + '&size=456x456&key=' + API_KEY

        # structure URL and download the image from street view
        input_url = request
        secret = totallynotasecret
        signed = sign_url(input_url, secret)
        print("Signed URL: " + signed)
        get_img(loc, myloc, signed)
