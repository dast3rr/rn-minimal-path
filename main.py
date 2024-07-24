import requests

import time
import json

from dotenv import find_dotenv, load_dotenv
import os
import sys
import itertools


load_dotenv(find_dotenv())
API_KEY = '9c9903e8-061d-40a0-b834-ad2e7174d45a'
url = f'https://routing.api.2gis.com/carrouting/6.0.0/global?key={API_KEY}'


def get_from_distances_cache(start_point, finish_point):
    start_point_str = f'{start_point[0]}-{start_point[1]}'
    finish_point_str = f'{finish_point[0]}-{finish_point[1]}'

    all_distances = {}
    with open('aaa apetuhon/data/all_distances.json') as f:
        all_distances = json.load(f)
    
    if start_point_str in all_distances.keys():
        if finish_point_str in all_distances[start_point_str].keys():
            return all_distances[start_point_str][finish_point_str]
    return None
    



def write_to_cache(start_point, finish_point, distance) -> None:
    all_distances = {}

    start_point_str = f'{start_point[0]}-{start_point[1]}'
    finish_point_str = f'{finish_point[0]}-{finish_point[1]}'

    with open('aaa apetuhon/data/all_distances.json') as f:
        all_distances = json.load(f)

    if start_point_str in all_distances.keys():
        all_distances[start_point_str][finish_point_str] = distance
    else:
        all_distances[start_point_str] = {finish_point_str: distance}
    with open('aaa apetuhon/data/all_distances.json', 'w') as f:
        json.dump(all_distances, f)


def get_cords(point):
    response = requests.get(f'https://catalog.api.2gis.com/3.0/items/geocode?q={point}&fields=items.point&key={API_KEY}')
    if response.status_code == 200:
        cords = response.json()['result']['items'][0]['point']
        return cords['lat'], cords['lon']
    else:
        print('Неизвестная ошибка, обратитесь в поддержку(получение координат)')
        sys.exit()


def get_distance(start_point, finish_point):
    distance = get_from_distances_cache(start_point, finish_point)
    if not distance:
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
        if response.status_code == 200:
            distance = response.json()['result'][0]['total_distance']
            write_to_cache(start_point, finish_point, distance)
            return response.json()['result'][0]['total_distance']
        else:
            print('Неизвестная ошибка, обратитесь в поддержку(определение расстояния)')
    return distance


def get_distance_matrix():
    points_cords = []
    points_ids = {}
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'points.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for point in lines:
            point_cords = get_cords(point.strip('\n'))
            if point_cords not in points_cords:
                points_cords.append(point_cords)
            if point.strip('\n') not in points_ids.values():
                points_ids[lines.index(point)] = point.strip('\n')
            

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
    return distance_matrix, points_ids


def tsp_dynamic_programming(dist_matrix, points_ids):

    n = len(dist_matrix)

   

    # Инициализация dp таблицы и пути

    dp = [[float('inf')] * n for _ in range(1 << n)]

    parent = [[-1] * n for _ in range(1 << n)]  # Родитель для восстановления пути

    dp[1][0] = 0  # Начинаем с первой вершины (0)


    # Заполнение dp таблицы

    for mask in range(1, 1 << n):

        for u in range(n):

            if mask & (1 << u):

                for v in range(n):

                    if mask & (1 << v) and u != v:

                        if dp[mask][u] > dp[mask ^ (1 << u)][v] + dist_matrix[v][u]:

                            dp[mask][u] = dp[mask ^ (1 << u)][v] + dist_matrix[v][u]

                            parent[mask][u] = v


    # Находим минимальное расстояние для возвращения в начальную точку

    min_dist = float('inf')

    end_mask = (1 << n) - 1

    last_vertex = -1

    for u in range(1, n):

        if min_dist > dp[end_mask][u] + dist_matrix[u][0]:

            min_dist = dp[end_mask][u] + dist_matrix[u][0]

            last_vertex = u


    # Восстанавливаем путь

    path = []

    mask = end_mask

    while last_vertex != -1:

        path.append(last_vertex)

        next_vertex = parent[mask][last_vertex]

        mask ^= (1 << last_vertex)

        last_vertex = next_vertex

    path.reverse()

    path.append(0)  # Добавляем начальную точку


    # Преобразуем путь в имена вершин

    path_names = [points_ids[i] for i in path]
    path_ids = [i for i in path]


    return path_names, path_ids, min_dist


def floyd_checking(matrix):
    A = [[matrix[i][j] for j in range(len(matrix))] for i in range(len(matrix))] 
    Prev = [[None for j in range(len(matrix))] for i in range(len(matrix))] 
    for k in range(len(matrix)):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if A[i][k] != 0 and A[k][j] != 0 and A[i][k] + A[k][j] < A[i][j]:
                    A[i][j] = A[i][k] + A[k][j]
                    Prev[i][j] = Prev[k][j]
    return matrix == A


def main():
    matrix, points_ids = get_distance_matrix()
    min_path, min_path_ids, min_distance = tsp_dynamic_programming(matrix, points_ids)

    print("Кратчайший путь:", min_path)

    print(min_path_ids)

    print("Минимальное расстояние:", min_distance)

    with open('aaa apetuhon/matrix.txt', 'w', encoding='utf-8') as f:
        for row in matrix:
            f.write(f'{' - '.join([str(n) for n in row])}\n')

    print(floyd_checking(matrix))


if __name__ == "__main__":
    main()