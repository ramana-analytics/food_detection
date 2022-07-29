import googlemaps
from pprint import pprint
import json
import requests

API_KEY = 'AIzaSyC_M6uWIjbtfCkPyL5yxrN822KUSLsH91Y'


def GetPatientLocationFromCoord(coord):
    map_client = googlemaps.Client(API_KEY)
    response = map_client.reverse_geocode(coord)
    place_ids = [ place['place_id'] for place in response ]
    place_id = place_ids[0]
    address = [address['formatted_address'] for address in response]
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + place_id + "&fields=name%2Crating%2Cformatted_phone_number&key="+ API_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    place = json.loads(response.text)
    place["address"]=address[0]
    del place["html_attributions"]
    del place["status"]
    place = json.dumps(place)
    return place

# coord = '18.561908947864495, 73.80722483091992'
# print(GetPatientLocationFromCoord(coord))