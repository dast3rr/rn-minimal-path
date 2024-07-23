import requests


def get_cords(point, API_KEY):
    response = requests.get('https://catalog.api.2gis.com/3.0/items/geocode?q={point}&fields=items.point&key={API_KEY}')
    # return response['result']['items']['point']