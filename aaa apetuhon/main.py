import requests

import time
from dotenv import find_dotenv, load_dotenv
import os


load_dotenv(find_dotenv())
API_KEY = '9c9903e8-061d-40a0-b834-ad2e7174d45a'
url = f'https://routing.api.2gis.com/carrouting/6.0.0/global?key={API_KEY}'


def get_cords(point):
    response = requests.get(f'https://catalog.api.2gis.com/3.0/items/geocode?q={point}&fields=items.point&key={API_KEY}')
    cords = response.json()['result']['items'][0]['point']
    return cords['lat'], cords['lon']


def get_distance(start_point, finish_point):
    data = {
    "points": [
        {
            "type": "walking",
            "lat": start_point[0],
            "lon": start_point[1]
        },
        {
            "type": "walking",
            "lat": finish_point[0],
            "lon": finish_point[1]
        }
    ],
    "type": "shortest"
    }
    response = requests.post(url, json=data)
    return response.json()['result'][0]['total_distance']



def main():
    points_cords = []
    with open('points.txt', 'r', encoding='utf-8') as f:
        for point in f.readlines():
            point_cords = get_cords(point)
            points_cords.append(point_cords)

    distance_matrix = []
    for start_cords in points_cords:
        row = []
        for cords in points_cords:
            if cords == start_cords:
                row.append(0)
            else:
                row.append(get_distance(start_cords, cords))
        distance_matrix.append(row)
        print(row)
    print(distance_matrix)




if __name__ == "__main__":
    main()